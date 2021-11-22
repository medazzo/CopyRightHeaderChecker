import logging
import os
import re
import tempfile
from shutil import copyfile

from copyrightheader.header import Header

_logger = logging.getLogger(__name__)


class Conf:
    """Configuration class"""

    def __init__(
        self,
        update=True,
        forceOldHeader=True,
        nameCompany="",
        addressCompany="",
        countryCompany="",
        yearCompany="",
        inputFolder="",
    ):
        self.inputFolder = inputFolder
        self.yearCompany = yearCompany
        self.newCopyrightHeader = ""
        self.countryCompany = countryCompany
        self.addressCompany = addressCompany
        self.nameCompany = nameCompany
        self.updateFiles = update
        self.shebangCheck = True
        self.forceOldHeader = forceOldHeader
        self.warnOldHeader = True
        self.excludeDirs = [".git", ".repo"]
        self.shebangs = ["#!/", "#!/bin", "#!/usr/bin"]
        self.copyrightHeader = [
            " @author $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$",
            " ",
            " @copyright $$CompanyYear$$ $$CompanyName$$",
            " All rights exclusively reserved for $$CompanyName$$",
            " unless otherwise expressly agreed",
            " ",
        ]
        self.headersCheck = [
            {
                "brief": "C/C++ Code",
                "extensions": [".c", ".cpp", ".h", ".hpp", ".java", ".js"],
                "names": [],
                "startLine": "/**",
                "endLine": "*/",
            },
            {
                "brief": "bash/scripting Code",
                "extensions": [
                    ".conf",
                    ".conf.sample",
                    ".bb",
                    ".inc",
                    ".service",
                    ".sh",
                    ".cfg",
                    ".m4",
                    ".init",
                    ".py",
                    ".pl",
                    ".yml",
                    ".yaml",
                ],
                "names": [
                    "requirements.txt",
                    "CMakeLists.txt",
                    "init",
                    "run-ptest",
                    "llvm-config",
                    "build-env-set",
                    "init-build-env",
                    "setup-build-env",
                    "Dockerfile",
                ],
                "startLine": "#",
                "endLine": "",
            },
            {
                "brief": "html/xml Code",
                "extensions": [".html", ".xml"],
                "names": [],
                "startLine": "<!--",
                "endLine": "-->",
            },
            {
                "brief": "Markdown Code",
                "extensions": [".md"],
                "names": [],
                "startLine": "[comment]: <>",
                "endLine": ")",
            },
        ]
        self.headers = []
        for bhv in self.headersCheck:
            self.headers.append(
                Header(
                    brief=bhv["brief"],
                    extensions=bhv["extensions"],
                    filenames=bhv["names"],
                    copyright_header=self.copyrightHeader,
                    start_line=bhv["startLine"],
                    end_line=bhv["endLine"],
                )
            )

    def short_info(self):
        _logger.info("")
        _logger.info("----------------------------------------")
        _logger.info("* Files are updated    : %s", self.updateFiles)
        _logger.info("* Check Shebang        : %s", self.shebangCheck)
        _logger.info("* Warn on old Header   : %s", self.warnOldHeader)
        _logger.info("* force Old Header     : %s", self.forceOldHeader)
        _logger.info("* Excluded Folders     : %s", self.excludeDirs)
        _logger.info("* Shebang List         : %s", self.shebangs)
        _logger.info("----------------------------------------")
        _logger.info("* Company Name         : %s", self.nameCompany)
        _logger.info("* Company Year         : %s", self.yearCompany)
        _logger.info("* Company Address      : %s", self.addressCompany)
        _logger.info("* Company Country      : %s", self.countryCompany)
        _logger.info("----------------------------------------")
        _logger.info("")

    def info(self):
        self.short_info()
        for h in self.headers:
            h.info()

    def checkfileShebang(self, fileData):
        """return true if file has a shebang"""
        for she in self.shebangs:
            if fileData.startswith(she):
                return True
        return False

    def GenerateNewCopyright(self):
        """will get the new CopyrightHeader"""
        # apply company information
        copyright = self.copyrightHeader
        copyright = [
            w.replace("$$CompanyName$$", self.nameCompany) for w in copyright
        ]
        copyright = [
            w.replace("$$CompanyCountry$$", self.countryCompany)
            for w in copyright
        ]
        copyright = [
            w.replace("$$CompanyAddress$$", self.addressCompany)
            for w in copyright
        ]
        copyright = [
            w.replace("$$CompanyYear$$", self.yearCompany) for w in copyright
        ]
        # update header
        maxline = max(copyright, key=len)
        maxl = len(maxline) + 1
        for i, w in enumerate(copyright):
            offset = maxl - len(w)
            wf = " " * offset
            w = w + wf
            copyright[i] = w

        self.newCopyrightHeader = copyright

    def stripcomments(self, text):
        return re.sub("//.*?(\r\n?|\n)|/\\*.*?\\*/", "", text, flags=re.S)

    def ApplyCopyright(self, oldfile, newfile, header, forceNewHeader=False):
        newheader = self.newCopyrightHeader
        fd, tmpFilename = tempfile.mkstemp()
        line = ""
        try:
            with os.fdopen(fd, "w") as dst:
                with open(oldfile) as src:
                    data = src.readlines()
                    index = 0
                    hd = ""
                    if self.checkfileShebang(data[0]):
                        line = data[0]
                        index = 1
                    if forceNewHeader:
                        hd = self.stripcomments("".join(data[index:10]))
                    # construction
                    if line:
                        dst.write(line)
                        dst.write("\n")
                    for cop in newheader:
                        dst.write(header.startLine)
                        dst.write(cop)
                        dst.write(header.endLine)
                        dst.write("\n")
                    if forceNewHeader:
                        dst.write(hd)
                    else:
                        dst.write("".join(data[index:10]))
                    dst.write("".join(data[10:]))
                    dst.close()
                    src.close()
                    copyfile(tmpFilename, newfile)
        finally:
            os.remove(tmpFilename)
