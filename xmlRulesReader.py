from abc import ABC, abstractmethod
from dataclasses import dataclass
from xml.dom.minidom import *
from pathlib import Path
import os

class IXmlReader(ABC):

    pass

class xmlReader (IXmlReader):
    
    def __init__(self, xmlFilename) -> None:
        self.__xmlFile = xmlFilename
        self.__absolutepath =  os.path.abspath(__file__)
        self.__fileDirectory = Path(os.path.dirname(self.__absolutepath))
        self.__xmlStringPath = str(self.__fileDirectory / self.__xmlFile)
        self.__dom_object = parse(self.__xmlStringPath)
        self.root = self.__dom_object.documentElement

class xmlReaderMethods(object):

    def __init__(self, xmlMiniDomObj) -> None:
        self.xmlMiniDom = xmlMiniDomObj

    def getDictFromAttributeValuesByTag(self, tag):
        return {self.getNameFromNode(x):self.getValueFromNode(x) for x in self.xmlMiniDom.getElementsByTagName(tag)}
        
    def getListFromTagValues(self, tag):
        return [self.getValueFromNode(x) for x in self.xmlMiniDom.getElementsByTagName(tag)]
    
    def getListFromTag(self, tag):
        return self.xmlMiniDom.getElementsByTagName(tag)

    def getValueFromTag(self):
        return list(self.xmlMiniDom.attributes.values())[0].value

    def getRuleSets(self):
        return ruleSets(self.getListFromTag("ruleset"))    

    def getValueFromNode(self, node):
        return list(node.attributes.values())[0].value

    def getNameFromNode(self, node):
        return list(node.attributes.values())[0].name
    
@dataclass
class ruleSets(list):

    def __init__(self, sets) -> None:
        self.extend([ruleSet(x) for x in sets])

@dataclass
class ruleSet(object):

    def __init__(self, set) -> None:
        self.set = xmlReaderMethods(set)
        self.DisplayName = self.set.getValueFromTag()
        self.Recipient = self.set.getListFromTagValues("mailinPath")[0]
        self.rules = [rule(x) for x in self.set.getListFromTag("rule")]

@dataclass
class rule(object):

    def __init__(self, obj) -> None:
        self.obj = xmlReaderMethods(obj)
        self.operation = self.obj.getValueFromTag()
        self.criteria = self.obj.getDictFromAttributeValuesByTag("criteria")
        self.targetPath = next(iter(self.obj.getListFromTagValues("targetPath")),None)
        

xmlFile = 'rules.xml'
xml = xmlReader(xmlFile)
xmlFuncTest = xmlReaderMethods(xml.root)
rueles = xmlFuncTest.getRuleSets()




