"""Tests for escape room game."""

from escaperoom.utils import print_log


def test_print_log(monkeypatch, capsys, tmp_path) -> None:  # noqa: ANN001
    """Test printing and logging utils."""
    # Create a fake directory
    fake_path = tmp_path
    monkeypatch.chdir(fake_path)

    # Run the function
    print_log("Hello, Test!\n")

    # Check the print statement
    captured = capsys.readouterr()
    assert captured.out == "Hello, Test!\n"

    # Check the logging function
    log_path = fake_path / "log.log"
    assert log_path.exists()
    assert log_path.read_text() == "Hello, Test!\n"
