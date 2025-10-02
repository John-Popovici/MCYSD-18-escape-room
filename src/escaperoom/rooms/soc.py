"""SOC room implementation."""

import Base


class Soc(Base):
    """Room handling SOC-related commands."""

    def __init__(self) -> None:
        """Initialize the SOC room."""
        super().__init__("SOC Room")

    def handle_command(self, command: str) -> bool:
        """Process player input inside the room returning sucess state."""
        print(f"RECEIVED: {command}")
        return True
