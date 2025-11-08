"""Tests escape room game engine."""

import pytest

from escaperoom.engine import Engine


def test_engine_repl_run(monkeypatch, tmp_path) -> None:  # noqa: ANN001
    """Simulate a short REPL run with real rooms and fake input."""
    # Engine
    engine = Engine(
        debug=False,
        start_room="intro",
        transcript_loc=str(tmp_path / "transcript.txt"),
        data_path="data/",
    )

    # Simulated input
    inputs = [
        ["help"],
        ["inventory"],
        ["move", "soc"],
        ["move"],
        ["move", "soc"],
        ["move", "bloo"],
        ["look"],
        ["save"],
        ["save", "save.json"],
        ["load"],
        ["load", "save.jso"],
        ["load", "save.json"],
        ["hint"],
        ["dance"],
        ["use"],
        ["use", "item"],
        ["quit"],
    ]

    def fake_get_input() -> list[str]:
        return inputs.pop(0)

    monkeypatch.setattr(engine, "get_input", fake_get_input)

    engine.run()
    assert not engine.game_running


def test_engine_incorrect() -> None:
    """Simulate a short REPL run with real rooms and fake input."""
    # Bad Engine
    with pytest.raises(ValueError, match="No room dance_room exists\\."):
        Engine(
            debug=False,
            start_room="dance_room",
            transcript_loc="transcript.txt",
            data_path="data/",
        )
