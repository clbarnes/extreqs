"""
# extreqs package
"""
from .main import parse_requirement_files
from .version import version as __version__  # noqa: F401
from .version import version_tuple as __version_info__  # noqa: F401

__all__ = ["parse_requirement_files"]
