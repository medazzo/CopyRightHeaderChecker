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
        print("")
        print("----------------------------------------")
        print("* Header checker         : ", self.brief)
        print("* Header extensions      : ", self.extensions)
        print("* Header fileNames       : ", self.fileNames)
        print("* Header copyrightHeader :  ")
        for line in self.copyrightHeader:
            print(self.startLine, line, self.endLine)

    def findFile(self, filename):
        """return True if filename will be managed with this header"""
        # Check if file is in names
        if filename in self.fileNames:
            self.filesManaged.append(filename)
            return True
        for ext in self.extensions:
            if filename.endswith(ext):
                self.filesManaged.append(filename)
                return True
        return False
