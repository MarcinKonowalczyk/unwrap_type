"""
Single-file module with for unwrapping Union and Optional types in Python.

This is a single-file module. It does not depend on any other files or external packages.
Its version is tracked internally in a separate repository. It can be used as a package,
or the file can be copied into a project and used directly. In the latter case, any
bugs/updates ought to be copied back to the original repository.

Written by Marcin Konowalczyk.
"""

__version__ = "0.1.1"

__all__ = [
    "Type",
    "unwrap_optional",
    "unwrap_union",
]

from typing import TypeVar, Union, _SpecialForm

try:
    from types import UnionType as _union_type  # type: ignore[attr-defined, unused-ignore]
except ImportError:
    _union_type = type(Union)  # type: ignore[misc, assignment, unused-ignore]

_none_type = type(None)

Type = Union[type, _SpecialForm]
Err = Union[str, None]
_T = TypeVar("_T")
Result = tuple[_T, Err]


def _get_args(type_: Type) -> Result[tuple[Type, ...]]:
    if hasattr(type_, "__args__"):
        return tuple(type_.__args__), None
    else:
        return (), "No __args__ attribute on type"


_NOT_A_UNION_TYPE = "Not a union type"


def unwrap_union(type_: Type) -> Result[tuple[Type, ...]]:
    """Unwrap a Union type and return a list of types."""
    if hasattr(type_, "__origin__"):
        # Python 3.8+
        if type_.__origin__ is Union:
            return _get_args(type_)
        else:
            return (), f"Unknown origin type: {type_.__origin__}"
    elif isinstance(type_, _union_type):
        # Python 3.10+
        if type_.__class__ is _union_type:
            return _get_args(type_)
        else:
            return (), f"Unknown union type: {type_}"
    else:
        return (), _NOT_A_UNION_TYPE + f": {type_}"


def unwrap_optional(type_: Type) -> Result[Type]:
    """Unwrap an Optional type and return the type inside it."""

    types, err = unwrap_union(type_)
    if err:
        if _NOT_A_UNION_TYPE in err and type_ is _none_type:
            # Special case for None type.
            # Optional[None] is a valid type and is its own optional
            return type_, None
        return type_, err
    if len(types) == 2:
        # Optional is implemented as Union[X, NoneType]
        for arg in types:
            if arg is not _none_type:
                return arg, None
    return type_, "Not an optional type"


__license__ = """
Copyright 2025 Marcin Konowalczyk

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
