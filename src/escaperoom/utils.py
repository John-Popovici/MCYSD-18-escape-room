"""Utilities for escape game."""

from pathlib import Path


def print_log(output_str: str) -> None:
    """Print and log the output string."""
    log(output_str)
    print(output_str, end="")  # noqa: T201


def log(output_str: str) -> None:
    """Log the output string."""
    Path("log.log").open("a").write(output_str)  # noqa: SIM115
