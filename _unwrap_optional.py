"""
Single-file module with for unwrapping Optional types in Python.

This is a single-file module. It does not depend on any other files or external packages.
Its version is tracked internally in a separate repository. It can be used as a package,
or the file can be copied into a project and used directly. In the latter case, any
bugs/updates ought to be copied back to the original repository.

Written by Marcin Konowalczyk.
"""

__version__ = "0.0.1"

from typing import Optional, Union

try:
    from types import UnionType as _union_type  # type: ignore[attr-defined, unused-ignore]
except ImportError:
    _union_type = type(Union)  # type: ignore[misc, assignment, unused-ignore]


def unwrap_optional(type_: type) -> tuple[bool, type]:
    def get_other_from_args(type_: type) -> type:
        """Get the other type from a Union type."""
        if hasattr(type_, "__args__"):
            for arg in type_.__args__:
                if arg is not type(None):
                    return arg  # type: ignore
        return type(None)

    if hasattr(type_, "__origin__"):
        # Python 3.8+
        if type_.__origin__ is Union:
            return True, get_other_from_args(type_)
        elif type_.__origin__ is Optional:
            # Optional is implemented as Union[X, NoneType]
            raise NotImplementedError("Optional is not supported")
        else:
            raise NotImplementedError(f"Unknown origin type: {type_.__origin__}")
    elif isinstance(type_, _union_type):
        # Python 3.10+
        if type_.__class__ is _union_type:
            return True, get_other_from_args(type_)
        else:
            raise NotImplementedError(f"Unknown union type: {type_}")

    return False, type_
