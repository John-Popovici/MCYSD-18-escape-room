"""Intro room implementation."""

from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput


class Intro(Base):
    """Room defining an intro room."""

    def __init__(self) -> None:
        """Initialize the intro room."""
        super().__init__(
            name="Intro Lobby",
            short_name="intro",
            desc="A terminal blinks in the corner. "
            + "You feel yourself being watched.",
        )

    @override
    def _inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        return RoomOutput(False, f"No such item {room_input.command[1]}.\n")

    @override
    def _use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        return RoomOutput(False, f"No such item {room_input.command[1]}.\n")
