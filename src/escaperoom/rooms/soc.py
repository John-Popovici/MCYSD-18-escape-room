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
            desc="The SSH logs show repeated authentication failures. "
            + "Your task is to identify the most likely attacking subnet.",
            items=["auth.log"],
            files=[f"{data_path}auth.log"],
        )

    @override
    def _inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        msg: str = ""
        success: bool = False
        if room_input.command[1] == "auth.log":
            msg += f"I am inspecting {self.files[0]}.\n"
            msg += f"File is {Path(self.files[0]).exists()}.\n"
            success = True
        else:
            msg += f"No such item {room_input.command[1]}.\n"
        return RoomOutput(success=success, message=msg)

    @override
    def _use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        raise NotImplementedError
