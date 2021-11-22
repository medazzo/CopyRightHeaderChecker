import pytest

from copyrightheader.checker import main

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"


def test_info_short(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["info", "-d", "short"])
    captured = capsys.readouterr()
    assert "Files are updated    :  True" in captured.out
    assert "Check Shebang        :  True" in captured.out
    assert "Warn on old Header   :  True" in captured.out
    assert "force Old Header     :  True" in captured.out
    assert "Excluded Folders     :  ['.git', '.repo']" in captured.out
    assert (
        "Shebang List         :  ['#!/', '#!/bin', '#!/usr/bin']"
        in captured.out
    )
    assert "Company Name         :" in captured.out
    assert "Company Year         :" in captured.out
    assert "Company Address      :" in captured.out
    assert "Company Country      :" in captured.out


def test_info_all(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["info", "-d", "all"])
    captured = capsys.readouterr()
    assert "Files are updated    :  True" in captured.out
    assert "Check Shebang        :  True" in captured.out
    assert "Warn on old Header   :  True" in captured.out
    assert "Header brief" in captured.out
    assert "Header extensions" in captured.out
    assert "Header fileNames" in captured.out
    assert "Header startLine" in captured.out
    assert "Header endLine" in captured.out


def test_process(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(
        [
            "process",
            "-r",
            "-n",
            "NAMECOMPANY",
            "-a",
            "ADDRESSCOMPANY",
            "-c",
            "COUNTRYCOMPANY",
            "-y",
            "YEARCOMPANY",
            "-i",
            "tests/data",
        ]
    )
    captured = capsys.readouterr()
    assert "* Company Name         :  NAMECOMPANY" in captured.out
    assert "* Company Year         :  YEARCOMPANY" in captured.out
    assert "* Company Address      :  ADDRESSCOMPANY" in captured.out
    assert "* Company Country      :  COUNTRYCOMPANY" in captured.out


def test_process_update(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(
        [
            "process",
            "-r",
            "-u",
            "-n",
            "NAMECOMPANY",
            "-a",
            "ADDRESSCOMPANY",
            "-c",
            "COUNTRYCOMPANY",
            "-y",
            "YEARCOMPANY",
            "-i",
            "tests/data",
        ]
    )
    captured = capsys.readouterr()
    assert "* Company Name         :  NAMECOMPANY" in captured.out
    assert "* Company Year         :  YEARCOMPANY" in captured.out
    assert "* Company Address      :  ADDRESSCOMPANY" in captured.out
    assert "* Company Country      :  COUNTRYCOMPANY" in captured.out
