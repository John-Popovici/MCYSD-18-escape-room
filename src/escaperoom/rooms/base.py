"""ABC for all room types."""

from abc import ABC, abstractmethod


class Base(ABC):
    """ABC defining a room interface."""

    def __init__(self, name: str) -> None:
        """Initialize the room with data."""
        self.name = name

    @abstractmethod
    def handle_command(self, command: str) -> bool:
        """Process player input inside the room returning sucess state."""

