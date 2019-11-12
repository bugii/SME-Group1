import time
import random
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import subprocess
import re

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
    f = open(filename, "a", encoding="utf-8")
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
        with open(directory + filename, encoding="utf-8") as f:
            content = f.readlines()
    except:
        print("Error in file_to_string method.")
        content = ["~FILE NOT FOUND!~"]
    content = [x.strip() for x in content]
    return content

def filter_apache_repositories(Linklist):
    Newlist = []
    for link in Linklist:
        if link.startswith("/apache/") and link.count("/")==2:
            Newlist.append(link)
    return Newlist

def create_timeline(file_list, filename):
    # Needs a list to iterate over. Everytime it findes an entry starting with pom.xml, it iterates back to find the
    # associated commit id and date. Outputs a list with the commit-date-tuples.
    output = []
    for idx, element in enumerate(file_list):
        if element.startswith(filename):
            j=idx-1
            while not file_list[j].startswith("Date: "):
                j-=1
            k=j-1
            while not file_list[k].startswith("commit "):
                k-=1
            output.append((file_list[j], file_list[k]))
    return output

def get_release_with_date(preroot):
    # Create a function to take the releases, the parameter is the url to the github project "https://github.com/apache/[project_name]"
    # The output is gonna be a list with all the releases of the project with their respective creation date.
    # Being each element of the list in the format "[release_name,yyyy-mm-dd]"
    root = preroot+"/releases"  #we add to the project url "/releases"
    releaselist = []        # create a variable to keep the releases with their respective time
    url = root
    page = requests.get(url)    #request for the page
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")

    while page.status_code == 200:      # While we get the page correctly
        for link in soup.find_all("a"):
            if re.search("/releases/tag/", link.get('href')):
                release = re.sub(".*/", "", link.get("href"))       # Here we take the name of the releases
                page1 = requests.get(root+"/tag/"+release)      # Here we look for the page of the release to take the information from it
                data1 = page1.text
                soup1 = BeautifulSoup(data1, features="html.parser")
                date = soup1.find_all("relative-time")[0]
                date = re.sub("T.*", "", date.get("datetime"))
                releaselist.append([release, date])             # We include the release and the date in the list
        url = root + "?after=" + release                    # We look for the next page of the release with the next patron [root + ?after=" + and the las release]
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")

    return releaselist                                  #We return the list

def get_bugs_period(project,from_date,to_date):
    # This function will take the link of  the apache projects from github
    # and also we have to take the begin and end dates of a period
    # And will return the numbers of bugs in the period selected
    # The dates has the following format: "yyyy-mm-dd"
    project = re.sub(".*/","",project)  #We take just the name of the project
    project = project.upper()              # convert to capital letters
    url ="https://issues.apache.org/jira/browse/"+project+"-0?jql=project%20%3D%20"+project+"%20AND%20issuetype%20%3D%20Bug%20AND%20created%20>%3D%20"+from_date+"%20AND%20created%20<%3D%20"+to_date+"%20%20ORDER%20BY%20created%20DESC"
    page = requests.get(url)    #request the page
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")      #make the parser
    for element in soup.find_all("div"):                    #if we find the div tag
        if element.get("data-issue-table-model-state") != None: # We check if we found the following information
            bugs = element.get("data-issue-table-model-state")   #and we take the information
            bugs = re.sub(".*\"total\":","",bugs)
            bugs = re.sub(",.*","",bugs)
    return int(bugs)