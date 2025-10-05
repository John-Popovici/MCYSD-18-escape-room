"""Abstract base class for all room types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class RoomInput:
    """Room interaction input."""

    command: list[str]
    inventory: dict[str, dict[str, str]] = field(default_factory=dict)

@dataclass
class RoomOutput:
    """Room interaction output."""

    success: bool = False
    message: str = ""


class Base(ABC):
    """ABC defining a room interface."""

    def __init__(
        self,
        name: str,
        short_name: str,
        desc: str,
        items: list[str],
        file_path: str,
    ) -> None:
        """Initialize the room with data."""
        self.name: str = name
        self.short_name: str = short_name
        self.desc: str = desc
        self.items: list[str] = items
        self.file_path: str = file_path


    def handle_command(self, room_input: RoomInput) -> RoomOutput:
        """Process player input inside the room."""
        # Handle look, inspect, use
        match room_input.command[0]:
            case "look":
                return self._look()
            case "inspect":
                return self._inspect(room_input)
            case "use":
                return self._use(room_input)
            case _:
                return RoomOutput(
                    success=False,
                    message=f"No such command {room_input.command[0]}",
                )


    def _look(self) -> RoomOutput:
        """Implement game command: look."""
        # Construct output message
        msg: str = f"You are in the {self.name}."
        msg += f"\n{self.desc}"
        if len(self.items) > 0:
            msg += "\nItems to interact with:"
            for item in self.items:
                msg += f" {item}"
        else:
            msg += "\nThere are no items to interact with."

        # Return output
        return RoomOutput(success=True, message=msg)


    @abstractmethod
    def _inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        raise NotImplementedError


    @abstractmethod
    def _use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        raise NotImplementedError
