"""SOC room implementation."""

from pathlib import Path
from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput


class Soc(Base):
    """Room handling SOC-related commands."""

    def __init__(self, data_path: str) -> None:
        """Initialize the SOC room."""
        super().__init__(
            name="SOC Triage Desk",
            short_name="soc",
            desc="The SSH logs show repeated authentication failures. " +
            "Your task is to identify the most likely attacking subnet.",
            items=["auth.log"],
        )
        self.file_path: str = f"{data_path}auth.log"


    @override
    def _inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        msg: str = ""
        success: bool = False
        if room_input.command[1] == "auth.log":
            msg += f"I am inspecting {self.file_path}"
            msg += f"\nFile is {Path(self.file_path).exists()}"
            success = True
        else:
            msg += f"No such item {room_input.command[1]}."
        return RoomOutput(success=success, message=msg)
        raise NotImplementedError


    @override
    def _use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        print(f"I am using {room_input.command[1]}")
        raise NotImplementedError
