import functions
import os
import requests
from bs4 import BeautifulSoup
import time
import script

'''
lista = functions.return_all_links("http://github.com/apache")
lista = functions.filter_apache_repositories(lista)
clear = lambda: os.system('cls')
clear()
for repo in lista:
    aux = functions.check_doc("http://github.com"+repo)
    print("http://github.com"+repo+"/search?q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle&unscoped_q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle")
    print()
    print(aux)
    input()
    clear()


#print(lista)

i = 0
while True:
    print(i)
    i += 1
    page = requests.get("http://github.com")
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")
    time.sleep(10)
'''

'''
script.read_gradle("./")
i = script.get_number_dependencies("./")
print(i)
'''
f = open("build.gradle","r")
lines = f.readlines()
listadepen = functions.dependency_line(lines,"build.gradle")
print(listadepen)
aux = functions.dependency_number(lines,"build.gradle")
print(aux)