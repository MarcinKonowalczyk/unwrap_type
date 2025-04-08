"""
Convert a dataclass to a SQLite table. This is an optional extension to the
single-file module `unwrap_type`. It is not required for the main functionality
of the module, but it is a common use case, so it might as well be set up
such that its easy to also grab and use.

Written by Marcin Konowalczyk.
"""

import sqlite3
from dataclasses import Field, dataclass, is_dataclass
from dataclasses import fields as dataclass_fields
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional

try:
    from .unwrap_type import Type, unwrap_optional
except ImportError as ie:
    for fallback in [
        "from unwrap_type import Type, unwrap_optional",
        "from _unwrap_type import Type, unwrap_optional",
        "from ._unwrap_type import Type, unwrap_optional",
    ]:
        try:
            exec(fallback)
            break
        except ImportError:
            pass
    else:
        raise ie

__version__ = "0.1.2"

__all__ = [
    "TYPE_MAP",
    "create",
    "insert",
    "parse_dataclass_field",
]


TYPE_MAP: dict[Type, str] = {
    int: "INTEGER",
    str: "TEXT",
    float: "REAL",
    Decimal: "NUMERIC",
    datetime: "DATETIME",
}

DEFAULT_TABLE_NAME = "data"


def parse_dataclass_field(
    field: Field,
    type_map: Optional[dict[Type, str]] = None,
) -> tuple[str, str, bool]:
    """Parse a row from the dataclass. This is used to convert the row to
    a SQLite type.
    """

    if type_map is None:
        type_map = TYPE_MAP

    is_optional = False
    ft = field.type
    sql_type = type_map.get(ft)  # type: ignore
    if sql_type is None:
        is_optional = True  # if we get out of this without an error, it's optional
        if isinstance(ft, str):
            # This is a string, so we don't know what to do with it
            raise ValueError(f"Unsupported field type: {ft}")
        inner, err = unwrap_optional(ft)
        if not err:
            sql_type = TYPE_MAP.get(inner)
            if sql_type is None:
                raise ValueError(f"Unsupported field type: {ft}")
        else:
            # Not an Optional, so we don't know what to do with it
            raise ValueError(f"Unsupported field type: {ft}")

    return field.name, sql_type, is_optional


def create(
    record_cls: object,
    *,
    primary_key: Optional[str] = None,
    type_map: Optional[dict[Type, str]] = None,
) -> str:
    """Create an SQlite table 'CREATE' command from a dataclass."""

    if not is_dataclass(record_cls):
        raise TypeError("record_cls is not a dataclass")

    fields = list(dataclass_fields(record_cls))

    headers = []
    for field in fields:
        name, sql_type, is_optional = parse_dataclass_field(field, type_map=type_map)
        header = f"{name} {sql_type}"
        if not is_optional:
            header += " NOT NULL"
        headers.append(header)
    if primary_key:
        headers.append(f"PRIMARY KEY ({primary_key})")

    return f"CREATE TABLE IF NOT EXISTS {{table_name}} ({', '.join(headers)})"


def insert(record: object) -> str:
    """Create a SQLite 'INSERT' command from an *instance* of a dataclass.
    The table name is set to `{table_name}` and must be set separately. For
    example: `insert(record).format(table_name="data")`.
    """
    if not is_dataclass(record):
        raise TypeError("record is not a dataclass")

    if isinstance(record, type):
        raise TypeError("record is a class, not an instance")

    fields = dataclass_fields(record)

    names = (field.name for field in fields)

    values = []
    for field in fields:
        value = getattr(record, field.name)
        if value is None:
            value = "NULL"
        else:
            if isinstance(value, str):
                value = value.replace("'", "''")
            value = f"'{value}'"
        values.append(value)

    return f"INSERT INTO {{table_name}} ({', '.join(names)}) VALUES ({', '.join(values)});"


################################################################################

if __name__ == "__main__":

    @dataclass
    class Record:
        """Some kind of data record"""

        id: int
        a: int
        b: str
        c: Optional[float] = None

    records: list[object] = [
        Record(id=1, a=1, b="foo"),
        Record(id=2, a=2, b="bar", c=3.14),
    ]

    __file_dir__ = Path(__file__).parent
    __project_root__ = __file_dir__.parent.parent

    db = __project_root__ / "example.db"

    # create the database
    cmd_drop = "DROP TABLE IF EXISTS data;"
    cmd_create = create(
        record_cls=Record,
        primary_key="id",
    ).format(table_name="data")

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(cmd_drop)
        cursor.execute(cmd_create)
        conn.commit()

    # dump data
    cmds = [insert(record).format(table_name="data") for record in records]

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        for cmd in cmds:
            cursor.execute(cmd)
        conn.commit()

    # read data
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

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
