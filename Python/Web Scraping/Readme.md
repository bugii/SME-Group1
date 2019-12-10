# How to use the script

In order to use the script, the following libraries have to be installed:

- requests
- bs4
- openpyxl

Depending on the python version, one of the following commands can be used for the installation:

```shell script
py -m pip install requests
```

or, alternatively

```shell script
pip install requests
```

Our script can be operated from "main.py". Open the file in an IDE of your choice. The following functions (from "functions.py") may be used:

| Command | Description | Arguments |
|------------|-------------|------|
| clear_main | Erases files and clears folders | List with file and folder names |
| generate_Apache_link_list | Creates a .txt file with links to Apache projects on Github | Integer designating the number of pages to be fetched |
| write_dependency_timelines | Clones all repositories one by one and writes their dependencies into a .txt file in the dependency folder | Filename and directory of the Apache link .txt, the maximum number of repositories to be downloaded and a boolean designating whether the dependencies should be spelled out |
| write_release_timelines | Fetches the releases for each project in the Apache link .txt | Filename and directory |
| write_complete_timeline | Gathers all available data into a single file and adds the number of bugs found on Jira | Filename, time period for which to fetch the number of bugs per release (set to 14 days by default) and whether or not to include the release dates in the output file |
| clean_up | Cleans a .txt file such that only complete (as in: contain a dependency and a bug number) lines remain | Filename, directory and a boolean designating whether the project names should be included |
| dependency_interpreter | For a given file with spelled out dependencies, fetches the number of dependencies with certain properties (see comments in "functions.py") | Filename and directory |
| convert_to_excel | Converts a given file to excel | Filename and boolean as to whether the date should be converted to an integer for easier sorting |
| median_calc | Supplementary function to calculate the median of the number of dependencies over the lifespan of a project | Filename |
