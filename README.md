# extreqs

Parse python requirements.txt files into setuptools extras.

`extreqs` is a build-time dependency used in projects with a `requirements.txt` and a `setup.py`,
where the `setup.py` reads the `requirements.txt` to determine the runtime dependencies.

## Do not use this package

`extreqs` was written in a simpler but much worse time for python packaging.
Historically, `setup.cfg` or `setup.py` was used to specify runtime dependencies.
Applications were supposed to use strict version constraints,
and libraries permissive version constraints.

For CI and development purposes,
it was convenient to use `requirements.txt` files to fix specific versions,
or to specify additional dependencies used at development time and not at runtime.

This meant manually syncing two files, which is a pain.
So the intended walls between the use of `requirements.txt` and `setup.py` started to break down, and a pattern emerged of parsing your single-source-of-truth `requirements.txt` to feed into your `setup.py`.

`extreqs` was developed to fill the need of describing ["extras"](https://stackoverflow.com/questions/52474931/what-is-extra-in-pypi-dependency) while still maintaining `requirements.txt` as your single source of truth.
`extreqs` was always intended primarily to support application development,
but could be used for library development as well as a bridge (or crutch?) for people who preferred using `requirements.txt` for specifying dependencies.

Today, various development tools, most notably [`uv`](https://docs.astral.sh/uv/), handle lock files for you based on the canonical `pyproject.toml` dependency list, which also handles extras and groups (for development dependencies).
Those tools, in particular `uv`, should be used instead.

This package is maintained for legacy purposes.

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
dep2  #extra: e1

#extra: e2
dep3

#extra: e3  # you can still have freeform comments!
dep4  #extra: e4 e5
dep5
```

would be parsed into

```python
install_requires = ["dep1"]
extras_require = {
    "e1": ["dep2"],
    "e2": ["dep3"],
    "e3": ["dep4", "dep5"],
    "e4": ["dep4"],
    "e5": ["dep4"],
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

## Development

Contributions are welcome, although any broadening of extreqs' scope is unlikely to be accepted - raise an issue first!

Releases are made like this

```sh
# commit all your changes, push, and ensure that CI passes
git add .
git commit -m "Prepare for a new version"
git push

# bump the version
uv version --bump minor

# commit the version bump
git add .
git commit -m "Bump to version $(uv version --short)"

# tag the commit
git tag -a "v$(uv version --short)" -m "New feature X"

# push to CI, which will do the releasing
git push --follow-tags
```
