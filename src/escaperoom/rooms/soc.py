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
    
def find_right_subnet(ip_list) -> str :
    ip_dict={}
    sub_dict={}
    for i in ip_list:
        if i in ip_dict:
            ip_dict[i]+=1
        else:
            ip_dict.update({i: 1})            
    """Remove last part of ip and replace it with subnet"""
    for i in ip_dict:
        subnet_ip= i.split('.')
        subnet_ip.pop()
        subnet_prefinal= ('.').join(subnet_ip)
        subnet_final= subnet_prefinal + ".0/24"
        
        if subnet_final in sub_dict:
            sub_dict[subnet_final]+= 1
        else:
            sub_dict.update({subnet_final: 1})          
    """Find most used subnet with .get to find the highest value"""       
    most_used_subnet= max(sub_dict, key= sub_dict.get)
    
    return most_used_subnet, sub_dict[most_used_subnet]
        
 
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
