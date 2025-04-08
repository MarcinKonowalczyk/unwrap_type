from typing import Union

from unwrap_type import unwrap_union


def roughly_match(pattern: str, string: str, case_sensitive: bool = False) -> bool:
    """Check if the given pattern appears in the string."""
    if not case_sensitive:
        pattern = pattern.lower()
        string = string.lower()
    return pattern in string


def test_unwrap_union_shallow() -> None:
    t = Union[int, str]
    unwrapped, err = unwrap_union(t)
    assert not err
    assert unwrapped == (int, str)


def test_unwrap_union_nested() -> None:
    t = Union[int, Union[str, float]]
    unwrapped, err = unwrap_union(t)
    assert not err
    assert unwrapped == (int, str, float)


def test_unwrap_union_nested_with_none() -> None:
    t = Union[int, Union[str, None]]
    unwrapped, err = unwrap_union(t)
    assert not err
    assert unwrapped == (int, str, type(None))


def test_unwrap_not_a_union() -> None:
    t = int
    unwrapped, err = unwrap_union(t)
    assert isinstance(err, str) and roughly_match("not a union", err)
    assert len(unwrapped) == 0
