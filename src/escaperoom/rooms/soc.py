"""SOC room implementation."""

import ipaddress as ipa
import re
from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.utils import item_to_str


class Soc(Base):
    """Room handling SOC-related commands."""

    @override
    def __init__(
        self,
        data_path: str,
    ) -> None:
        """Initialize the SOC room."""
        super().__init__(
            name="SOC Triage Desk",
            short_name="soc",
            desc="The SSH logs show repeated authentication failures. "
            + "Someone - or something - has been trying to gain access.",
            items=["auth.log"],
            files=[f"{data_path}auth.log"],
        )
        self.inspected_file = False

    @override
    def interact(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect, use, interact."""
        if room_input.command[1] == "auth.log":
            # Ensure interaction only happens once
            if self.inspected_file:
                return RoomOutput(
                    success=False,
                    message="This has already been inspected.\n",
                )

            # Solve the room challenge
            output_str: str = "Parsing logs...\n"
            [item_name, item_data] = self.solve(self.files[0])
            output_str += item_to_str(item_name, item_data)

            # Add data to inventory
            room_input.inventory[item_name] = item_data

            self.inspected_file = True
            return RoomOutput(
                success=True,
                message=output_str,
            )
        return super().interact(room_input)

    @override
    def hint(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: hint."""
        output_str: str = ""
        if self.inspected_file:
            output_str += "You have already verified the authentication log.\n"
        else:
            output_str += "You feel there is something in this room to do.\n"
        return RoomOutput(
            success=True,
            message=output_str,
        )

    def solve(self, file_path: str) -> (str, dict[str, str]):
        """Solve the room challenge.

        Uses a temporary variable to process failed IPs and create the TOKEN.
        """
        failed_ips, malformed_count = self.collect_failed_ip(file_path)
        if not failed_ips:
            return ("KEYPAD", {"TOKEN" : "NONE"})
        very_used_subnet, count_subnet  = self.find_right_subnet(failed_ips)

        # Inside of final_ip, because ruff check asked for it
        final_ip = [
            ip for ip in failed_ips
            if ipa.IPv4Address(ip) in ipa.IPv4Network(very_used_subnet)
        ]

        # Check the most used IP for the TOKEN creation
        top_ip = max(final_ip, key=final_ip.count)
        # Picks one line in the auth.log file containing the most used ip
        sample_line = ""
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if top_ip in line:
                    sample_line = line.strip()
                    break

        # Just keep the last octet for the TOKEN
        final_token= top_ip.split(".")[3]
        # TOKEN construction
        token_final = final_token + str(count_subnet)

        return (
            "KEYPAD",
            {
                "TOKEN": token_final,
                "TOP24": very_used_subnet,
                "COUNT": str(count_subnet),
                "SAMPLE": sample_line,
                "MALFORMED_SKIPPED": malformed_count,
            },
        )

    def find_right_subnet(self, ip_list:list) -> str :
        """Find the most used subnet."""
        ip_dict={}
        for i in ip_list:
            if i in ip_dict:
                ip_dict[i]+=1
            else:
                ip_dict.update({i: 1})

        # Remove last part of ip and replace it with subnet
        sub_dict={}
        for i, count in ip_dict.items():
            subnet_ip= i.split(".")
            subnet_ip.pop()
            subnet_prefinal= (".").join(subnet_ip)
            subnet_final= subnet_prefinal + ".0/24"

            if subnet_final in sub_dict:
                sub_dict[subnet_final]+= count
            else:
                sub_dict.update({subnet_final: count})

        # Find most used subnet with .get to find the highest value
        most_used_subnet= max(sub_dict, key= sub_dict.get)

        return most_used_subnet, sub_dict[most_used_subnet]

    def parse_failed_ip(self, line: str) -> tuple[str, str | None]:
        """Check through the file and returns the ip's."""
        if "password" not in line:
            return ("malformed", None)
        if "Failed password" not in line:
            return ("irrelevant", None)
        if " from " not in line:
            return("malformed", None)
        # Check each line if they have the right construction
        ip_addr = line.find(" from ")
        # Find the right index for the IP address
        tail_ip_addr = line[ip_addr + len(" from "):]
        # Check if the IP has the right format
        match_ip = re.search( r"\d+(?:\.\d+){3}", tail_ip_addr)

        if match_ip is None:
            return ("malformed", None)
        ip_str = match_ip.group()

        try:
            ipa.IPv4Address(ip_str)
        except ValueError:
            return ("malformed", None)
        return("failed", ip_str)

    def collect_failed_ip(self, file_path:str) -> tuple[list[str], int]:
        """Open the file.

        Checks each line for status and IP; appends failed-login IPs to a list
        and increments a counter for malformed lines.
        """
        with open(file_path, encoding="utf-8") as f:
            failed_ip=[]
            malformed_count= 0
            for line in f:
                status, ip = self.parse_failed_ip(line)
                if status == "failed":
                    failed_ip.append(ip)
                elif status == "malformed":
                    malformed_count += 1
                else:
                    continue
            return failed_ip, malformed_count
