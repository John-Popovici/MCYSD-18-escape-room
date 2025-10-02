"""CLI entry point (REPL)."""
import argparse


def main() -> None:
    """Escape room setup method."""
    parser = argparse.ArgumentParser()

    # python escape.py --start intro --transcript run.txt
    parser.add_argument(
        "-s", "--start", dest = "start", default = "intro",
        help = "Starting location",
    )
    parser.add_argument(
        "-t", "--transcript", dest = "transcript", default = "run.txt",
        help = "Trsanscript file",
    )

    print("Hello from mcysd-18-escape-room!")
    print(square(5))
    print(square_wrong(5))


def square(a: int) -> int:
    """Square a number correctly."""
    return a**2


def square_wrong(a: int) -> int:
    """Square a number incorrectly."""
    return a + a


if __name__ == "__main__":
    main()
