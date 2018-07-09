#!/usr/bin/env python3

import os, os.path
from markdown import Markdown

class WikiController:
    def __init__(self):
        self.mddir = None
        self.indexfile = None
        self.tchanged = None
        self.outhtml = None
        self.title = ""
        self.style = None

    def setDir(self, wikidir):
        self.mddir = wikidir

    def setIndex(self, wikiindex):
        self.indexfile = wikiindex
        self.tchanged = os.stat(self.indexfile).st_mtime

    def setOut(self, outfile):
        self.outhtml = outfile

    def setTitle(self, wikititle):
        self.title = wikititle

    def setStyle(self, stylename):
        self.style = stylename

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
        wrp = self._wrapping()
        htmlstr = wrp[0] + htmlstr + wrp[1]
        outstream = open(self.outhtml, "w")
        outstream.write(htmlstr)
        outstream.close()
        self.tchanged == os.stat(self.indexfile).st_mtime

    def update(self):
        if not self.checkIndex():
            self.forceUpdate()

    def _wrapping(self):
        return ('<!DOCTYPE html>\n<html>\n<meta charset="UTF-8">\n\n<head>\n<title>' + self.title + "</title>" +\
               ('<link rel="stylesheet" type="text/css" href="' + self.style + '">' if self.style else "") +\
                "</head>\n<body>", "</body>\n</html>")

if __name__ == "__main__":
    import time
    import traceback
    import logging
    
    # argparse must be added
    WIKI_DIR = os.path.join(os.getcwd(), "wiki")
    INDEX_FILE = os.path.join(WIKI_DIR, "index.txt")
    OUT_HTML = os.path.join(WIKI_DIR, "index.html")
    CSS_STYLE = os.path.join(WIKI_DIR, "style.css")
    WIKI_TITLE = "Wiki"

    wc = WikiController()
    wc.setDir(WIKI_DIR)
    wc.setIndex(INDEX_FILE)
    wc.setOut(OUT_HTML)
    wc.setStyle(CSS_STYLE)
    wc.setTitle(WIKI_TITLE)
    wc.forceUpdate()

    while True:
        time.sleep(10)
        try:
            wc.update()
        except Exception as e:
            logging.error(traceback.format_exc())
