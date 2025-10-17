"""SOC room implementation."""

from typing import override

import re
import ipaddress

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.utils import item_to_str

def parse_failed_ip(line: str) -> tuple[str, str | None]:
    """Checks each line if they have the right construction"""
    if "Failed password" not in line:
        return ("irrelevant", None)
    elif " from " not in line:
        return("malformed", None)
        
    ip_addr = line.find(" from ")
    """Finds the right index for the IP address"""
    tail_ip_addr = line[ip_addr + len(" from "):]
    """Checks if the IP has the right format"""
    match_ip = re.search( r'\d+(?:\.\d+){3}', tail_ip_addr)
    
    if match_ip is None:
        return ("malformed", None)
    ip_str = match_ip.group()    
    
    try:
        ipaddress.IPv4Address(ip_str)
    except ValueError:
        return ("malformed", None)
    return("failed", ip_str)

def collect_failed_ip(file_path) -> tuple[list[str], int]:
    """Opens the file, checks each line for status and ip and if failed login -> added to failed_ip"""
    with open(file_path, encoding='utf-8') as f:
        failed_ip=[]
        malformed_count= 0
        for line in f:
            status, ip = parse_failed_ip(line)
            if status == "failed":
                failed_ip.append(ip)
            elif status == "malformed":
                malformed_count += 1
            else:
                continue
        return failed_ip, malformed_count
 
class Soc(Base):
    """Room handling SOC-related commands."""

    @override
    def __init__(self, data_path: str) -> None:
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
    def inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        if room_input.command[1] == "auth.log":
            output_str: str = "Parsing logs...\n"

            # Solve the room challenge
            [item_name, item_data] = self.solve(self.files[0])
            output_str += item_to_str(item_name, item_data)

            # Add data to inventory
            room_input.inventory[item_name] = item_data

            self.inspected_file = True
            return RoomOutput(
                success=True,
                message=output_str,
            )
        return super().inspect(room_input)

    @override
    def use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        return super().inspect(room_input)

    @override
    def hint(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: hint."""
        output_str: str = ""
        if self.inspected_file:
            output_str += "You have everything you need from this room.\n"
        else:
            output_str += "You feel there is something in this room to do.\n"
        return RoomOutput(
            success=True,
            message=output_str,
        )

    def solve(self, file_path: str) -> (str, dict[str, str]):
        """Solves the room challenge."""
        # return (
        #     "KEYPAD",
        #     {
        #         "TOKEN": "4217",
        #         "TOP24": "blahblah",
        #         "COUNT": "whatever",
        #     },
        # )
        raise NotImplementedError
