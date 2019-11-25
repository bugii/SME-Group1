import functions

# I installed the requests library and bs4 library via the following command line input: "py -m pip install bs4" and
# "py -m pip install requests"; alternatively, you can try "pip install bs4" and "pip install requests".

# First, clear up all files and folders.
# If you want to clear the output files, add "output_clean.txt" and "output_interpreted.txt" to the list.
#functions.clear_main(["f:Dependencies", "f:Logs", "f:Releases", "f:Repositories", "f:Timelines", "ApacheGithubLinks.txt"])

# Here we scan Github for all Apache Source Projects.
#functions.generate_Apache_link_list(1)

# Goes through the txt, clones all projects one by one and writes the dependency time line into "Dependencies"
#functions.write_dependency_timelines("ApacheGithubLinks.txt", "", MaxNumberOfClones=8)

# Goes through the txt, writes the release time lines into "Releases"
#functions.write_release_timelines("ApacheGithubLinks.txt", "")

# Puts together a time line, consisting of the project names, the releases, the preceding number of dependencies
# and the following bugs
#functions.write_complete_timeline(include_release_date=True)

# Clean-up of complete.txt in the Timelines folder; outputs a "output_clean.txt" in the main directory.
#functions.clean_up("complete.txt", "Timelines/")

# Additional information extraction. In the end, the output file is named "output_interpreted.txt" and has (so far)
# the following format: 10:5:3::2019-11-19::5:dependency1,dependency2...dependency10
# Interpretation: 10 dependencies, 5 are from Apache, 3 are Apache commons for the release from 2019-11-19; there
# were 5 bugs afterwards (bug_time, specified in write_complete_timeline); and the complete list of dependencies,
# separated by comma.
functions.dependency_interpreter("output_clean.txt", "")
