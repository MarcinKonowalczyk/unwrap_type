from typing import Optional

from unwrap_type import unwrap_optional


def test_unwrap_optional() -> None:
    t = Optional[int]
    unwrapped, err = unwrap_optional(t)
    assert not err
    assert unwrapped is int


def test_unwrap_optional_none() -> None:
    t = Optional[None]
    unwrapped, err = unwrap_optional(t)
    assert not err
    assert unwrapped is type(None)


def test_unwrap_optional_of_optional() -> None:
    t = Optional[Optional[int]]
    unwrapped, err = unwrap_optional(t)
    assert not err
    assert unwrapped is int
