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
        self.oldNumberOfLines = 6
        self.filesAlreadyCopyright = []
        self.copyrightHeader = [
            " @author $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$",
            " ",
            " @copyright $$CompanyYear$$ $$CompanyName$$",
            " All rights exclusively reserved for $$CompanyName$$,",
            " unless otherwise expressly agreed",
            "",
        ]
        self.headersCheck = [
            {
                "brief": "C/C++ Code",
                "extensions": [".c", ".cpp", ".h", ".hpp"],
                "names": [],
                "startLine": "///",
                "endLine": "",
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
                ],
                "names": [
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
                "brief": "html/js Code",
                "extensions": [".html"],
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

    def checkfileCopyright(self, filename):
        """return true if file has already a Copyright in first X lines"""
        infile = open(filename)
        for x in xrange(self.oldNumberOfLines):
            line = infile.readline()
            if "Copyright" in line or "copyright" in line:
                self.filesAlreadyCopyright.append(filename)
                return True
        return False

    def checkfileShebang(self, filename):
        """return true if file has a shebang"""
        print("  Will check shebang  .. ")
        infile = open(filename)
        firstLine = infile.readline()
        infile.close()
        for she in self.shebangs:
            print(
                "??  did file ",
                filename,
                " start with ",
                she,
                " [",
                firstLine,
                "] ",
            )
            if firstLine.startswith(she):
                return True
        return False

    def ApplyCopyright(self, srcfile, dstfile):
        """will apply new Copyright on dst file then append the old src file"""
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

        if srcfile != dstfile:
            # create dir file if not exist
            nbase = os.path.dirname(dstfile)
            if not os.path.exists(nbase):
                os.makedirs(nbase)
            tmpd = dstfile
        else:
            tmp = "/tmp/tmp-fheadercopyrightLicense"

        dst = open(tmp, "w")
        isSheb = self.checkfileShebang(srcfile)
        src = open(srcfile)
        if isSheb:
            line = src.readline()
            dst.write(line)
            for cop in copyright:
                dst.write(cop)
                dst.write("\n")
            # continue copy src file
            while line:
                line = src.readline()
                dst.write(line)
        else:
            print(" \t ==>  file  ", srcfile, " DONT have shebang !")
            for cop in copyright:
                dst.write(cop)
                dst.write("\n")
            dst.write(src.read())

        dst.close()
        src.close()
        if srcfile == dstfile:
            copyfile(tmp, dstfile)
