import logging
import os

_logger = logging.getLogger(__name__)
_logger.propagate = True

class Header:
    """Header class"""

    def __init__(
        self,
        brief,
        extensions,
        filenames,
        copyright_header,
        start_line,
        end_line,
    ):
        self.brief = brief
        self.extensions = extensions
        self.fileNames = filenames
        self.copyrightHeader = copyright_header
        self.startLine = start_line
        self.endLine = end_line
        self.filesManaged = []

    def info(self):
        _logger.info("")
        _logger.info("----------------------------------------")
        _logger.info("* Header brief           : %s", self.brief)
        _logger.info("* Header extensions      : %s", self.extensions)
        _logger.info("* Header fileNames       : %s", self.fileNames)
        _logger.info("* Header startLine       : %s", self.startLine)
        _logger.info("* Header endLine         : %s", self.endLine)

    def findFile(self, filename):
        """return True if filename will be managed with this header"""
        # Check if file is in names
        head, tail = os.path.split(filename)
        _logger.debug("  - - -	=> %s / %s", head, tail)
        if tail in self.fileNames:
            self.filesManaged.append(filename)
            return True
        for ext in self.extensions:
            if filename.endswith(ext):
                self.filesManaged.append(filename)
                return True
        return False
