"""Tests for escape room game."""

import pytest

import escape


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (
            ["progname"],
            {
                "debug": False,
                "start_room": "intro",
                "transcript_loc": "run.txt",
                "data_path": "data/",
            },
        ),
        (
            ["progname", "-d"],
            {
                "debug": True,
                "start_room": "intro",
                "transcript_loc": "run.txt",
                "data_path": "data/",
            },
        ),
        (
            ["progname", "-s", "SOC"],
            {
                "debug": False,
                "start_room": "soc",
                "transcript_loc": "run.txt",
                "data_path": "data/",
            },
        ),
        (
            ["progname", "-s", "soc"],
            {
                "debug": False,
                "start_room": "soc",
                "transcript_loc": "run.txt",
                "data_path": "data/",
            },
        ),
        (
            ["progname", "--start", "intro", "--transcript", "run.txt"],
            {
                "debug": False,
                "start_room": "intro",
                "transcript_loc": "run.txt",
                "data_path": "data/",
            },
        ),
    ],
)
def test_arg_parsing(monkeypatch, argv, expected) -> None:  # noqa: ANN001
    """Test CLI argument parsing for different inputs."""
    monkeypatch.setattr("sys.argv", argv)

    captured = {}

    class DummyEngine:
        def __init__(
            self,
            debug: bool,
            start_room: str,
            transcript_loc: str,
            data_path: str,
        ) -> bool:
            """Initialize the dummy engine."""
            captured.update(
                {
                    "debug": debug,
                    "start_room": start_room,
                    "transcript_loc": transcript_loc,
                    "data_path": data_path,
                },
            )

        def run(self) -> None:
            """Simulate runnign without REPL loop."""

    # Replace the engine and run main
    monkeypatch.setattr(escape, "Engine", DummyEngine)
    escape.main()

    assert captured == expected


# def test_square() -> None:
# @pytest.mark.xfail(reason="Not yet implemented")
# @pytest.mark.xfail(reason="Not yet implemented")
