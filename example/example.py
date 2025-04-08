import sqlite3
from dataclasses import Field, dataclass, is_dataclass
from dataclasses import fields as dataclass_fields
from pathlib import Path
from typing import Optional, Union

from unwrap_type import Type, unwrap_optional

################################################################################

SQL_TYPE_MAP: dict[Type, str] = {
    int: "INTEGER",
    str: "TEXT",
    float: "REAL",
}

DEFAULT_TABLE_NAME = "data"


def _parse_dataclass_field(field: Field) -> tuple[str, str, bool]:
    """Parse a row from the dataclass. This is used to convert the row to
    a SQLite type.
    """
    # Check if the field is optional
    is_optional = False
    ft = field.type
    sql_type = SQL_TYPE_MAP.get(ft)  # type: ignore
    if sql_type is None:
        is_optional = True  # if we get out of this without an error, it's optional
        if isinstance(ft, str):
            # This is a string, so we don't know what to do with it
            raise ValueError(f"Unsupported field type: {ft}")
        inner, err = unwrap_optional(ft)
        if not err:
            sql_type = SQL_TYPE_MAP.get(inner)
            if sql_type is None:
                raise ValueError(f"Unsupported field type: {ft}")
        else:
            # Not an Optional, so we don't know what to do with it
            raise ValueError(f"Unsupported field type: {ft}")

    return field.name, sql_type, is_optional


def _dataclass_fields_to_sqlite_create(
    record_cls: object,
    *,
    fields: Optional[list[Field]] = None,
    primary_key: Optional[str] = None,
    table_name: str = DEFAULT_TABLE_NAME,
) -> str:
    """Convert a list of fields to a SQLite table definition."""

    if not is_dataclass(record_cls):
        raise TypeError("record_cls is not a dataclass")

    if fields is None:
        fields = list(dataclass_fields(record_cls))

    cmd = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    for field in fields:
        name, type, optional = _parse_dataclass_field(field)
        print(f"Field: {name}, Type: {type}, Optional: {optional}")
        cmd += f"{name} {type}"
        cmd += " NOT NULL" if not optional else ""
        cmd += ", "
    cmd = cmd.rstrip(", ")
    if primary_key:
        cmd += f", PRIMARY KEY ({primary_key})"
    cmd += ");"

    return cmd


def init_sqlite(record_cls: object, db_name: Union[str, Path], table_name: str = DEFAULT_TABLE_NAME) -> None:
    """Initialize a SQLite database. The database is created in the current
    directory.
    """

    cmd_drop = f"DROP TABLE IF EXISTS {table_name};"
    cmd_create = _dataclass_fields_to_sqlite_create(
        record_cls=record_cls,
        primary_key="id",
        table_name=table_name,
    )

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(cmd_drop)
        cursor.execute(cmd_create)
        conn.commit()


def _record_to_sqlite(
    record: object,
    *,
    table_name: str = DEFAULT_TABLE_NAME,
) -> str:
    """Convert a DataRow to a SQLite insert command."""
    if not is_dataclass(record):
        raise TypeError("record is not a dataclass")

    fields = dataclass_fields(record)

    cmd = f"INSERT INTO {table_name} ({', '.join(field.name for field in fields)}) VALUES ("

    for field in fields:
        value = getattr(record, field.name)
        if value is None:
            cmd += "NULL, "
            continue
        if isinstance(value, str):
            value = value.replace("'", "''")
        cmd += f"'{value}', "
    cmd = cmd.rstrip(", ")
    cmd += ");"

    return cmd


def dump_to_sqlite(
    db_name: Union[str, Path],
    records: list[object],
    *,
    table_name: str = DEFAULT_TABLE_NAME,
) -> None:
    """Dump the response to a SQLite database."""

    if not records:
        # dont even try to connect if we have no records
        return

    cmds = [_record_to_sqlite(record, table_name=table_name) for record in records]

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for cmd in cmds:
            cursor.execute(cmd)
        conn.commit()


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

    __this_dir__ = Path(__file__).parent

    init_sqlite(Record, __this_dir__ / "example.db")
    dump_to_sqlite(__this_dir__ / "example.db", records)

    # Print the records from the database
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
