"""
Single-file module with for unwrapping Optional types in Python.

This is a single-file module. It does not depend on any other files or external packages.
Its version is tracked internally in a separate repository. It can be used as a package,
or the file can be copied into a project and used directly. In the latter case, any
bugs/updates ought to be copied back to the original repository.

Written by Marcin Konowalczyk.
"""

__version__ = "0.0.2"

__all__ = [
    "unwrap_optional",
]

from typing import Optional, Union

try:
    from types import UnionType as _union_type  # type: ignore[attr-defined, unused-ignore]
except ImportError:
    _union_type = type(Union)  # type: ignore[misc, assignment, unused-ignore]

from typing import _SpecialForm

Type = Union[type, _SpecialForm]


def unwrap_optional(type_: Type) -> tuple[bool, Type]:
    def get_other_from_args(type_: Union[type, _SpecialForm]) -> type:
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
