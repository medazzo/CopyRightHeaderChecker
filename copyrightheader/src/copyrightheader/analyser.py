import ntpath
import os
import time

from copyrightheader.header import Header


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
        print("- - - - - - -  Analyse - - - - - - -")
        start = time.time()
        self.FindFiles()
        end = time.time()
        took = end - start
        print("- - - - - - -  Analyse - - took %.4f sec -" % took)
        print("- - - - - - -  Process - - - - - - -")
        start = time.time()
        self.ApplyNewHeader()
        end = time.time()
        took = end - start
        print("- - - - - - -  Process - - took %.4f sec -" % took)

    def ApplyNewHeader(self):
        """will apply new Copyright on array of files into OutDir with Same tree as original"""
        self.conf.GenerateNewCopyright()
        print("- -  we will use Header :")
        for w in self.conf.newCopyrightHeader:
            print(">", w, "<")
        print("- - ")
        filesUpdated = 0
        for h in self.conf.headers:
            for x in h.filesManaged:
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

                self.conf.ApplyCopyright(x, nfile, h)
                filesUpdated = filesUpdated + 1
        print("  - - -	=> ", format(filesUpdated), " files are updated ")

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
                    print(
                        " ! ==> Cannot find Header for file --> ",
                        format(sfileN),
                    )
                    self.filesUnsupported.append(sfileN)
        for h in self.conf.headers:
            print("   - ", len(h.filesManaged), "   ", h.brief, " files.")
        print(
            "  - - -	! ",
            len(self.filesAlreadyCopyright),
            " files are already with a Copyright Headers :",
        )
        for x in self.filesAlreadyCopyright:
            print("   - ", x)
        print(
            "  - - -	! ",
            len(self.filesUnsupported),
            " files are Unsupported :",
        )
        for x in self.filesUnsupported:
            print("   - ", x)
