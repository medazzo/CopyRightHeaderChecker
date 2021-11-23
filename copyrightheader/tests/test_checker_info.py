import pytest
import logging
from copyrightheader.checker import main

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"

LOGGER = logging.getLogger(__name__)

def test_info_verbose_short(caplog):    
    with caplog.at_level(logging.INFO):
        main(["info", "-d", "short"])
    assert "Printing some informations .." not in caplog.text    
    
    with caplog.at_level(logging.DEBUG):
        main(["info", "-v", "-d", "short"])
    assert "Printing some informations .." in caplog.text

def test_info_verbose_all(caplog):
    with caplog.at_level(logging.INFO):
        main(["info", "-d", "all"])
    assert "Printing some informations .." not in caplog.text    
    
    with caplog.at_level(logging.DEBUG):
        main(["info", "-v", "-d", "all"])
    assert "Printing some informations .." in caplog.text
    "Starting Working on folder"



def test_info_short(caplog):
    LOGGER.info('Testing now.')
    with caplog.at_level(logging.DEBUG):
        main(["info", "-d", "short"])
    assert "Files are updated    : True" in caplog.text
    assert "Check Shebang        : True" in caplog.text
    assert "Warn on old Header   : True" in caplog.text
    assert "force Old Header     : True" in caplog.text
    assert "Excluded Folders     : ['.git', '.repo']" in caplog.text
    assert (
        "Shebang List         : ['#!/', '#!/bin', '#!/usr/bin']"
        in caplog.text
    )
    assert "Company Name         :" in caplog.text
    assert "Company Year         :" in caplog.text
    assert "Company Address      :" in caplog.text
    assert "Company Country      :" in caplog.text


def test_info_all(caplog):
    with caplog.at_level(logging.DEBUG):
        main(["info", "-d", "all"])
    assert "Files are updated    : True" in caplog.text
    assert "Check Shebang        : True" in caplog.text
    assert "Warn on old Header   : True" in caplog.text
    assert "Header brief" in caplog.text
    assert "Header extensions" in caplog.text
    assert "Header fileNames" in caplog.text
    assert "Header startLine" in caplog.text
    assert "Header endLine" in caplog.text
