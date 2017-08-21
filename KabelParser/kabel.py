import re
import io
from .kabel_parser import KabelParser

def parseFile(fpath):
    fin = open(fpath, "r", encoding="UTF-8")
    intext = fin.read()
    fin.close()
    return parse(intext)

def parse(textStr):
    in_lines = textStr.split("\n")
    parser = KabelParser()    
    patBracket = re.compile("\[(.*?)\]")
    for ln in in_lines:        
        if ln.startswith("//#"):
            parser.parseBlock(ln[4:].strip())
        else:
            mList = patBracket.findall(ln)
            for idvBracket in mList:
                parser.parseInline(idvBracket)

    parser.documentEnd()

    fout = io.StringIO()
    parser.write(fout)
    owl = fout.getvalue()
    fout.close()

    return owl

