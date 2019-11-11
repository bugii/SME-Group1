import time
import random
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import subprocess

def wait_random():
    # Generates a random wait time, usually around 1 to 2 seconds, with some longer intervals up to 7 seconds added for
    # good measure.
    int1 = random.random()
    print("Pause for a short time...")
    if(int1>0.8):
        time.sleep(4+(3*int1))
    else:
        time.sleep(2.8)
        time.sleep(int1*2)

def write_to_txt(string1, filename):
    # Writes the string supplied into a txt file in the main directory.
    f = open(filename, "a")
    f.write(string1+"\n")
    f.close()

def write_to_dependencies_txt(string1):
    # Writes string1 to the txt-file and adds a newline character.
    f = open("dependencies.txt", "a")
    f.write(string1 + "\n")
    f.close()

def return_all_links(url):
    # As it says: Returns all links from a website. If the website does not respond with 200, it returns a list with 0 as
    # the only element.
    Linklist = []
    page = requests.get(url)
    if page.status_code != 200:
        return [0]
    else:
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        for link in soup.find_all('a'):
            Linklist.append(link.get('href'))
        return Linklist

"""def deepscan_url(url):
# Note that this is a very specific block of code. It extracts all urls that end on .pom.
    Linklist = return_all_links(url)
    for x in Linklist:
        if x.endswith(".pom"):
            write_to_txt(url + x)
            print("Writing to txt: " + url + x)
        else:
            if x.endswith("/") and not x.endswith("../"):
                print("Proceeding to: "+ url + x)
                deepscan_url(url + x)
"""

def create_dependency_from_str_soup(soup):
    # The output looks like this: MyProject/MyProject/1.4.2::, which encodes groupId, artifactId and version
    # of the project; this is followed by dependencies in the exact same format, seperated by a single colon.
    # I.e.: MyProject/MyProject/1.4.2::jUnit/jUnit/1.2.7:OtherGroup/OtherArtifact/1.0.1
    outputline = ""
    outputline = outputline + str(soup[soup.find("<groupid>")+9:soup.find("</groupid>")]) + "/"
    outputline = outputline + str(soup[soup.find("<artifactid>")+12:soup.find("</artifactid>")]) + "/"
    outputline = outputline + str(soup[soup.find("<version>")+9:soup.find("</version>")]) + "::"
    print(outputline)

    if soup.find("<dependencies>") != -1:
        dependencies = str(soup[soup.find("<dependencies>")+14:soup.find("</dependencies>")]).splitlines()
        print(dependencies)
        temp_string = ""
        for x in dependencies:
            if x.startswith("<groupid>") or x.startswith("<artifactid>"):
                temp_string = temp_string + x[x.find(">")+1:x.find("</")] + "/"
            elif x.startswith("<version>"):
                outputline = outputline + temp_string + x[x.find(">")+1:x.find("</")] + ":"
                temp_string = ""
    else:
        outputline = outputline + "none"

    return(outputline)

def dependencies_from_pom_url(url):
    response = requests.get(url)
    print(response)
    wait_random()
    soup = BeautifulSoup(response.text, 'html.parser')
    write_to_dependencies_txt(create_dependency_from_str_soup(str(soup)))

def command_window(*args):
    # Allows command window inputs via String Arguments (separated by commas), i.e. ("git", "status") for "git status"
    # If the first keyword starts with "cwd=", i.e. ("cwd=Folder01", "dir"), it executes the following commands in this
    # very subdirectory (here it would list the content of Folder01 via the "dir" command).
    if args[0].startswith("cwd="):
        directory = args[0][4:]
        out = subprocess.check_output(list(args[1:]), cwd=directory)
        return out.decode() # returns a string with integrated newline characters (readability)
    else:
        subprocess.check_output(list(args))
        return subprocess.getoutput(list(args))

def file_to_stringlist(filename, directory):
    # Straightforward: Tries to read the file in the given directory and outputs a list with the lines.
    # Example: ("file99.txt", "Repositories/Folder01/"). Note that "directory" can be left empty for home directory.
    try:
        with open(directory + filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
    except:
        print("Error in file_to_string method: File or directory invalid.")
        content = ["~FILE NOT FOUND!~"]
    return content

def filter_apache_repositories(Linklist):
    Newlist = []
    for link in Linklist:
        if link.startswith("/apache/") and link.count("/")==2:
            Newlist.append(link)
    return Newlist