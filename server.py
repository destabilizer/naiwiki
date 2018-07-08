#!/usr/bin/env python3

import os, os.path
from markdown import Markdown

class WikiController:
    def __init__(self):
        mddir = None
        indexfile = None
        tchanged = None
        outhtml = None

    def setDir(self, wikidir):
        mddir = wikidir

    def setIndex(self, wikiindex):
        indexfile = wikiindex
        tchanged = os.stat(self.indexfile).st_mtime

    def setOut(self, outfile):
        outhtml = outfile

    def checkIndex(self):
        return (os.stat(self.indexfile).st_mtime == self.tchanged)

    def forceUpdate(self):
        ind = open(indexfile)
        gluemd = ""
        for l in ind.readlines():
            lp = os.path.join(mddir, l)
            gluemd += open(lp).read()
            gluemd += "\n\n"
        m = Markdown(output_format="html")
        htmlstr = m.convert(gluemd)
        outstream = open(outhtml, "w")
        outstream.write(htmlstr)
        outstream.close()

    def update(self):
        if not self.checkIndex():
            self.forceUpdate()

if __name__ == "__main__":
    import time
    
    # argparse must be added
    WIKI_DIR = os.path.join(os.getcwd(), "wiki")
    INDEX_FILE = os.path.join(WIKI_DIR, "index.txt")
    OUT_HTML = os.path.join(WIKI_DIR, "index.html")

    wc = WikiController()
    wc.setDir(WIKI_DIR)
    wc.setIndex(INDEX_FILE)
    wc.setOut(OUT_HTML)

    while True:
        time.sleep(10)
        try:
            wc.update()
