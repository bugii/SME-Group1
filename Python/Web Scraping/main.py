import requests
import urllib.request
from bs4 import BeautifulSoup
import functions

# I installed the requests library and bs4 library via the following command line input: "py -m pip install bs4" and
# "py -m pip install requests"; alternatively, you can try "pip install bs4" and "pip install requests".

# This is just a test. It downloads my homework from 2 years ago into a local repo, then creates a log.

output = functions.command_window("git", "status")
#print(str(output))
functions.command_window("cwd=Repositories", "git", "clone", "https://github.com/chfaes/Assignment-6.git", "-b", "master")
output = functions.command_window("git", "log", "--stat")
#print(str(output))
output = functions.command_window("dir")
#print(str(output))
output = functions.command_window("cwd=Repositories/Assignment-6", "git", "log", "--stat")
print(output)
print(functions.file_to_stringlist("customer.py", "Repositories/Assignment-6/"))

# Here we scan the complete https://repo.maven.apache.org/maven2/ and copy all the .pom links into a txt in the main
# directory.

"""
open('output.txt', 'w').close() # Clears the output file at the beginning.
functions.deepscan_url('https://repo.maven.apache.org/maven2/')

# We now want to copy the contents (all the lines, the urls) from output.txt into a list.

content = functions.file_to_stringlist("output.txt")

# Next, we create another txt, this time containing the dependencies.

open('dependencies.txt', 'w').close() # Clears the dependencies file at the beginning.
for x in content:
    functions.dependencies_from_pom_url(x)
"""