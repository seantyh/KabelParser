import sys
import re
from kabel_parser import KabelParser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("kabel.py <input file.kabel.txt>")
        exit()
    inkabel = sys.argv[1]
    outkabel = inkabel.replace(".kabel.txt", ".owl")
    fin = open(inkabel, "r", encoding="UTF-8")
    in_lines = list(fin.readlines())
    parser = KabelParser()
    patBracket = re.compile("\[(.*?)\]")
    for ln in in_lines:        
        if ln.startswith("//#"):
            parser.parseBlock(ln[4:].strip())
        else:
            mList = patBracket.findall(ln)
            for idvBracket in mList:
                parser.parseInline(idvBracket)
    fin.close()

    parser.documentEnd()

    fout = open(outkabel, "w", encoding="UTF-8")    
    parser.write(fout)
    fout.close()

