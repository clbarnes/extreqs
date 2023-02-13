# extreqs

Parse python requirements.txt files into setuptools extras.

## Usage

`extreqs` looks for special comments (`#extra:`) in your requirements files.
Note the lack of space after the `#`!
Anything which follows that (until the end of line, or another `#`) is treated as a whitespace-separated list of extras.
For example, `#extra: dev test doc` marks dependencies belonging to the `dev`, `test`, and `doc` extras.

If the `#extra:` comment is on the same line as (following) a dependency, then just that dependency belongs to that extra.
If the `#extra:` comment is on a line on its own, all dependencies below it belong to that extra, until the next `#extra:` line.

For example:

```txt
# requirements.txt
dep1
dep2  #extra: extra1

#extra: extra2
dep3

#extra: extra3  # you can still have freeform comments!
dep4  #extra: extra4 extra5
dep5
```

would be parsed into

```python
install_requires = ["dep1"]
extras_require = {
    "extra1": ["dep2"],
    "extra2": ["dep3"],
    "extra3": ["dep4", "dep5"],
    "extra4": ["dep4"],
    "extra5": ["dep4"],
}
```

Additionally, entire files can belong to a particular extra.

Note that python extras are not smart enough to deal with dependencies which belong only to _combinations_ of extras, or _negative_ extras: a dependency which belongs to multiple extras (given by the context of the file, block, or line) just belongs to multiple extras.
This is a limitation of python packaging and cannot be addressed here.

In your `setup.py`:

```python
#!/usr/bin/env python3
"""setup.py"""
from pathlib import Path

from extreqs import parse_requirements_files_dict
from setuptools import setup

here = Path(__file__).resolve().parent

req_kwargs = parse_requirements_files_dict(
    # files without an extra context are in *args
    here / "requirements.txt",
    # files with an extra context are in **kwargs
    optional=here / "requirements-optional.txt",
)

setup(
    name="my_package",
    ...
    **req_kwargs,
    ...
)
```

`extreqs` is an install-time dependency, and so must be added to your `pyproject.toml`:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools", "extreqs"]
build-backend = "setuptools.build_meta"
```

Look out for dependency specifiers which are accepted by pip, but not by setuptools (e.g. editable install `-e` or references to other requirement files `-r`).

## Notes

This package should only be used in certain circumstances, and may lead to bad habits if over-used.
Requirements files are intended for specifying reproducible (i.e. hard version constraints), maximal environments for other developers, CI, and so on to be able to run all tests, features, lints etc..
Package dependencies are intended to specify the minimal dependencies with permissive version constraints for users to install the package for use.

This package is, therefore, more applicable to distributing applications (CLI, web backends, etc.) than it is libraries.
