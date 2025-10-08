"""Intro room implementation."""

from typing import override

from escaperoom.rooms.base import Base


class Intro(Base):
    """Room defining an intro room."""

    @override
    def __init__(self) -> None:
        """Initialize the intro room."""
        super().__init__(
            name="Intro Lobby",
            short_name="intro",
            desc="A terminal blinks in the corner. "
            + "You feel yourself being watched.",
        )
