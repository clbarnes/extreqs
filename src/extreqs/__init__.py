"""
# extreqs package
"""

from importlib.metadata import version as _version

from .main import parse_requirement_files, parse_requirement_files_dict

__version__ = _version("extreqs")

__all__ = ["parse_requirement_files", "parse_requirement_files_dict"]
