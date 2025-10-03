"""CLI entry point (REPL)."""
import argparse


def main() -> None:
    """Escape room setup method."""
    parser = argparse.ArgumentParser()

    # Parse arguments
    parser.add_argument(
        "-s", "--start", dest = "start_room", default = "intro",
        help = "Starting location",
    )
    parser.add_argument(
        "-t", "--transcript", dest = "transcript_loc", default = "run.txt",
        help = "Trsanscript file",
    )
    args = parser.parse_args()

    print(f"Starting in {args.start_room} and saving to {args.transcript_loc}")
    print(square(5))
    print(square_wrong(5))

    # Generate rooms


def square(a: int) -> int:
    """Square a number correctly."""
    return a**2


def square_wrong(a: int) -> int:
    """Square a number incorrectly."""
    return a + a


if __name__ == "__main__":
    main()
