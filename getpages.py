import re
import shutil
from bs4 import BeautifulSoup, NavigableString
from requests import get

def read(path):
    with open(path,"rt") as f:
        return f.read()

def current():
    domain = re.findall('https://cdn[a-z]+\.(?:xyz|cc)//', read("in.txt"))
    imghash = re.findall('upload\/\w{32}.jpg', read("in.txt"))
    assert(len(domain) == len(imghash))
    n = len(domain)
    #now have a list of /upload/hash.jpg
    for i in range(n):
        r = requests.get(domain[i]+imghash[i], stream=True)
        if r.status_code == 200:
            with open(str(i+1).zfill(2)+".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            
#def main():
response = get("https://manamoa.net/bbs/board.php?bo_table=manga&wr_id=3240824")
html_soup = BeautifulSoup(response.text, 'html.parser')
i = 0
parent = html_soup.find('div', attrs={'class': "view-content scroll-viewer"})
#children = parent.findChildren(recursive=True)
for child in parent.children:
    print(child)
    imgtags = child.find_all('img', src=re.compile('https://cdn[a-z]+\.(?:xyz|cc)//upload\/\w{32}.jpg'))
    for tag in imgtags:
        r = get(tag['src'], stream=True)
        if r.status_code == 200:
            i+=1
            with open(str(i+1).zfill(2)+".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)