"""Final Gate room implementation."""

from typing import override

from escaperoom.rooms.base import Base, RoomInput, RoomOutput
from escaperoom.utils import item_to_str


class Final(Base):
    """The final gate room."""

    @override
    def __init__(self, data_path: str) -> None:
        """Initialize the Final Gate room."""
        super().__init__(
            name="Final Gate",
            short_name="final",
            desc="You stand before the Final Gate. "
            + "The console asks for proof.",
            items=["gate"],
            files=[f"{data_path}final_gate.txt"],
        )
        self.inspected_file = False

    @override
    def interact(self, room_input: RoomInput) -> RoomOutput:
        """Implement game command: inspect, use, interact."""
        if room_input.command[1] == "gate":
            # Ensure interaction only happens once
            if self.inspected_file:
                return RoomOutput(
                    success=False,
                    message="The gate has already been inspected.\n",
                )

            # Check if the user has collected the necessary evidence
            if all(
                k in room_input.inventory
                for k in ("DNS", "SAFE", "PID", "KEYPAD")
            ):

                # Solve the room challenge
                output_str: str = "Collected tokens: \n"
                [item_name, item_data] = self.solve(
                    self.files[0], room_input.inventory,
                )
                output_str: str = item_to_str(item_name, item_data)

                # Add data to inventory
                room_input.inventory[item_name] = item_data

                self.inspected_file = True
                return RoomOutput(
                    success=True,
                    message=output_str,
                )

            collected = {}
            for token in room_input.inventory:
                collected[token] = room_input.inventory.get(token).get("TOKEN")

            collected_tokens_str = ", ".join(
                [f"{k}={v}" for k, v in collected.items()],
            )
            output_str = f"Collected tokens: {collected_tokens_str}\n"
            output_str += "Not all tokens found. The gate remains locked.\n"

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
            output_str += ("There is nothing left to do.\n" +
            "You breathe a sigh of relief.\n")
        else:
            output_str += ("Do you dare use the gate? " +
            "It stands before you, beckoning.\n")
        return RoomOutput(
            success=True,
            message=output_str,
        )

    def solve(
        self,
        file_path: str,
        inventory: dict[str, dict[str, str]],
    ) -> tuple[str, dict[str, str]]:
        """Solves the room challenge."""
        with open(file_path, encoding="utf-8") as f:
            data: str = f.read()

        group_id = ""
        expected_hmac = ""
        token_order = []

        for line in data.splitlines():
            if "=" in line:
                if line.startswith("group_id"):
                    group_id = line.split("=")[1]
                elif line.startswith("expected_hmac"):
                    expected_hmac = line.split("=")[1]
                elif line.startswith("token_order"):
                    token_order = line.split("=")[1].split(",")

        tokens = [inventory.get(token).get("TOKEN") for token in token_order]

        return (
            "FINAL",
            {
                "FINAL_GATE": "PENDING",
                "MSG": f"{group_id}|{'-'.join(tokens)}",
                "EXPECTED_HMAC": expected_hmac,
            },
        )
