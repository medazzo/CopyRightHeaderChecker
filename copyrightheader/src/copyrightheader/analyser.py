import logging
import ntpath
import os
import time

from copyrightheader.header import Header

_logger = logging.getLogger(__name__)


class Analyser:
    """Header class"""

    def __init__(self, inputFolder, dryRun, conf):
        self.inputFolder = inputFolder
        self.dryRun = dryRun
        self.conf = conf
        self.oldNumberOfLines = 6
        self.filesAlreadyCopyright = []
        self.filesUnsupported = []
        if dryRun:
            self.outputfolder = "./tmp"
        else:
            self.outputfolder = self.inputFolder

    def process(self):
        """Process and start copyright header checks"""
        _logger.info("- - - - - - -  Analyse - - - - - - -")
        start = time.time()
        self.FindFiles()
        end = time.time()
        took = end - start
        _logger.info("- - - - - - -  Analyse - - took %.4f sec -", took)
        _logger.info("- - - - - - -  Process - - - - - - -")
        start = time.time()
        self.ApplyNewHeader()
        end = time.time()
        took = end - start
        _logger.info("- - - - - - -  Process - - took %.4f sec -", took)

    def ApplyNewHeader(self):
        """will apply new Copyright on array of files into OutDir with Same tree as original"""
        self.conf.GenerateNewCopyright()
        _logger.info("- -  we will use Header :")
        for w in self.conf.newCopyrightHeader:
            _logger.info(">%s<", w)
        _logger.info("- - ")
        filesUpdated = 0
        forceNewHeader = False
        for h in self.conf.headers:
            for x in h.filesManaged:
                forceNewHeader = False
                if self.dryRun:
                    p = os.path.dirname(x)
                    while p.startswith("../"):
                        p = p[3:]
                    if p.startswith("/"):
                        p = p[1:]
                    Ofolder = self.outputfolder + "/" + p
                    nfile = Ofolder + "/" + ntpath.basename(x)
                    # create dir file if not exist
                    nbase = os.path.dirname(nfile)
                    if not os.path.exists(nbase):
                        os.makedirs(nbase)
                else:
                    nfile = x
                if (
                    x in self.filesAlreadyCopyright
                    and self.conf.forceOldHeader
                ):
                    _logger.warn(
                        "- - => %s : Force removal of old Header !", format(x)
                    )
                    forceNewHeader = True
                self.conf.ApplyCopyright(x, nfile, h, forceNewHeader)
                filesUpdated = filesUpdated + 1
        _logger.info("  - - -	=> %s files are updated ", format(filesUpdated))

    def checkfileCopyright(self, filename):
        """return true if file has already a Copyright in first X lines"""
        infile = open(filename)
        for x in range(self.oldNumberOfLines):
            line = infile.readline()
            if "Copyright" in line or "copyright" in line:
                self.filesAlreadyCopyright.append(filename)
                return True
        return False

    def FindFiles(self):
        """Find all concerned files as defined up"""
        for root, dirs, files in os.walk(self.inputFolder):
            dirs[:] = [d for d in dirs if d not in self.conf.excludeDirs]
            for x in files:
                sfileN = os.path.join(root, x)
                #  check old copyright
                self.checkfileCopyright(sfileN)
                # find Headers
                found = False
                for h in self.conf.headers:
                    if h.findFile(sfileN):
                        found = True
                        break
                # not Headers suitable for this file
                if not found:
                    _logger.warn(
                        " ! ==> Cannot find Header for file --> %s",
                        format(sfileN),
                    )
                    self.filesUnsupported.append(sfileN)
        for h in self.conf.headers:
            _logger.info("   - %s   %s  files.", len(h.filesManaged), h.brief)
        _logger.info(
            "  - - -	! %s files are already with a Copyright Headers :",
            len(self.filesAlreadyCopyright),
        )
        for x in self.filesAlreadyCopyright:
            _logger.info("   - %s", x)
        _logger.info(
            "  - - -	! %s files are Unsupported :", len(self.filesUnsupported)
        )
        for x in self.filesUnsupported:
            _logger.info("   - %s", x)
