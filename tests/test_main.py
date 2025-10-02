"""Tests for escape room game."""

import pytest

from escape import square, square_wrong


def test_square() -> None:
    """Test correct square function."""
    integer = 5
    assert square(integer) == 25
    assert square(1) == 1
    assert square(-5) == 25
    assert square(0) != "hello"

@pytest.mark.xfail(reason="Not yet implemented")
def test_square_wrong() -> None:
    """Test incorrect square function."""
    assert square_wrong(5) == 25
    assert square_wrong(1) == 1
    assert square_wrong(-5) == 25

@pytest.mark.xfail(reason="Not yet implemented")
def test_square_wrong_2() -> None:
    """Test incorrect square function."""
    assert square_wrong(2) == 4
