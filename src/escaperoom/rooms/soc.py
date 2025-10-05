"""SOC room implementation."""

from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput


class Soc(Base):
    """Room handling SOC-related commands."""

    def __init__(self) -> None:
        """Initialize the SOC room."""
        super().__init__(
            name="SOC Triage Desk",
            short_name="soc",
            desc="The SSH logs show repeated authentication failures. " +
            "Your task is to identify the most likely attacking subnet.",
            items=["auth.log"],
            file_path="data/auth.log",
        )


    @override
    def _inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        print(f"I am inspecting {room_input.command[1]}")
        raise NotImplementedError


    @override
    def _use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        print(f"I am using {room_input.command[1]}")
        raise NotImplementedError
