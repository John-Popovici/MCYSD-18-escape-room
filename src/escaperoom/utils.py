"""Utilities for escape game."""

import traceback
from pathlib import Path


def print_log(output_str: str) -> None:
    """Print and log the output string."""
    log(output_str)
    print(output_str, end="")  # noqa: T201


def log(output_str: str) -> None:
    """Log the output string."""
    Path("log.log").open("a").write(output_str)  # noqa: SIM115


def item_to_str(item_name: str, item_data: dict[str, str]) -> str:
    """Convert item dictionary entry to string representation."""
    try:
        output_str: str = ""

        # Add token value
        output_str += f"TOKEN[{item_name}]={item_data['TOKEN']}\n"

        # Add evidence list
        for entry, data in item_data.items():
            if entry != "TOKEN":
                output_str += f"EVIDENCE[{item_name}].{entry}={data}\n"

        return output_str
    except Exception:  # noqa: BLE001
        # Log exception
        log("Error in parsing item.\n")
        tb_str: str = traceback.format_exc()
        log(tb_str)

        # Simple casting
        return str(f"{item_name}={item_data!s}") + "\n"
