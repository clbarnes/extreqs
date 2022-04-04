import logging
import typing as tp
from collections import defaultdict
from pathlib import Path

import pkg_resources

logger = logging.getLogger(__name__)


def str_as_list(s: tp.Optional[tp.Union[str, tp.List[str]]]) -> tp.List[str]:
    if s is None:
        return []
    if isinstance(s, str):
        return [s]
    return s


class Parser:
    def __init__(self, fpath, file_context=None) -> None:
        self.file_context = str_as_list(file_context)
        self.block_context: tp.List[str] = []
        self.fpath = fpath
        self.line_num = -1

    def _context(self, line_context=None):
        out = []
        out.extend(self.file_context)
        out.extend(self.block_context)
        out.extend(str_as_list(line_context))
        return out

    def _parse_extra_spec(self, s):
        return s.split("#")[0].strip().split()

    def _parse_line(self, line):
        line = line.strip()

        if not line:
            return None

        req, *extra_specs = line.split("#extra:")
        req = req.strip()
        if req.startswith("#"):
            return None

        if len(extra_specs) > 1:
            logger.warning(
                "Multiple extra specs found; ignoring all but the first %s:%s",
                self.fpath,
                self.line_num,
            )
        if not extra_specs:
            line_spec = []
        else:
            line_spec = self._parse_extra_spec(extra_specs[0])

        if req:
            return req, self._context(line_spec)
        else:
            self.block_context = line_spec
            return None

    def parse(self):
        install_requires = []
        extras_require = defaultdict(list)

        with open(self.fpath) as f:
            for line in f:
                self.line_num += 1

                result = self._parse_line(line)
                if result is None:
                    continue

                req, context = result

                if not is_valid_req(req):
                    raise ValueError(
                        "'{req}' is not a valid requirement string "
                        f"{self.fpath}:{self.line_num}"
                    )

                if not context:
                    install_requires.append(req)
                else:
                    for ctx in context:
                        extras_require[ctx].append(req)

        return install_requires, extras_require


def merge_install_extras(*install_extras):
    install = []
    extras = defaultdict(list)
    for install2, extras2 in install_extras:
        install.extend(install2)
        for k, v in extras2.items():
            extras[k].extend(v)
    return install, dict(extras)


def parse_requirement_files(
    *req_files: Path,
    **extra_req_files: Path,
) -> tp.Tuple[tp.List[str], tp.Dict[str, tp.List[str]]]:
    """Parse requirements files into setuptools requirements.

    Requirements files whose listed dependencies all belong to
    a particular extra should be passed as keyword arguments,
    `extra_name="path/to/requirements.txt"`.

    Returns
    -------
    tuple[list[str], dict[str, list[str]]]
        List and dict to be passed to `setuptools.setup`'s
        `install_requires` and `extras_require` arguments
        respectively.
    """
    to_merge = [Parser(fpath).parse() for fpath in req_files]
    to_merge.extend(
        Parser(fpath, extra).parse() for extra, fpath in extra_req_files.items()
    )
    return merge_install_extras(*to_merge)


def is_valid_req(req):
    try:
        reqs = list(pkg_resources.parse_requirements(req))
        if len(reqs) != 1:
            return False
    except Exception:
        return False
    return True
