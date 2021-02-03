#!/usr/bin/env python3

import re
import sys
import os
import locale

class SongFile:
    """
    This class represents a TEX file containing a single Song
    """

    SUBAUTHOR_SEPARATORS = [',', '/', 'feat.' ]

    def __init__(self, path: str):
        self.path = path
        self._decode()

    def _decode(self):
        with open(self.path, "r") as f:
            line = f.readline()

        regex = re.compile(r'\\beginsong{([^}]+)}(\[by={([^}]+)}\])?')

        match = regex.search(line)
        if match is None:
            raise ValueError("cannot parse the first line in file '{}'".format(self.path))

        title = match[1]
        author = match[3]

        if author is not None:
            for sep in self.__class__.SUBAUTHOR_SEPARATORS:
                if sep in author:
                    author = author[:author.find(sep)].rstrip()

        self.title = title
        self.author = author

if __name__ == "__main__":
    for fn in sorted(os.listdir(sys.argv[1]), key=locale.strxfrm):
        s = SongFile(os.path.join(sys.argv[1], fn))

        print(s.author)
        

