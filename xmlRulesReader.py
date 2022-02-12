from abc import ABC, abstractmethod
from xml.dom.minidom import *
from pathlib import Path
import os

class IXmlReader(ABC):

    @abstractmethod
    def getMailInPathsFromXML(self):
        pass

    @abstractmethod
    def getRulesByRuleSetName(self, ruleSetName):
        pass

class xmlReader (IXmlReader):
    
    def __init__(self, xmlFilename) -> None:
        self.__xmlFile = xmlFilename
        self.__absolutepath =  os.path.abspath(__file__)
        self.__fileDirectory = Path(os.path.dirname(self.__absolutepath))
        self.__xmlStringPath = str(self.__fileDirectory / self.__xmlFile)
        self.__dom_object = parse(self.__xmlStringPath)
        self.__root = self.__dom_object.documentElement

    def getMailInPathsFromXML(self):
        return [(x.getAttribute("name"),[y.getAttribute("path")for y in x.getElementsByTagName("mailinPath")])for x in self.__root.getElementsByTagName("ruleset")]

    def getRulesByRuleSetName(self, ruleSetName):
        root = self.__root.getElementsByTagName("ruleset")
        for x in root:
            if x.getAttribute("name") == ruleSetName:
                return [self.__getRuleAsList(y) for y in x.getElementsByTagName("rule")]

    def __getRuleAsList(self, domObject):
        return [domObject.getAttribute("tag")] + [self.__retValueByType(x) for x in domObject.childNodes if x.nodeType == 1 ]

    def __retValueByType(self,value):
        checkList = ["name","absender","tage","path"]
        for x in checkList:
            if value.hasAttribute(x):
                if value.tagName == "criteria":
                    return (value.tagName,x, value.getAttribute(x))
                return (value.tagName,value.getAttribute(x))
        raise NotImplemented

"""xmlFile = 'rules.xml'
xml = xmlReader(xmlFile)

print(xml.getRulesByRuleSetName("Verkehrsdispo"))
print(xml.getMailInPathsFromXML())"""




    