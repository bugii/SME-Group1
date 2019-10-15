import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# installed requests and bs4 via py -m pip install bs4 and py -m pip install requests; alternatively, you may
# try pip install bs4 and pip install requests.
# All packages via py -m pip freeze are in the Requirements.txt in the main folder; install via pip install -m Requirements.txt

#
# This code scans the complete apache maven repository and outputs all artifacts found including their dependencies
#
url = 'https://mvnrepository.com/artifact/org.apache'
response = requests.get(url)
#sleep is here just to get used to it early on: Don't spam servers, you run the risk of being blocked
time.sleep(0.1)
print(response)

soup = BeautifulSoup(response.text, 'html.parser')
soup.findAll('a')

Linklist = []
for link in soup.find_all('a'):
    Linklist.append(link.get('href'))
print("links in " + url + " : ")
print(Linklist)

Linklist2 = []
for x in Linklist:
    if  x.startswith("/artifact"):
        Linklist2.append(x)
print("filtered links:")
print(Linklist2)

print(" ")
print("starting loop")

for y in range(len(Linklist2)-1):
    time.sleep(1)
    url2 = 'https://mvnrepository.com' + Linklist2[y]
    print(url2)
    response = requests.get(url2)

    print(response)
    Linklist.clear()
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.findAll('a')
    for link in soup.find_all('a'):
        Linklist.append(link.get('href'))
    print(Linklist)

    Linklist3=[]
    for x in Linklist:
        if x.startswith('/artifact/org.apache.maven') and not x.endswith('/usages'):
            Linklist3.append(x)
    print(Linklist3)

    """______________________________________________
    lists = soup.select("")
    print(lists)
    for x in lists:
        print(x.text)
    string1 = str(soup)
    #print(string1)
   

    #one_a_tag = soup.findAll('a')[36]
    #link = one_a_tag['href']
    #download_url = 'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite'+ link
    #urllib.request.urlretrieve(download_url, './' + link[link.find('/turnstile_') + 1:])
     """
