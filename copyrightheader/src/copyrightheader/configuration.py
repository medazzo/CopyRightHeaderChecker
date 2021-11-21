import os
from shutil import copyfile

from copyrightheader.header import Header


class Conf:
    """Configuration class"""

    def __init__(
        self,
        report=True,
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
        self.reporting = report
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
        print("")
        print("----------------------------------------")
        print("* Reporting is enabled : ", self.reporting)
        print("* Files are updated    : ", self.updateFiles)
        print("* Check Shebang        : ", self.shebangCheck)
        print("* Warn on old Header   : ", self.warnOldHeader)
        print("* force Old Header     : ", self.forceOldHeader)
        print("* Excluded Folders     : ", self.excludeDirs)
        print("* Shebang List         : ", self.shebangs)
        print("----------------------------------------")
        print("* Company Name         : ", self.nameCompany)
        print("* Company Year         : ", self.yearCompany)
        print("* Company Address      : ", self.addressCompany)
        print("* Company Country      : ", self.countryCompany)
        print("----------------------------------------")
        print("")

    def info(self):
        self.short_info()
        for h in self.headers:
            h.info()

    def checkfileShebang(self, filename):
        """return true if file has a shebang"""
        infile = open(filename)
        firstLine = infile.readline()
        infile.close()
        for she in self.shebangs:
            if firstLine.startswith(she):
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

    def ApplyCopyright(self, oldfile, newfile, header):
        dst = open(newfile, "w")
        isSheb = self.checkfileShebang(oldfile)
        src = open(oldfile)
        newheader = self.newCopyrightHeader
        if isSheb:
            line = src.readline()
            dst.write(line)
            for cop in newheader:
                dst.write(header.startLine)
                dst.write(cop)
                dst.write(header.endLine)
                dst.write("\n")
            # continue copy src file
            while line:
                line = src.readline()
                dst.write(line)
        else:
            for cop in newheader:
                dst.write(header.startLine)
                dst.write(cop)
                dst.write(header.endLine)
                dst.write("\n")
            dst.write(src.read())

        dst.close()
        src.close()
