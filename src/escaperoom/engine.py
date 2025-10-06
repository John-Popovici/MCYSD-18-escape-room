"""The engine for the escape game."""

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.rooms.soc import Soc


class Engine:
    """Main REPL engine handling user input and room logic."""

    def __init__(
        self,
        debug: bool,
        start_room: str,
        transcript_loc: str,
    ) -> bool:
        """Initialize the game engine."""
        self.debug: bool = debug
        self.game_running: bool = True
        self.transcript_loc: str = transcript_loc

        # Set up game information
        self.inventory: dict[str, dict[str, str]] = {}

        # Set up rooms and current_room
        self.rooms: set[Base] = {Soc("data/")}

        self.current_room: Base
        for room in self.rooms:
            print(f"{start_room} looking for {room.short_name}")
            if start_room in (room.name, room.short_name):
                self.current_room = room

        if self.current_room is None:
            error_msg: str = f"No room {start_room} exists. Please try again."
            raise ValueError(error_msg)

        # Print out introduction
        print("Cyber Escape Room started. Type 'help' for commands.")

    def run(self) -> None:
        """Start the REPL loop."""
        # Game loop
        while self.game_running:
            # Wait input
            command: list[str] = input("> ").lower().strip().split()

            # Process input
            # Handle move, inventory, hint, save, load, quit, look, and other
            match command[0]:
                case "move":
                    raise NotImplementedError
                case "inventory":
                    raise NotImplementedError
                case "hint":
                    raise NotImplementedError
                case "help":
                    raise NotImplementedError
                case "save":
                    raise NotImplementedError
                case "load":
                    raise NotImplementedError
                case "quit":
                    raise NotImplementedError
                case _:
                    # Commands passed into room
                    room_output: RoomOutput = self.current_room.handle_command(
                        room_input=RoomInput(command, self.inventory),
                    )

                    output_string: str = room_output.message

                    # if adding to the message
                    if command[0] == "look" and len(self.rooms) > 1:
                        output_string += "\nDoors lead to:"
                        for room in self.rooms:
                            if self.current_room not in (
                                room.name,
                                room.short_name,
                            ):
                                output_string += f" {room.short_name}"

            print(output_string)
            # Update game state

            # Print out update
