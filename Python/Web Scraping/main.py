import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# installed requests and bs4 via py -m pip install bs4 and py -m pip install requests; alternatively, you may
# try pip install bs4 and pip install requests.
# All packages via py -m pip freeze are in the Requirements.txt in the main folder; install via pip install -m Requirements.txt

#url = 'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite'
url = 'https://mvnrepository.com/artifact/org.apache.commons'
response = requests.get(url)
#sleep is here just to get used to it early on: Don't spam servers, you run the risk of being blocked
time.sleep(0.1)
print(response)

soup = BeautifulSoup(response.text, 'html.parser')
soup.findAll('a')
#print(soup)


for link in soup.find_all('a'):
    #find all links that do not end on "usages" (otherwise all links would be de facto duplicated)
    if(link.get('href').startswith('/artifact/org.apache.commons') and not link.get('href').endswith('usages')):
        print(link.get('href'))


"""
lists = soup.select("")
print(lists)
for x in lists:
    print(x.text)
string1 = str(soup)
#print(string1)
"""

#one_a_tag = soup.findAll('a')[36]
#link = one_a_tag['href']
#download_url = 'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite'+ link
#urllib.request.urlretrieve(download_url, './' + link[link.find('/turnstile_') + 1:])
