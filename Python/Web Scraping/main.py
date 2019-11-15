import functions

# I installed the requests library and bs4 library via the following command line input: "py -m pip install bs4" and
# "py -m pip install requests"; alternatively, you can try "pip install bs4" and "pip install requests".

# First, clear up all files and folders.
functions.clear_main(["f:Dependencies", "f:Logs", "f:Releases", "f:Repositories", "ApacheGithubLinks.txt"])

# Here we scan Github for all Apache Source Projects.
functions.generate_Apache_link_list(1)

# Goes throught the txt, clones all projects one by one and writes the dependency time line into "Dependencies"
functions.write_dependency_timelines("ApacheGithubLinks.txt", "")

# Goes through the txt, writes the release time lines into "Releases"
functions.write_release_timelines("ApacheGithubLinks.txt", "")

# To Do: Obtain the number of bugs following a release.
#print(functions.get_bugs_period("https://github.com/apache/incubator", "2018-02-07", "2019-11-12"))