"""CLI entry point (REPL)."""

import argparse
from argparse import Namespace

from escaperoom.engine import Engine


def main() -> None:
    """Parse arguments and start the game."""
    parser = argparse.ArgumentParser()

    # Parse arguments
    _ = parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Enable debug output",
    )
    _ = parser.add_argument(
        "-s",
        "--start",
        dest="start_room",
        default="intro",
        help="Starting location",
    )
    _ = parser.add_argument(
        "-t",
        "--transcript",
        dest="transcript_loc",
        default="run.txt",
        help="Transcript file",
    )
    args: Namespace = parser.parse_args()

    try:
        # Create and run game engine
        engine: Engine = Engine(
            debug=args.debug,  # pyright: ignore[reportAny]
            start_room=args.start_room,  # pyright: ignore[reportAny]
            transcript_loc=args.transcript_loc,  # pyright: ignore[reportAny]
        )
        engine.run()
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
