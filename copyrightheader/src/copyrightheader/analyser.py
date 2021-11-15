import ntpath
import os
import time


class Analyser:
    """Header class"""

    def __init__(self, inputFolder, dryRun, conf):
        self.inputFolder = inputFolder
        self.dryRun = dryRun
        self.conf = conf
        if dryRun:
            self.outputfolder = "./tmp"
        else:
            self.outputfolder = self.inputFolder

    def info(self):
        print("")
        print("----------------------------------------")
        print("* Header checker         : ", self.brief)
        print("* Header extensions      : ", self.extensions)
        print("* Header fileNames       : ", self.fileNames)
        print("* Header copyrightHeader :  ")
        for line in self.copyrightHeader:
            print(self.startLine, line, self.endLine)

    def process(self):
        """Process and start copyright header checks"""
        print("- - - - - - -  Analyse  - - - - - - ->")
        self.FindFiles()
        print("- - - - - - -  Process  - - - - - - ->")
        if not self.dryRun:
            self.ApplyIn()
        else:
            self.ApplyInTmp()
        print("     Generated   to ", self.Outputfolder)
        print("<- - - - - - - Done - - - - - - - - - -")

    def ApplyInTmp(self):
        """will apply new Copyright on array of files into OutDir with Same tree as original"""
        start = time.time()
        for h in self.conf.headers:
            for x in h.filesManaged:
                # fix filename
                p = os.path.dirname(x)
                while p.startswith("../"):
                    p = p[3:]
                if p.startswith("/"):
                    p = p[1:]
                Ofolder = self.outputfolder + "/" + p
                nfile = Ofolder + "/" + ntpath.basename(x)
                h.ApplyCopyright(x, nfile)
        end = time.time()
        took = end - start
        print(
            "  - - - - - - Applying ",
            h.brief,
            " took  %.4f sec  - - - - - - " % took,
        )

    def ApplyIn(self):
        """will apply new Copyright on array of files into original Dir"""
        # checks
        start = time.time()
        for h in self.conf.headers:
            for x in h.filesManaged:
                h.ApplyCopyright(x, x)
        end = time.time()
        took = end - start
        print(
            "  - - - - - - Applying ",
            h.brief,
            " took  %.4f sec  - - - - - - " % took,
        )

    def FindFiles(self):
        """Find all concerned files as defined up"""
        start = time.time()
        for root, dirs, files in os.walk(self.inputFolder):
            dirs[:] = [d for d in dirs if d not in self.conf.excludeDirs]
            for x in files:
                sfileN = os.path.join(root, x)
                print(" ==>  Checking file --> {}", format(sfileN))
                #  check old copyright
                if self.conf.checkfileCopyright(sfileN):
                    self.conf.filesAlreadyCopyright.append(sfileN)
            # checks
            found = False
            for h in self.conf.headers:
                if h.findFile(sfileN):
                    print(h.brief, " >>   Found file --> ", sfileN)
                    found = True
                    break
        end = time.time()
        took = end - start
        print("  - - - - - - Analyse   took  %.4f sec  - - - - - - " % took)
        for h in self.conf.headers:
            print(
                "  - - - - - -    ",
                len(h.filesManaged),
                "            ",
                h.brief,
                " files.",
            )
        print(
            "  - - - - - -  	! ",
            len(self.conf.filesAlreadyCopyright),
            " files are already with a Copyright Headers :",
        )
        for x in self.conf.filesAlreadyCopyright:
            print("   - ", x)
