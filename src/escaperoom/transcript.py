import os

class TranscriptLogger:
    """Transcript logger."""
    
    def __init__(self, file: str = "run.txt"):
        self.file = file
        
        # Ensure the transcript directory exists
        os.makedirs(os.path.dirname(file) or ".", exist_ok=True)
        # Ensure the transcript file exists
        if not os.path.exists(file):
            open(file, "w", encoding="utf-8").close()
        
    def log_evidence(self, evidence: str):
        """This functions logs evidence to the transcript file.

        Args:
            evidence (str): The collected evidence that should be logged in the transcript.
        """
        with open(self.file, "a") as f:
            f.write(evidence)