import pytest

from copyrightheader.VERSION import __version__

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"


def test_version():
    """CLI Tests"""
    assert __version__ == "0.0.1"
