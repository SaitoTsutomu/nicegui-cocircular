"""共円"""

from importlib.metadata import metadata

import fire

from .cocircular import run_game

_package_metadata = metadata(str(__package__))
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")

__all__ = ["__author__", "__version__"]


def main() -> None:
    """スクリプト実行"""
    fire.Fire(run_game)
