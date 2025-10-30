"""The engine for the escape game."""

import textwrap

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.rooms.dns import Dns
from escaperoom.rooms.intro import Intro
from escaperoom.rooms.malware import Malware
from escaperoom.rooms.soc import Soc
from escaperoom.rooms.vault import Vault
from escaperoom.transcript import TranscriptLogger
from escaperoom.utils import log, print_log


class Engine:
    """Main REPL engine handling user input and room logic."""

    def __init__(
        self,
        debug: bool,
        start_room: str,
        transcript_loc: str,
        data_path: str,
    ) -> None:
        """Initialize the game engine."""
        self.debug: bool = debug
        self.game_running: bool = True

        # Set up transcript file
        self.transcript_loc: str = transcript_loc
        self.transcript_logger = TranscriptLogger(file=self.transcript_loc)

        # Set up log
        log_str: str = "-------------------------------\n"
        log_str += "New game generated:\n"
        log_str += f"debug = {debug}\n"
        log_str += f"start_room = {start_room}\n"
        log_str += f"transcript_loc = {transcript_loc}\n"
        log_str += f"data_path = {data_path}\n"
        log(log_str)

        # Set up game information
        self.inventory: dict[str, dict[str, str]] = {}

        # Set up rooms and current_room
        self.rooms: set[Base] = {
            Intro(),
            Soc(self.transcript_logger, data_path),
            Dns(self.transcript_logger, data_path),
            Vault(self.transcript_logger, data_path),
            Malware(self.transcript_logger, data_path),
        }

        self.current_room: Base = self.set_start_room(self.rooms, start_room)

        # Print out introduction
        print_log("Cyber Escape Room started. Type 'help' for commands.\n")

    def run(self) -> None:
        """Start the REPL loop."""
        # Game loop
        while self.game_running:
            # Wait input
            command: list[str] = self.get_input()

            # Process command
            output_str: str = self.handle_command(command)
            print_log(output_str)

    @staticmethod
    def set_start_room(rooms: set[Base], start_room: str) -> Base:
        """Search for starting room in defined rooms."""
        temp_current_room: Base | None = None
        for room in rooms:
            if start_room in room.names:
                temp_current_room = room
                break

        # Determine if room was found
        if temp_current_room is None:
            error_msg: str = f"No room {start_room} exists.\n"
            raise ValueError(error_msg)
        return temp_current_room

    @staticmethod
    def get_input() -> list[str]:
        """Get and normalize user input."""
        input_str: str = input("> ").lower().strip()
        log("> " + input_str + "\n")
        return input_str.split()

    def handle_command(self, command: list[str]) -> str:
        """Process user commands and return output string."""
        # Handle engine commands move, inventory, hint, save, load, quit
        match command[0]:
            case "move":
                return self.move(command)
            case "inventory":
                return self.show_inventory()
            case "help":
                return self.help()
            case "save":
                raise NotImplementedError
            case "load":
                raise NotImplementedError
            case "quit":
                return self.quit()
            case _:
                return self.handle_room_command(command)

    def handle_room_command(self, command: list[str]) -> str:
        """Delegate command to the current room and handle special cases."""
        # Commands passed into room
        room_output: RoomOutput = self.current_room.handle_command(
            room_input=RoomInput(command, self.inventory),
        )
        log("RoomOutput_sucess=" + str(room_output.success) + "\n")
        log("RoomOutput_message=" + room_output.message + "\n")

        # Handle special cases
        match command[0]:
            case "look":
                return self.look(room_output)
            case "hint":
                return self.hint(room_output)
            case _:
                return room_output.message

    def hint(self, room_output: RoomOutput) -> str:
        """Implement engine layer for game command: hint."""
        return room_output.message

    def look(self, room_output: RoomOutput) -> str:
        """Implement engine layer for game command: look."""
        output_str: str = room_output.message
        if len(self.rooms) > 1:
            doors: list[str] = [
                room.short_name
                for room in self.rooms
                if self.current_room is not room
            ]
            output_str += "Doors lead to: " + ", ".join(doors) + "\n"

        return output_str

    def quit(self) -> str:
        """Implement game command: quit."""
        self.game_running = False

        self.transcript_logger.log_inventory(self.inventory)

        return "Goodbye. Transcript written to run.txt\n"

    def move(self, command: list[str]) -> str:
        """Implement game command: move."""
        # If no room specified
        if len(command) == 1:
            return "Specify a move room target.\n"

        # If already in the room
        if command[1] in self.current_room.names:
            return f"You are already in the {self.current_room.name}.\n"

        # Search for destination room
        for room in self.rooms:
            if command[1] in room.names:
                self.current_room = room
                return self.current_room.look().message

        # No room found
        return f"No such room {command[1]}.\n"

    def help(self) -> str:
        """Implement game command: help.

        Returns:
            str: The response of the command.

        """
        return textwrap.dedent("""
        About
        -----
        Your goal is to explore and solve puzzles in different rooms.
        Each room presents unique challenges which you must solve
        in order to progress.

        Use commands to look around, move between rooms,
        collect items, and figure out how to escape.
        Type commands in the prompt to interact with the game world.


        Available commands
        ------------------

        - help            Show this help message
        - hint            Display a gameplay hint
        - move <room>     Move to a different room
        - inventory       Show your current inventory
        - save            Save the current game state
        - load            Load a previously saved game
        - quit            Exit the game
        - inspect <item>  Interact with an item
        - use <item>      Interact with an item
        - interact <item> Interact with an item
        \n
        """)

    def show_inventory(self) -> str:
        """Implement game command: inventory.

        Returns:
            str: The response of the command.

        """
        output_str = (
            "You currently hold: " + ", ".join(self.inventory.keys()) + "\n"
        )

        if not self.inventory:
            output_str = "You do not have any items in your inventory.\n"

        return output_str
