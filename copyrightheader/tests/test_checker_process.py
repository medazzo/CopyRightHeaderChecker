import pytest
import logging
from copyrightheader.checker import main

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"

LOGGER = logging.getLogger(__name__)
options =  [
            "process",
            "-n",
            "NAMECOMPANY",
            "-a",
            "ADDRESSCOMPANY",
            "-c",
            "COUNTRYCOMPANY",
            "-y",
            "YEARCOMPANY",
            "-i",
            "./tests/data",
        ]
options_update = [
            "process",
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
            "./tests/data",
        ]
def test_process_verbose(caplog):    
    with caplog.at_level(logging.INFO):
        main(options)
    assert "Starting Working on folder" not in caplog.text    
    
    with caplog.at_level(logging.DEBUG):
        main(options)
    assert "Starting Working on folder" in caplog.text

def test_process_dryrun(caplog):
    with caplog.at_level(logging.DEBUG):
        main(options)
    assert "* Company Name         : NAMECOMPANY" in caplog.text
    assert "* Company Year         : YEARCOMPANY" in caplog.text
    assert "* Company Address      : ADDRESSCOMPANY" in caplog.text
    assert "* Company Country      : COUNTRYCOMPANY" in caplog.text

def test_process_update(caplog):
    with caplog.at_level(logging.DEBUG):
        main(options_update)
    assert "* Company Name         : NAMECOMPANY" in caplog.text
    assert "* Company Year         : YEARCOMPANY" in caplog.text
    assert "* Company Address      : ADDRESSCOMPANY" in caplog.text
    assert "* Company Country      : COUNTRYCOMPANY" in caplog.text
