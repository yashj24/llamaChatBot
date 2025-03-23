from atlassian import Confluence
from bs4 import BeautifulSoup

confluence = Confluence(
   url = "https://uclalibrary.atlassian.net/wiki/",
   username = "",
   password = ""
)
file = open("spacedata.txt" , "a" , encoding = "utf-8")
def putDataInTextFile(data):
    page_title = data["title"]
    soup = BeautifulSoup(data["body"]["storage"]["value"] , "html.parser")
    file.write("Page id : "+ data["id"] + "\n")
    file.write("Page Title: " + page_title + "\n")
    file.write("Page Content : " + soup.get_text() + "\n")
    file.write("Page End, new page below.." + "\n")
    file.write("\n")
   

data1 = confluence.get_page_by_id(page_id='122454475',expand ="body.storage") # how to zoom
data2 = confluence.get_page_by_id(page_id='39129287',expand ="body.storage") # MFA
data3 = confluence.get_page_by_id(page_id='123994407',expand ="body.storage") #meeting owls overview
data4 = confluence.get_page_by_id(page_id='950239233',expand ="body.storage") # how to install oasis
data5 = confluence.get_page_by_id(page_id='39135031',expand ="body.storage") # join and Use the Library Slack Workspace
putDataInTextFile(data1)
putDataInTextFile(data2)
putDataInTextFile(data3)
putDataInTextFile(data4)
putDataInTextFile(data5)
file.close()
















