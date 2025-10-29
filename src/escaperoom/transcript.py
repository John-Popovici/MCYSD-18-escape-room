"""Transcript logger implementation."""

from pathlib import Path


class TranscriptLogger:
    """Transcript logger."""

    def __init__(self, file: str = "run.txt") -> None:
        """Initialize the transcript logger.

        Args:
            file (str, optional): The file in which the transcript
                                  should be logger. Defaults to "run.txt".

        """
        self.file = file

        # Ensure the transcript directory exists
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        # Ensure the transcript file exists
        if not Path(file).exists():
            open(file, "w", encoding="utf-8").close()

    def log_evidence(self, evidence: str) -> None:
        """Log evidence to the transcript file.

        Args:
            evidence (str): The collected evidence that should
                            be logged in the transcript.

        """
        with open(self.file, "a") as f:
            f.write(evidence)
