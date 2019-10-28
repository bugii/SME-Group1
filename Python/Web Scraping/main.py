import requests
import urllib.request
from bs4 import BeautifulSoup
import functions

# I installed the requests library and bs4 library via the following command line input: "py -m pip install bs4" and
# "py -m pip install requests"; alternatively, you can try "pip install bs4" and "pip install requests".

# This is just a test. It downloads my homework from 2 years ago into a local repo; then creates a log of this current
# project; still trying to figure out how to change the directory to access the history/log of my homework.

functions.command_window("git", "status")
functions.command_window("git", "clone", "https://github.com/chfaes/Assignment-6.git", "-b", "master")
output = functions.command_window("git", "log", "--stat")
print("hello world")
print(str(output))

# Here we scan the complete https://repo.maven.apache.org/maven2/ and copy all the .pom links into a txt in the main
# directory.

"""
open('output.txt', 'w').close() # Clears the output file at the beginning.
functions.deepscan_url('https://repo.maven.apache.org/maven2/')

# We now want to copy the contents (all the lines, the urls) from output.txt into a list.

with open("output.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

# Next, we create another txt, this time containing the dependencies.

open('dependencies.txt', 'w').close() # Clears the dependencies file at the beginning.
for x in content:
    functions.dependencies_from_pom_url(x)
"""