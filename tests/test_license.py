from pathlib import Path
from typing import Union

from conftest import __project_root__

license_file = __project_root__ / "LICENSE.txt"
main_file = __project_root__ / "src" / "unwrap_type" / "unwrap_type.py"
other_file = __project_root__ / "src" / "unwrap_type" / "dataclass_to_sqlite.py"


def include_test(a: Union[str, Path], b: Union[str, Path]) -> bool:
    """Check if content of file a is included in file b."""
    with open(a) as f:
        a_text = f.read()

    with open(b) as f:
        b_text = f.read()

    return a_text in b_text


def test_license() -> None:
    assert license_file.exists(), f"License file {license_file} not found."
    assert main_file.exists(), f"Source file {main_file} not found."

    # Make sure the license is included in the source file verbatim
    assert include_test(license_file, main_file), "License not found in source file."


def test_license_other() -> None:
    assert license_file.exists(), f"License file {license_file} not found."
    assert other_file.exists(), f"Source file {other_file} not found."

    # Make sure the license is included in the source file verbatim
    assert include_test(license_file, other_file), "License not found in source file."
