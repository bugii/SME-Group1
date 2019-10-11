import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# installed requests and bs4 via py -m pip install bs4 and py -m pip install requests; alternatively, you may
# try pip install bs4 and pip install requests

url = 'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite'
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, 'html.parser')
soup.findAll('a')
print(soup)

#one_a_tag = soup.findAll('a')[36]
#link = one_a_tag['href']
#download_url = 'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite'+ link
#urllib.request.urlretrieve(download_url, './' + link[link.find('/turnstile_') + 1:])
#time.sleep(1)