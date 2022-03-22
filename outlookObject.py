from abc import ABC, abstractmethod
from ast import YieldFrom
import win32com.client
from xmlRulesReader import *
from datetime import *
class outlookApi(object):
    """
    Outlook Api Stuff:
    """
    olFolderInbox = 6
    olMail = 43

    def __init__(self) -> None:
        self.__outlook = win32com.client.Dispatch("Outlook.Application")
        self.__mapi = self.__outlook.GetNamespace("MAPI")
        self.__recipient = None
        self.__mailItems = None
            
    def setRecipient(self, recipient):
        self.__recipient = self.__mapi.CreateRecipient(recipient)
        self.__recipient.Resolve

    def getFolderByString(self, FolderString):
        if isinstance(FolderString, str):
            strList = FolderString.split('|')
            rootFolder = self.__mapi.GetSharedDefaultFolder(self.__recipient, self.olFolderInbox).Parent
            for folder in strList:
                rootFolder = rootFolder.Folders(folder)
            return rootFolder

    def readMailItemsFromInbox(self):
        self.__mailItems = self.__mapi.GetSharedDefaultFolder(self.__recipient, self.olFolderInbox).Items
        yield from self.__mailItems 
 
    def readMailItemsFromInboxByFilter(self, filter, dict):
        filterString = filter(dict)
        yield from  self.__mapi.GetSharedDefaultFolder(self.__recipient, self.olFolderInbox).Items.Restrict(filterString)

    def find(self, id):
        return self.__mapi.GetItemFromID(id)

    def __repr__(self) -> str:
        if self.__mailItems is None or (len(self.__mailItems) == 0):
            return "No Mails loaded. Load with: \n \t 'readMailItemsFromInbox()' or \n \t 'readMailItemsFromInboxByFilter(filter, dict)' " 
        else:
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


#id = '00000000791E8F48704B174BACEB6C34D285EAA507008E1BA98461214C4A92B4611F6831E8D500000000010C00008E1BA98461214C4A92B4611F6831E8D500028D5A841A0000'

#ol = outlookApi()
#tl = ol.find(id)
#print("Wait")