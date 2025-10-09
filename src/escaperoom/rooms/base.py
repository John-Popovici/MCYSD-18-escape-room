"""Abstract base class for all room types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


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

    @abstractmethod
    def __init__(
        self,
        name: str,
        short_name: str,
        desc: str,
        items: list[str] | None = None,
        files: list[str] | None = None,
    ) -> None:
        """Initialize the room with data."""
        if items is None:
            items = []
        self.name: str = name
        self.short_name: str = short_name
        self.names: set[str] = {self.name, self.short_name}
        self.desc: str = desc
        self.items: list[str] = items
        self.files: list[str] | None = files

        # Check all files exist
        if files is not None:
            for file in files:
                if not Path(file).exists():
                    error_msg: str = f"No such data file {file} exists.\n"
                    raise FileNotFoundError(error_msg)

    def handle_command(self, room_input: RoomInput) -> RoomOutput:
        """Process player input inside the room."""
        # Handle look, inspect, use
        match room_input.command[0]:
            case "look":
                return self.look()
            case "inspect":
                return self.inspect(room_input)
            case "use":
                return self.use(room_input)
            case "hint":
                return self.hint(room_input)
            case _:
                return RoomOutput(
                    success=False,
                    message=f"No such command {room_input.command[0]}.\n",
                )

    @abstractmethod
    def hint(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: hint."""
        raise NotImplementedError

    def look(self) -> RoomOutput:
        """Implement game command: look."""
        # Construct output message
        msg: str = f"You are in the {self.name}.\n"
        msg += f"{self.desc}\n"
        if self.items is not None and len(self.items) > 0:
            msg += "Items to interact with:"
            for item in self.items:
                msg += f" {item}"
            msg += "\n"
        else:
            msg += "There are no items to interact with.\n"

        # Return output
        return RoomOutput(
            success=True,
            message=msg,
        )

    def inspect(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect."""
        return RoomOutput(
            success=False,
            message=f"No such item {room_input.command[1]} to inspect.\n",
        )

    def use(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: use."""
        return RoomOutput(
            success=False,
            message=f"No such item {room_input.command[1]} to use.\n",
        )
