import logging
import re
import pdb

inline_pat = re.compile("([=#:])?([^=#:\]]+)")
FrameHead = ["Class", "Inidvidual", "ObjectProperty", "DataProperty"]

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel("DEBUG")

class KabelParser:
    def __init__(self):
        self.state = {}
        self.blockNames = []
        self.blockBuf = []
        self.blockList = []
        self.inlineList = []
        self.idvMap = {}
    
    def documentEnd(self):
        if self.blockBuf:
            self.blockNames.append(self.state["blockHead"])
            self.blockList.append(self.blockBuf)
            self.blockBuf = []
        self.linkIndividuals()

    def parseBlock(self, blockStr):
        lineValue = blockStr[blockStr.find(":")+1:].strip()
        lineHead = blockStr[:blockStr.find(":")].strip()
        
        if lineHead in FrameHead:
            if self.blockBuf:
                self.blockNames.append(self.state.get("blockName", ""))
                self.blockList.append(self.blockBuf)
                self.blockBuf = []
            self.state["blockName"] = lineValue
            self.state["blockHead"] = lineHead

        # store current line into self.blockBuf
        if lineHead not in FrameHead:
            blockStr = "  " + blockStr
        else:
            blockStr = "\n" + blockStr

        self.blockBuf.append(blockStr)        
        
    def parseInline(self, inlineStr):
        mList = inline_pat.findall(inlineStr)        
        if not mList:
            print("invalid inline: ", inlineStr)
            return
        oriText = mList[0][1]

        idvType = ""; idvAlias = ""; idvName = oriText
        if len(mList) > 1:
            logger.debug("mList.groups: %s", mList)
            for m in mList[1:]:
                prefix = m[0]
                if prefix == ":":
                    idvType = m[1]
                elif prefix == "#":
                    idvName = m[1]
                elif prefix == "=":
                    idvAlias = m[1]

        idvData = {
            "text": oriText,  "name": idvName,
            "alias": idvAlias, "type": idvType}
        idvObj = {}

        if idvName:
            self.idvMap[idvName] = idvData
            self.inlineList.append(idvName)
        else:
            self.idvMap[oriText] = idvData
            self.inlineList.append(oriText)

    def linkIndividuals(self):
        for blockIdx, blockHead in enumerate(self.blockNames):
            blockLines = self.blockList[blockIdx]
            if blockHead == "Individual":
                hasExpanded, expLines = self.expandIdvFrame(blockLines)
                self.blockList[blockIdx] = expLines
            elif blockHead == "Class":
                pass
            elif blockHead == "ObjectProperty":
                pass
            elif blockHead == "DataProperty":
                pass
            else:
                pass

        for idvName in self.inlineList:
            hasExpanded = self.idvMap[idvName].get("hasExpanded", False)
            if not hasExpanded:
                idvObj = self.idvMap[idvName]                
                blockStr = ["\nIndividual: " + idvObj["name"]]
                if idvObj["type"]:
                    blockStr.append("  Type: " + idvObj["type"])
                self.blockList.append(blockStr)                    

    def expandIdvFrame(self, lines):
        expLines = []
        ln0 = lines[0]
        idvName = ln0[ln0.find(":")+1:].strip()
        idvObj = self.idvMap.get(idvName, None)
        
        if idvObj:
            ln0 = ln0.replace(idvName, idvObj["name"])
            expLines.append(ln0)
            expLines += lines[1:]
            
            if idvObj.get("type", ""):
                expLines.append("  Type: %s" % idvObj["type"])
            idvObj["hasExpanded"] = True
        else:
            idvObj["hasExpanded"] = False

        return expLines

    def write(self, fobj):
        for block in self.blockList:
            blockStr = "\n".join(block)
            fobj.write(blockStr)
            fobj.write("\n")




