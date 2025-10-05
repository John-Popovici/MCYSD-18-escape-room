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
    ) -> None:
        """Initialize the game engine."""
        self.debug: bool = debug
        self.start_room: str = start_room
        self.transcript_loc: str = transcript_loc

    def run(self) -> None:  # noqa: C901, PLR0912
        """Start the REPL loop."""
        # Make rooms
        rooms: set[Base] = {Soc()}

        # Make game states
        game_running: bool = True
        inventory: dict[str, dict[str, str]] = {}

        current_room: Base | None = None
        for room in rooms:
            print(f"{self.start_room} looking for {room.short_name}")
            if self.start_room in (room.name, room.short_name):
                current_room = room

        if current_room is None:
            print(f"No starting room {self.start_room} exists. Closing game.")
            return

        # Print out introduction
        print("Cyber Escape Room started. Type 'help' for commands.")

        # Game loop
        while game_running:
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
                    room_output: RoomOutput = current_room.handle_command(
                        room_input=RoomInput(command, inventory))

                    output_string: str = room_output.message

                    # if adding to the message
                    if command[0] == "look":
                        output_string += "\nDoors lead to:"
                        for room in rooms:
                            output_string += f" {room.short_name}"

                    print(output_string)


            # Update game state

            # Print out update

