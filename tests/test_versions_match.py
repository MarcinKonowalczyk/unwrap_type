import re
from collections.abc import Iterator

import pytest
from conftest import __project_root__
from packaging.version import Version

main_file = __project_root__ / "src" / "unwrap_type" / "unwrap_type.py"
other_file = __project_root__ / "src" / "unwrap_type" / "dataclass_to_sqlite.py"


def iter_lines(filename: str, encoding: str = "utf-8") -> Iterator[str]:
    """Yield lines from the file one-by-one"""
    with open(filename, encoding=encoding) as f:
        while line := f.readline():
            yield line


def get_version(filename: str) -> str:
    """Get the __version__ string from the file"""
    version_regex = r"^__version__ *= *(?P<quote>[\"'])(?P<version>[^'\"]*)(?P=quote)"
    for line in iter_lines(filename):
        if match := re.search(version_regex, line):
            return match.group("version")
    raise RuntimeError(f"Unable to find version in {filename}")


def test_versions_match() -> None:
    main_version = Version(get_version(str(main_file)))
    other_version = Version(get_version(str(other_file)))
    if main_version != other_version:
        pytest.fail(f"Versions do not match: {main_file}={main_version}, {other_file}={other_version}")
