from typing import Optional

from unwrap_type import unwrap_optional


def test_unwrap_optional() -> None:
    t = Optional[int]
    assert unwrap_optional(t) == (True, int)
