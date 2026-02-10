"""
# extreqs package
"""

from .main import parse_requirement_files, parse_requirement_files_dict
from importlib.metadata import version as _version

__version__ = _version("extreqs")

__all__ = ["parse_requirement_files", "parse_requirement_files_dict"]
