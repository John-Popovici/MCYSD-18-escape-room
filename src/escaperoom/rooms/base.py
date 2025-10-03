"""Abstract base class for all room types."""

from abc import ABC, abstractmethod


class Base(ABC):
    """ABC defining a room interface."""

    def __init__(self, name: str, file_path: str) -> None:
        """Initialize the room with data."""
        self.name = name
        self.file_path = file_path

    @abstractmethod
    def handle_command(self, command: str) -> bool:
        """Process player input inside the room returning sucess state."""

