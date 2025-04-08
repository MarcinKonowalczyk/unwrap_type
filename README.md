# unwrap_type

![GitHub Tag](https://img.shields.io/github/v/tag/MarcinKonowalczyk/unwrap_type?label=version)
[![Single file](https://img.shields.io/badge/single%20file%20-%20purple)](https://raw.githubusercontent.com/MarcinKonowalczyk/unwrap_type/main/src/unwrap_type/unwrap_type.py)
[![test](https://github.com/MarcinKonowalczyk/unwrap_type/actions/workflows/test.yml/badge.svg)](https://github.com/MarcinKonowalczyk/unwrap_type/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Python versions](https://img.shields.io/badge/python-3.9%20~%203.13-blue)

Single-file module with for unwrapping Union and Optional types into their underlying types.

An example use-case is when trying to automatically convert dataclasses to sqlite statements. See `dataclass_to_sqlite.py` for such an example.

### Install

Just copy the single-module file to your project and import it.

```bash
cp ./src/unwrap_type/unwrap_type.py src/your_package/_unwrap_type.py
```

Or even better, without checking out the repository:

```bash
curl https://raw.githubusercontent.com/MarcinKonowalczyk/unwrap_type/main/src/unwrap_type/unwrap_type.py > src/your_package/_unwrap_type.py
```

Note that like this *you take ownership of the code* and you are responsible for keeping it up-to-date. If you change it that's fine (keep the license pls). That's the point here. You can also copy the code to your project and modify it as you wish.

If you want you can also build and install it as a package, but then the source lives somewhere else. That might be what you want though. 🤷‍♀️

```bash
pip install flit
flit build
ls dist/*
pip install dist/*.whl
```
