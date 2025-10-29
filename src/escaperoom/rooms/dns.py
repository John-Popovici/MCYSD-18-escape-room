"""DNS Closet room implementation."""

import base64
import binascii
import configparser
from pathlib import Path
from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.transcript import TranscriptLogger
from escaperoom.utils import item_to_str


class Dns(Base):
    """A room presenting a configuration analysis and decoding challenge."""

    @override
    def __init__(
        self,
        transcript_logger: TranscriptLogger,
        data_path: str,
    ) -> None:
        """Initialize the DNS Closet room."""
        super().__init__(
            name="DNS Closet",
            short_name="dns",
            desc="The walls are covered with scribbled key=value pairs...",
            items=["dns.cfg"],
            files=[f"{data_path}dns.cfg"],
        )
        self.transcript_logger=transcript_logger
        self.inspected_file = False

    @override
    def interact(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect, use, interact."""
        if room_input.command[1] == "dns.cfg":
            # Ensure interaction only happens once
            if self.inspected_file:
                return RoomOutput(
                    success=False,
                    message="This has already been inspected.\n",
                )

            # Solve the room challenge
            output_str: str = "Decoding hints...\n"
            item_name, item_data = self.solve(self.files[0])
            output_str += item_to_str(item_name, item_data)

            # Log evidence in transcript
            self.transcript_logger.log_evidence(
                item_to_str(item_name, item_data),
            )

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
            output_str += ("You feel there is something in " +
            "this room to inspect.\n")
        return RoomOutput(
            success=True,
            message=output_str,
        )

    def solve(self, file_path: str) -> tuple[str, dict[str, str]]:
        """Solves the room challenge."""
        data = Path(file_path).read_text()

        config = configparser.ConfigParser(allow_no_value=True, strict=False)
        config.read_string("[DEFAULT]\n" + data)
        cfg = dict(config["DEFAULT"])

        # Decode all hints
        hints = {}
        for key, val in cfg.items():
            if key.startswith("hint"):
                try:
                    hints[key] = base64.b64decode(val).decode("utf-8")
                except (TypeError, binascii.Error, UnicodeDecodeError):
                    hints[key] = None

        # Find token: decode token_tag to get hint number
        tag = base64.b64decode(cfg["token_tag"]).decode("utf-8")
        target = f"hint{tag}"
        token = hints[target].split()[-1].removesuffix(".")

        return (
            "DNS",
            {
                "TOKEN": token,
                "KEY": target,
                "DECODED_LINE": hints[target],
            },
        )
