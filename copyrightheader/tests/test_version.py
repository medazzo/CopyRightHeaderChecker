import pytest

from copyrightheader._version import version

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"


def test_version():
    """CLI Tests"""
    assert "0.0.1" in version
