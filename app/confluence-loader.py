from atlassian import Confluence
from bs4 import BeautifulSoup

confluence = Confluence(
   url = "https://uclalibrary.atlassian.net/wiki/",
   username = "",
   password = ""
)
def getAllSpaceKeys(confluence):
    print("inside getAllSpaceKeys")
    start = 0
    limit = 100
    spaceId = []
    while True:
        spacesBatch = confluence.get_all_spaces(start , limit)
        for space in spacesBatch["results"]:
            spaceId.append(space['key'])
        start += limit
        if len(spacesBatch["results"]) < limit:
            break
    return spaceId

def getAllPagesOfSpace(confluence , spaceKey):
    start = 0
    limit = 1000
    _all_pages = []
    while True:
        pages = confluence.get_all_pages_from_space(spaceKey , start , limit , content_type='page')
        _all_pages += pages
        if len(pages) < limit :
            break
        start += limit
    return _all_pages


allpages = getAllPagesOfSpace(confluence , "LITKB")
print(len(allpages))
file = open("spacedata.txt" , "a" , encoding = "utf-8")
print("Writing space content in file")
for page in allpages:
    page_content = confluence.get_page_by_id(page['id'],expand ="body.storage")
    page_title = page_content["title"]
    soup = BeautifulSoup(page_content["body"]["storage"]["value"] , "html.parser")
    file.write("Page id : "+ page["id"])
    file.write("Page Title: " + page_title )
    file.write("Page Content : " + soup.get_text())
    file.write("\n")

file.close()