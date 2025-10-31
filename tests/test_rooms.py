"""Tests for escape room game utility functions."""

import importlib
import pkgutil

import pytest

from escaperoom.rooms.base import Base, RoomInput, RoomOutput

ROOMS_PACKAGE = "src.escaperoom.rooms"
# Discover all modules under src.escaperoom.rooms
room_modules: list[str] = []
for _, name, _ in pkgutil.iter_modules([ROOMS_PACKAGE.replace(".", "/")]):
    if name != "base":
        room_modules.append(name)


def load_room(room_name: str) -> Base:
    """Dynamically load a room class."""
    module = importlib.import_module(f"{ROOMS_PACKAGE}.{room_name}")

    # Find a class that subclasses Base
    room_cls: Base | None = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Base) and obj is not Base:
            room_cls = obj
            break

    assert room_cls, f"No subclass of Base found in {room_name}"

    # Initialize room (inject dummy data path)
    if room_name == "intro":
        return room_cls()
    return room_cls("data/")

@pytest.mark.parametrize("room_name", room_modules)
def test_room_basic(room_name) -> None:  # noqa: ANN001
    """Test room basic commands."""
    room: Base = load_room(room_name)

    commands: dict[tuple[str], bool] = {
        ("fake_command",): False,
        ("hint",): True,
        ("look",): True,
    }

    # Run commands for the rooms
    for command_tup, expected_success in commands.items():
        command: list[str] = list(command_tup)
        output: RoomOutput = room.handle_command(RoomInput(command))
        assert output.success == expected_success, f"{command}"
        assert isinstance(output.message, str)


@pytest.mark.parametrize("room_name", room_modules)
def test_room_interaction(request, room_name) -> None:  # noqa: ANN001
    """Test room interaction commands."""
    room: Base = load_room(room_name)

    commands: dict[tuple[str], bool] = {
        ("inspect",): False,
        ("inspect", "fake_item"): False,
        ("inspect", "auth.log"): room_name == "soc",
        ("inspect", "dns.cfg"): room_name == "dns",
        ("inspect", "vault_dump.txt"): room_name == "vault",
        ("inspect", "proc_tree.jsonl"): room_name == "malware",
        ("use", "fake_item"): False,
        ("use", "gate"): room_name == "final",
    }

    # Run commands for the rooms
    for command_tup, expected_success in commands.items():
        command: list[str] = list(command_tup)

        # Expect fail of unimplemented inspect and use functions
        if command[0] in ("inspect", "use") and room_name in (
            # "soc",
            # "dns",
            # "vault",
            # "malware",
            "final",
        ):
            request.node.add_marker(
                pytest.mark.xfail(reason="Not yet implemented"),
            )

        output: RoomOutput = room.handle_command(RoomInput(command))
        assert output.success == expected_success, f"{command}"
        assert isinstance(output.message, str)
