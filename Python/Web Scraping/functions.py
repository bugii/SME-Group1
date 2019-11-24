import time
import random
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import subprocess
import re
from datetime import datetime
from datetime import timedelta

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

def date_normalization(date):
    # expects input of the form 'Date:   Tue Nov 19 16:52:55 2019 +0000 [...]"; outputs 2019-11-19.
    output = ""
    try:
        if date[27] == " ":
            output = output + date[28:32]
        else:
            output = output + date[27:31]
    except:
        print("Unexpected date format. Returning empty string.")
        return(output)
    output = output + "-"
    if date[12:15]=="Jan":
        output = output + "01"
    elif date[12:15]=="Feb":
        output = output + "02"
    elif date[12:15]=="Mar":
        output = output + "03"
    elif date[12:15]=="Apr":
        output = output + "04"
    elif date[12:15]=="May":
        output = output + "05"
    elif date[12:15]=="Jun":
        output = output + "06"
    elif date[12:15]=="Jul":
        output = output + "07"
    elif date[12:15]=="Aug":
        output = output + "08"
    elif date[12:15]=="Sep":
        output = output + "09"
    elif date[12:15]=="Oct":
        output = output + "10"
    elif date[12:15]=="Nov":
        output = output + "11"
    elif date[12:15]=="Dec":
        output = output + "12"
    output = output + "-"
    if date[17]==" ":
        output = output + "0" + date[16]
    else:
        output = output + date[16:18]
    return(output)

def date1_greater_date2(date1, date2):
    # takes 2019-11-19, 2018-12-12 and compares the raw numbers for size; here, the first on is greater, so the function
    # returns True.
    try:
        date1 = date1[:4] + date1[5:7] + date1[8:]
        date2 = date2[:4] + date2[5:7] + date2[8:]
        return int(date1)>int(date2)
    except:
        print("Invalid date comparison.")
        return False

def date_adder(date, days):
    try:
        datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
        datetime_object = datetime_object + timedelta(days)
        return datetime_object.strftime('%Y-%m-%d')
    except:
        print("Invalid Date adder.")
        return ""


def clear_folder(folder):
    try:
        print("Clearing folder: " + folder)
        command_window("rm", "-rf", folder)  # Erases folder
        command_window("mkdir", folder)  # Creates folder
    except:
        print("Cannot clear folder " + folder)

def clear_main(list_to_clear):
    # clears all folders in list_to_clear (i.e. "f:Folder034"); deletes the other files (i.e. "myfile01") in main directory
    for i in list_to_clear:
        if i.startswith("f:"):
            clear_folder(i[2:])
        else:
            print("Deleting: " + i)
            command_window("rm", "-rf", i)

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
"""

def dependency_line(string_list, file_type):
    # Needs a string list as input (from either pom.xml or build.gradle files) and file_type ("pom.xml" or "build.gradle")
    # and creates a string as an output of the form groupID/artifactID/version;groupID/artifactID/version;..., containing
    # every dependency found in string_list.
    output_string = ""
    if file_type == "pom.xml":
        for idx,val in enumerate(string_list):
            if val == "<dependency>" and string_list[idx+1].startswith("<groupId>") and string_list[idx+3].startswith("<version>"):
                output_string = output_string +\
                                string_list[idx+1][9:string_list[idx+1].rindex("<")]+\
                                "/"\
                                +string_list[idx+2][12:string_list[idx+2].rindex("<")]+\
                                "/"\
                                +string_list[idx+3][9:string_list[idx+3].rindex("<")]+\
                                ","
        return output_string
    else:
        print("For Claudia")

def dependency_number(string_list, file_type):
    # for pom.xml or build.gradle files: couunts the number of dependencies in that file.
    if file_type == "pom.xml":
        return string_list.count("<dependency>")
    else:
        print("For Claudia (again)")

"""
def dependencies_from_pom_url(url):
    response = requests.get(url)
    print(response)
    wait_random()
    soup = BeautifulSoup(response.text, 'html.parser')
    write_to_dependencies_txt(create_dependency_from_str_soup(str(soup)))
"""

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
    if len(content) == 0:
        print("EMPTY FILE!")
        content = ["EMPTY FILE!"]
    return content

def filter_apache_repositories(Linklist):
    Newlist = []
    for link in Linklist:
        if link.startswith("/apache/") and link.count("/")==2:
            Newlist.append(link)
    return Newlist

def create_timeline(file_list, filename):
    # Needs a list to iterate over. Every time it finds an entry starting with "filename", it iterates back to find the
    # associated commit id and date. Outputs a list with the commit-date-tuples. Only functions with github logs.
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
    releases = "-1"

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
        if releases != "-1":
            url = root + "?after=" + release                    # We look for the next page of the release with the next patron [root + ?after=" + and the las release]
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, features="html.parser")
        else:
            page.status_code = 404
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
    bugs = -1
    for element in soup.find_all("div"):                    #if we find the div tag
        if element.get("data-issue-table-model-state") != None: # We check if we found the following information
            bugs = element.get("data-issue-table-model-state")   #and we take the information
            bugs = re.sub(".*\"total\":","",bugs)
            bugs = re.sub(",.*","",bugs)
    return int(bugs) # if the project can't be found on Jira, it returns -1.

def generate_Apache_link_list(upper_boundary):
    # Scans the github Apache repositories (see "url") and copies all project links into a .txt file; also returns
    # them as a list.
    Apache_Project_Links = []
    i = 1
    while i != -1 and i <= upper_boundary:
        if i == 1:
            url = "https://github.com/apache?utf8=%E2%9C%93&q=&type=source&language="
        else:
            url = "https://github.com/apache?language=&page=" + str(i) + "&q=&type=source&utf8=%E2%9C%93"
        output = return_all_links(url)
        if output[0] == 0:
            i = -1
        else:
            output = filter_apache_repositories(output)
            Apache_Project_Links.extend(output)
            print("Page " + str(i) + " done. Waiting 10 seconds...")
            time.sleep(10.1)
            i += 1
    for i in Apache_Project_Links:
        write_to_txt(i, "ApacheGithubLinks.txt")
    return Apache_Project_Links

def write_dependency_timelines(txt, dir, MaxNumberOfClones=-1):
    # from the .txt file in directory dir: Uses the entries as links to clone the github repositories, extract the
    # number of dependencies and write them into a file in the "Dependencies" folder. After that, it clears the
    # "Repositories" folder.
    for i in file_to_stringlist(txt, dir):
        if MaxNumberOfClones==0:
            break
        elif MaxNumberOfClones>0:
            print("Attempting to clone " + str(MaxNumberOfClones) + " more repositories")
        dependency_filename = ""
        if check_existence_on_github(i, "pom.xml"):
            dependency_filename = "pom.xml"
        elif check_existence_on_github(i, "build.gradle"):
            dependency_filename = "build.gradle"
        else:
            print(i + " does not contain pom.xml or build.gradle. Proceeding to next link.")
            continue
        clear_folder("Repositories")
        try:
            command_window("cwd=Repositories", "git", "clone", "https://github.com" + i, "-b", "master")
            print("Writing log for " + i[i.rindex("/"):])
            output = command_window("cwd=Repositories" + i[i.rindex("/"):], "git", "log", "--stat")
            write_to_txt(str(output), "Logs/Git_Log_" + i[i.rindex("/") + 1:] + ".txt")
            MaxNumberOfClones -= 1
            time.sleep(0.1)
            output = file_to_stringlist("Git_Log_" + i[i.rindex("/") + 1:] + ".txt", "Logs/")
            output = create_timeline(output, dependency_filename)
            for j in output:
                try:
                    command_window("cwd=Repositories/" + i[i.rindex("/") + 1:], "git", "checkout", j[1][7:], dependency_filename)
                    dep_file_line_list = file_to_stringlist(dependency_filename, "Repositories" + i[i.rindex("/"):] + "/")
                    print("Writing dependencies for " + i[i.rindex("/") + 1:])
                    write_to_txt(j[0] + " : " + str(dependency_number(dep_file_line_list, dependency_filename)),
                                 "Dependencies/" + i[i.rindex("/") + 1:] + ".txt")
                    write_to_txt(dependency_line(dep_file_line_list, dependency_filename),
                                 "Dependencies/" + i[i.rindex("/") + 1:] + "_2.txt")
                    time.sleep(0.1)
                except:
                    print(dependency_filename + " did not exist for " + j[1])
        except:
            print("Exception in cloning.")

def write_release_timelines(txt, dir):
    for i in file_to_stringlist(txt, dir):
        print("["+i+"]---")
        try:
            for j in get_release_with_date("https://github.com" + i):
                write_to_txt(j[1] + " : " + j[0], "Releases/" + i[i.rindex("/") + 1:] + ".txt")
                print("Writing releases for " + i[i.rindex("/") + 1:])
                time.sleep(0.1)
        except:
            print("Could not write releases for " + i[i.rindex("/") + 1:])



def check_doc(link):
    # This function look for all the pom.xml and build.gradle int the project and keep their relative dir in a list
    # In case it finds a pom.xml or a build.gradle in the main directory is gonna return a list having two booleans,[contains pom, contains gradle], true in case it found it, false otherwise.

    i=1
    list=[[],[]]
    root= link
    link+= "/search?q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle&unscoped_q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle"
    page = requests.get(link)
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")
    while page.status_code== 200:
        for element in soup.find_all("a"):
            if re.search("/pom\.xml", element.get('href')):
                link1 = re.sub(".*/blob/([0-9A-Fa-f])*/", "", element.get("href"))
                if link1 not in list[0]:
                   list[0].append(link1)
            if re.search("/build\.gradle", element.get('href')):
                link2 = re.sub(".*/blob/([0-9A-Fa-f])*/", "", element.get("href"))
                if link2 not in list[1]:
                    list[1].append(link2)
        i += 1
        link = root + "/search?p="+ str(i) + "&q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle&unscoped_q=apache+filename%3Apom+extension%3Axml+OR+apache+filename%3Abuild+extension%3Agradle"
        page = requests.get(link)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
    bollist = [False, False]
    if "pom.xml" in list[0]:
        bollist[0] = True
    if "build.gradle" in list[1]:
        bollist[1] = True
    return bollist


def check_existence_on_github(directory, filename):
    # Given the directory, i.e. /apache/pulsar, and a filename, i.e. pom.xml, checks if that file exists (returns True).
    page = requests.get("https://github.com"+directory+"/blob/master/"+filename)
    return page.status_code!=404


def write_complete_timeline(bug_time = 14, filename = "ApacheGithubLinks.txt", include_release_date = True):
    # for each project in the file in the main directory (by default "ApacheGithubLinks.txt") writes per release in
    # the corresponding file (from the Releases folder) the number of dependencies directly before the release and
    # the number of bugs after release (by bug_time, by default 14 days, from Jira) into a line.
    content = file_to_stringlist(filename, "")
    for i in content:
        for j in (file_to_stringlist(i[8:] + ".txt", "Releases/")):
            dependencies = file_to_stringlist(i[8:] + ".txt", "Dependencies/")
            dependencies_all = file_to_stringlist(i[8:] + "_2.txt", "Dependencies/")
            for idx, k in enumerate(dependencies):
                best_date = date_normalization(k)
                if not date1_greater_date2(best_date, j[:10]):
                    l=-1
                    while True:
                        l=l-1
                        if k[l] == " " or l < -10:
                            break
                    numb_dependencies = str(k[l+1:])
                    numb_release = str(j[:10])
                    try:
                        numb_bugs = str(get_bugs_period("https://github.com" + i, j[:10], date_adder(j[:10], bug_time)))
                    except:
                        print("Invalid Jira request for bug number. Writing -1 instead.")
                        numb_bugs = str(-1)
                    temp_string = ""
                    if include_release_date:
                        temp_string = temp_string + numb_release + "::"
                    try:
                        write_to_txt(numb_dependencies + "::" + temp_string + numb_bugs + "::" + dependencies_all[idx], "Timelines/complete.txt")
                        print("Writing: " + numb_dependencies + "::" + temp_string + numb_bugs + "::" + dependencies_all[idx])
                        break
                    except:
                        print("Can't write to txt: Index out of range or other error. Writing NONE instead.")
                        write_to_txt(numb_dependencies + "::" + temp_string + numb_bugs + "::" + "NONE", "Timelines/complete.txt")
                        break

def clean_up(file, folder):
    temp_list = file_to_stringlist(file, folder)
    for i in temp_list:
        if i[i.rindex("::")-2] != "-" and i[0].isdigit():
            write_to_txt(i, "output_clean.txt")





