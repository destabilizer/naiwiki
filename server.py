#!/usr/bin/env python3

import os, os.path
from markdown import Markdown
import subprocess

ROOT_FILE = "index.md"

class WikiController:
    def __init__(self):
        self.gitdir = None
        self.outdir = None
        self.lastcommit = None
        self._md = Markdown()

    def setGit(self, gitDir):
        self.gitdir = gitDir
    
    def setOut(self, outDir):
        self.outdir = outDir
    
    def isUpToDate(self):
        return self.lastcommit == self.upCommit()

    def upCommit(self):
        res = subprocess.run(['git', 'log', '-n', '1'], cwd=self.gitdir, stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').split()[1]

    def _setUpToDate(self):
        self.upcommit = self.upCommit()
    
    def _compileHTML(self, filename=ROOT_FILE):
        head, body = self._compile(filename)
        outhtml = '<!DOCTYPE html>\n<html>\n<meta charset="UTF-8">\n\n<head>\n' +\
                  head + '\n</head>\n<body>' + body + "\n</body>\n</html>\n"
        outname = os.path.join(self.outdir, ".".join(filename.split(".")[:-1]) + ".html")
        f = open(outname, "w")
        f.write(outhtml)
        f.close()
        
    def _compilecmd(self, line):
        l = line.split()
        if l[0] == "@compile":
            self._compileHTML(filename=l[1])
            return ("", "")
        elif l[0] == "@insert":
            t = self._compile(l[1])
            return ("", t[1])
        elif  l[0] == "@style":
            return ('<link rel="stylesheet" type="text/css" href="' + l[1] + '">', "")
        elif l[0] == "@title":
            return ('<title>' + ' '.join(l[1:]) + '</title>', "")
        else:
            ... # what?

    def _compile(self, filename):
        src = open(os.path.join(self.gitdir, filename))
        srclines = src.readlines()
        outhead, outbody = "", ""
        srcmd = ""
        for l in srclines:
            if l[0] == "@":
                t = self._compilecmd(l)
                if t[1] != "":
                    outbody += self._md.convert(srcmd) + "\n"
                    scrmd = ""
                outhead += t[0]; outbody += t[1]
            else:
                srcmd += l
        outbody += self._md.convert(srcmd)
        return (outhead, outbody)

    def update(self):
        if not self.isUpToDate():
            self._compileHTML()
            self._setUpToDate()

if __name__ == "__main__":
    import time
    import traceback
    import logging
    import sys
    
    wc = WikiController()
    wc.setGit(sys.argv[1])
    wc.setOut(sys.argv[2])

    while True:
        try:
            subprocess.run(['git', 'pull'], cwd=wc.gitdir, stdout=subprocess.PIPE)
            wc.update()
        except Exception as e:
            logging.error(traceback.format_exc())
        time.sleep(30)
