"""SOC room implementation."""

from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.utils import item_to_str


class Soc(Base):
    """Room handling SOC-related commands."""

    @override
    def __init__(self, data_path: str) -> None:
        """Initialize the SOC room."""
        super().__init__(
            name="SOC Triage Desk",
            short_name="soc",
            desc="The SSH logs show repeated authentication failures. "
            + "Someone - or something - has been trying to gain access.",
            items=["auth.log"],
            files=[f"{data_path}auth.log"],
        )
        self.inspected_file = False

    @override
    def interact(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect, use, interact."""
        if room_input.command[1] == "auth.log":
            # Ensure interaction only happens once
            if self.inspected_file:
                return RoomOutput(
                    success=False,
                    message="This has already been inspected.\n",
                )

            # Solve the room challenge
            output_str: str = "Parsing logs...\n"
            [item_name, item_data] = self.solve(self.files[0])
            output_str += item_to_str(item_name, item_data)

            # Add data to inventory
            room_input.inventory[item_name] = item_data

            self.inspected_file = True
            return RoomOutput(
                success=True,
                message=output_str,
            )
        return super().interact(room_input)

    @override
    def hint(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: hint."""
        output_str: str = ""
        if self.inspected_file:
            output_str += "You have everything you need from this room.\n"
        else:
            output_str += "You feel there is something in this room to do.\n"
        return RoomOutput(
            success=True,
            message=output_str,
        )

    def solve(self, file_path: str) -> (str, dict[str, str]):
        """Solves the room challenge."""
        # return (
        #     "KEYPAD",
        #     {
        #         "TOKEN": "4217",
        #         "TOP24": "blahblah",
        #         "COUNT": "whatever",
        #     },
        # )
        raise NotImplementedError
