from abc import ABC, abstractmethod
from msilib.schema import Error
import win32com.client
from xmlRulesReader import *
from datetime import *
class outlookApi(object):
    """
    Outlook Api Stuff:
    """
    olFolderInbox = 6
    olMail = 43

    def __init__(self,recipient) -> None:
        self.__outlook = win32com.client.Dispatch("Outlook.Application")
        self.__mapi = self.__outlook.GetNamespace("MAPI")
        self.__recipient = None
        self.__mailItems = None
        self.setRecipient(recipient)
            
    def setRecipient(self, recipient):
        self.__recipient = self.__mapi.CreateRecipient(recipient)
        self.__recipient.Resolve

    def readMailItemsFromInbox(self):
        self.__mailItems = self.__mapi.GetSharedDefaultFolder(self.__recipient, self.olFolderInbox).Items
        return (x for x in self.__mailItems if x.Class == self.olMail)

    def readMailItemsFromInboxByFilter(self, filter, dict):
        filterString = filter(dict)
        self.__mailItems = self.__mapi.GetSharedDefaultFolder(self.__recipient, self.olFolderInbox).Items.Restrict(filterString)
        return (x for x in self.__mailItems if x.Class == self.olMail)
   
    def __repr__(self) -> str:
        return "\n".join(map(lambda x : x.Subject, self.__mailItems)) + str(len (self.__mailItems))
    
def filter(filterDict):
    sw ={
        "SenderEmailAddress"    :   "((urn:schemas:httpmail:fromemail Like '%VALUE%') OR (http://schemas.microsoft.com/mapi/proptag/0x5D02001F Like '%VALUE%'))",
        "Subject"               :   "(urn:schemas:httpmail:subject Like '%VALUE%')",
        "ReceivedTime"          :   "(urn:schemas:httpmail:datereceived < 'VALUE')",
    }
    
    return "@SQL=" + " AND ".join([ sw[fName].replace("VALUE", fValue) if fName != "ReceivedTime" else \
                                    sw[fName].replace("VALUE", (datetime.today() - timedelta(days=int(fValue))).strftime('%Y-%m-%d %H:%M %p')) \
                                    for fName, fValue in filterDict.items()])

ol = outlookApi("Region.Mitte.Verkehrsdispo.Trier@deutschebahn.com")
#ol.out()
#print(ol.find("00000000874D1B6A6D17A24AB78977D94C9943410700F97EE50A14DD0D40B89EC2D8805390DC00000000010C0000F97EE50A14DD0D40B89EC2D8805390DC00031CAEC6E20000","Jan.Ehrmantraut@deutschebahn.com"))

xmlFile = 'rules.xml'
xml = xmlReader(xmlFile)
xmlFuncTest = xmlReaderMethods(xml.root)
rules = xmlFuncTest.getRuleSets()
critValues = (rules[0].rules[0].criteria)
#critValues.pop("Subject")
#critValues.pop("ReceivedTime")
print(filter(critValues))
ol.readMailItemsFromInboxByFilter(filter,critValues)
print(ol)



