"""CLI entry point (REPL)."""

import argparse
import traceback
from argparse import Namespace

from escaperoom.engine import Engine
from escaperoom.utils import log, print_log


def main() -> None:
    """Parse arguments and start the game."""
    parser = argparse.ArgumentParser()

    # Parse arguments
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Enable debug output",
    )
    parser.add_argument(
        "-s",
        "--start",
        dest="start_room",
        default="intro",
        help="Starting location",
    )
    parser.add_argument(
        "-t",
        "--transcript",
        dest="transcript_loc",
        default="run.txt",
        help="Transcript file",
    )
    parser.add_argument(
        "-p",
        "--data-path",
        dest="data_path",
        default="data/",
        help="Path to data directory",
    )
    args: Namespace = parser.parse_args()

    try:
        # Create and run game engine
        engine: Engine = Engine(
            debug=args.debug,
            start_room=args.start_room.lower(),
            transcript_loc=args.transcript_loc,
            data_path=args.data_path,
        )
        engine.run()
    except ValueError as e:
        print_log(str(e))
        tb_str: str = traceback.format_exc()
        log(tb_str)
    except FileNotFoundError as e:
        print_log(str(e))
        tb_str: str = traceback.format_exc()
        log(tb_str)
    except Exception:  # noqa: BLE001 # logging used in testing
        print_log("An error has occured. See log for details.\n")
        tb_str: str = traceback.format_exc()
        log(tb_str)


if __name__ == "__main__":
    main()
