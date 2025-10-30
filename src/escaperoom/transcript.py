"""Transcript logger implementation."""

from pathlib import Path

from escaperoom.utils import item_to_str


class TranscriptLogger:
    """Transcript logger."""

    def __init__(self, file: str = "run.txt") -> None:
        """Initialize the transcript logger.

        Args:
            file (str, optional): The file in which the transcript
                                  will be saved. Defaults to "run.txt".

        """
        self.file = file

        # Ensure the transcript directory exists
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        # Clean transcript
        with open(file, "w", encoding="utf-8") as f:
            f.write("")

    def log_inventory(
        self,
        inventory: dict[str, dict[str, str]],
    ) -> None:
        """Log inventory to the transcript file.

        Args:
            inventory (dict[str, dict[str, str]]):
                The inventory that should
                be logged to the transcript.

        """
        with open(self.file, "a", encoding="utf-8") as f:
            f.writelines(
                item_to_str(item_name, item_data)
                for item_name, item_data in inventory.items()
            )
