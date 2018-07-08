#!/usr/bin/env python3

import os, os.path
from markdown import Markdown

class WikiController:
    def __init__(self):
        self.mddir = None
        self.indexfile = None
        self.tchanged = None
        self.outhtml = None

    def setDir(self, wikidir):
        self.mddir = wikidir

    def setIndex(self, wikiindex):
        self.indexfile = wikiindex
        self.tchanged = os.stat(self.indexfile).st_mtime

    def setOut(self, outfile):
        self.outhtml = outfile

    def checkIndex(self):
        return (self.tchanged == os.stat(self.indexfile).st_mtime)

    def forceUpdate(self):
        ind = open(self.indexfile)
        gluemd = ""
        for l in ind.readlines():
            lp = os.path.join(self.mddir, l)
            gluemd += open(lp.split()[0]).read()
            gluemd += "\n\n"
        m = Markdown(output_format="html")
        htmlstr = m.convert(gluemd)
        outstream = open(self.outhtml, "w")
        outstream.write(htmlstr)
        outstream.close()
        self.tchanged == os.stat(self.indexfile).st_mtime

    def update(self):
        if not self.checkIndex():
            self.forceUpdate()

if __name__ == "__main__":
    import time
    import traceback
    import logging
    
    # argparse must be added
    WIKI_DIR = os.path.join(os.getcwd(), "wiki")
    INDEX_FILE = os.path.join(WIKI_DIR, "index.txt")
    OUT_HTML = os.path.join(WIKI_DIR, "index.html")

    wc = WikiController()
    wc.setDir(WIKI_DIR)
    wc.setIndex(INDEX_FILE)
    wc.setOut(OUT_HTML)
    wc.forceUpdate()

    while True:
        time.sleep(10)
        try:
            wc.update()
        except Exception as e:
            logging.error(traceback.format_exc())
