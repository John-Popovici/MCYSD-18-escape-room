"""Vault room implementation."""

import re
from pathlib import Path
from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.utils import item_to_str, log


class Vault(Base):
    """Room handling Vault-related commands."""

    @override
    def __init__(self, data_path: str) -> None:
        """Initialize the Vault room."""
        super().__init__(
            name="Vault Corridor",
            short_name="vault",
            desc="A noisy dump contains safe codes, they need to be checked. "
            + "Who has been trying to get in?",
            items=["vault_dump.txt"],
            files=[f"{data_path}vault_dump.txt"],
        )
        self.inspected_file = False

    @override
    def inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        if room_input.command[1] == "vault_dump.txt":
            output_str: str = "Veriying checksums...\n"

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
        regex_pattern: str = (
            r"S\s*A\s*F\s*E\s*{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*}"
        )
        data: str = Path(file_path).read_text()

        # Perform regex search for all pattern matches
        search: list[tuple[str]] = re.findall(regex_pattern, data)

        # validate all pattern matches
        valid_results: list[tuple[int]] = []
        for a, b, c in search:
            if int(a) + int(b) == int(c):
                valid_results.append((int(a), int(b), int(c)))

        # Log if more than one valid result found
        log("Found multiple valid results:\n")
        for a, b, c in valid_results:
            log(f"[{a}+{b}={c}]\n")

        # TOKEN[SAFE]=a-b-c
        # EVIDENCE[SAFE].MATCH="SAFE{a-b-c}"
        # EVIDENCE[SAFE].CHECK=a+b=c
        (a, b, c) = valid_results[0]
        return (
            "SAFE",
            {
                "TOKEN": f"{a}-{b}-{c}",
                "MATCH": f"SAFE{{{a}-{b}-{c}}}",
                "CHECK": f"{a}+{b}={c}",
            },
        )
