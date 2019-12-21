# An Empirical Investigation on the Evolution of Project Dependencies in Modern Software Systems

### Introduction

Dependencies are a big part of current software as building everything from scratch is very infeasible and not efficient. The evolution of dependencies is an interesting topic to analyze as it gives you a better understanding of the software architecture and possibly makes the software maintenance progress easier. In our project we are analyzing dependencies in the apache echosystem. Because many projects tend to move to the cloud, ways to analyze dependencies change. Therefore, also projects using the microservice architecture are analyzed in terms of their dependencies. Last but not least we are comparing the original microservice architecture to the acutal result of the implementation with the help of existing visualization tools.

### Goals

The goal of this is project is to investigate how dependencies evolve in modern ecosystems and affect their respective projects with a focus on the apache ecosystem, microservices projects, and visualization. We came up with the following research questions:

- RQ1:  How does the usage of dependencies correlate with code destabilization, as measured by the amount of issues and bugs after a project release? Since dependencies are often added to projects with a care free attitude, it seems important to understand how to add dependencies responsibly.
- RQ2: Do newer (by looking at latest commit) projects have more and smaller (in terms of megabyte of the underlying container) microservices? This is important to analyze since the main idea of the microservice approach is to have multiple small services. Observing the opposite could indicate that the architecture should be split up more and that there is a trend moving away from a true microservices architecture.
- RQ3: With increasing number of microservices in a project, how do the dependencies between them evolve? With an increase in dependencies between different microservices, updates should be made more carefully because other services depend on it. Also, it would underline the importance of visualisation tools (RQ4) in case there is an exponential relationship between the two, because remembering the real underlying architecture becomes almost impossible.
- RQ4: Is it possible to deduct from its dependencies the architecture of a project with a microservice architectural style using a visualization tool?

### Part 1 (RQ 1): Traditional Ecosystems

#### Introduction to Maven and Gradle

The Gradle Build Tool and Apache Maven are some of the more well-known software project management tools. They are, amongst other things, managing project dependencies. Gradle stores its dependencies in a file named "build.gradle" in the main directory; Maven projects have a "pom.xml" file. Both files can be analyzed in order to extract the number of dependencies as well as several more details like version numbers. In our project, we focus exclusively on projects that have one of these files in the main directory.

#### Hypotheses and Methodology

In order to answer RQ1, we intended to analyze Maven and Gradle projects by fetching the number of dependencies over the project's respective lifespan, cross-match the dependencies with the releases of such a project and then fetch the number of bugs in the weeks following the release. We hypothesize that having more dependencies results in more bugs as well; and since dependencies are often added to projects with a care-free attitude, it seems important to understand how to add dependencies responsibly.

We proceeded to write a python script that would allow us to automatically perform the aforementioned tasks by scanning the Apache ecosystem on Github. Specifically, our script works the following way:

Identification of suitable projects -> Cloning into a local repository -> Creation of dependency timeline via checkout of the dependency file -> Creation of release timeline -> Fetching of bug data -> Merge available data into a single .txt file -> Clean-up of data, clearing folders

#### Data mining

The identification of suitable projects is done via repeated Github requests. Through string slicing, a list of projects is compiled from the response and then pre-checked for the existence of either a "build.gradle" or a "pom.xml" in its main directory.

The script clones the Github projects one by one via command line calls. Before cloning, the folder is being cleared such that disk space does not run out in the process.

Via repeated git checkout commands, the dependency files or each project are sequentially downloaded, and their dependencies stored (with their dates included).

All releases of a project are fetched from Github via URL request and subsequent string analysis.

Based on the releases, requests are sent to Jira, an online project management tool. The number of bug entries is fetched, as per standard the number of bugs up to two weeks after the release date. Note that not all projects have associated Jira pages and therefor, our script fails to provide a bug number.

From the available data up to this point, a cumulative output is created and written into a .txt file. This output may be further analyzed and interpreted by our script (to gain more information about the type of dependencies per project) or written into excel files for further processing.

#### Results

Of the first 100 repositories, 37 were usable in terms of dependency files, releases on Github and bug reports on Jira. A total of 344 data tuples of the format "dependencies, release_date, bugs" were extracted and plotted. Figure 1 shows all tuples sorted by the number of dependencies (highest first), including linear trend lines. Figure 2 shows all tuples cumulated over time. Note that for presentation purposes, the time scale is not linear; it extends from 2014 to 2019 with comparatively few data points in the first years. Figures 3 and 4 show 145 data tuples each, this time dependencies on Apache projects (Figure 3) or Apache commons projects (Figure 4).

<img alt="Duration" src="Python/Web Scraping/Figures/Figure1.png" width="600" />
<img alt="Duration" src="Python/Web Scraping/Figures/Figure2.png" width="600" />
<img alt="Duration" src="Python/Web Scraping/Figures/Figure3.png" width="600" />
<img alt="Duration" src="Python/Web Scraping/Figures/Figure4.png" width="600" />

#### Discussion

Given Figure 1, it appears that the number of dependencies prior to a release does not affect the number of bugs in a 2-week time span after said release. A linear trend might become more obvious with more data points, but given that the trend line is almost horizontal, we are confident in saying that dependencies do not lead to bugs. Therefor, RQ1 can be answered simply: no correlation between dependencies and bugs could be detected.

Regarding Figure 2, it would appear that the number of dependencies and bugs grow over time. Given that the time frame extends over 5 years in this particular figure and the datapoints represent cumulated numbers, we interpret this as the Apache ecosystem growing in size and numbers, which would obviously lead to more dependencies and bugs as a result. It is important to note that Figure 2 does not imply a link between dependencies and bugs, since the number of active projects in the ecosystem confounds the results.

Figure 3 suggests that a larger number of dependencies on Apache projects correlates with more bugs after a project release. However, upon closer inspection, it turned out that the outliers between data points 40 and 60 (x-Axis) are all from the same project (flink) which has a considerably higher bug count than the other projects and distorts the data. We therefor assume that dependencies on Apache projects are no more or less likely to cause bugs than other dependency types.

The same holds true for Figure 4: Despite a visible correlation between bugs and dependencies on Apache commons projects, flink once more is responsible for the outliers. We assume that Apache commons projects do not correlate disproportionately with bugs.

It is worth noting that Figures 3 and 4 use a smaller set of data points (145 compared to 344). In order to further clarify the situation, especially with regards to outliers, a larger data set might be helpful.


### Part 2 (RQ 2 and 3): Microservices

#### Introduction to Docker and docker compose files

Docker is a tool to create and run so-called containers. Containers are self-contained, standalone bundles of software which are run in a closed a environment. Often Docker is compared to a Virtual Machine (VM). While they do have some similarities, they are implemented quite differently: Instead of allocating resources to a Virtual Machine and not sharing those across other VMs, Docker containers run in the same operating system as its host. This way different containers can have access to a lot of the operating system resources, which leads to very lightweight containers. Despite being small in size, containers come with all they need: the app itself and all the required binaries and libraries. As a result, every computer with Docker installed is able to run those containers without any further configuration. This technology facilitates the deployment process drastically since it is ensured that containers run on every Docker client regardless of their underlying architecture.

To take it a step further, consider a system with many different containers and maybe even multiple instances of all of them, running them all manually can be very tedious. This is where a docker compose file comes into play. It allows to give all the required instructions in a single file. This file can be run with a single command and starts up all the required containers automatically. 

Docker compose files contain a lot of valuable information and is the main resource for this section.

#### Methodology
##### Fetching projects

With the help of a python script we query the Github API for repositories containing docker-compose.yml files in their
root directory. This makes further analysis easier since you don't have to search for the file inside the repository. The following parameters were used for the code search request:

```python
sizes = ["1..2000", "2001..4000", "4001..6000", "6001..8000", "8001..10000"]

res = session.get('https://api.github.com/search/code',
                              params={'q': 'path:/ filename:docker-compose.yml size:' + size,
                                      'sort': 'stars',
                                      'order': 'desc',
                                      'per_page': per_page,
                                      'page': page})
```

The Github API currently has a limit of 1000 repositories. In order to get more than 1000 results, we used a little trick:
By splitting up the search into multiple size intervals results in two benefits. First, we are able to have more results, secondly,
you automatically obtain a good mixture of smaller and bigger projects.

From this response the repository urls can be extracted and fetched in the next step. 

That way, most of the important data for later was extracted from the repository responses. The following data was obtained:

1. Project name
2. Creation & last updated date, which were then used to calculate the duration of the project
3. Main language of the project
4. Number of contributors to the project
5. Number of commits in the project (excluding merge commits)

Those metrics were stored in pickle files, which is the python way of storing objects to disk. Also, in order to be able to analyze the microservices of each project, the content of the repositories have to be looked at. 

##### Analyzing microservices

It should be pointed out that there are two possible ways of analyzing dependencies for projects with a microservices architecture, namely either *statically* or *dynamically*. While the first one analyzes static configuration files, such as docker compose for instance, the latter looks at the system at runtime. Since in this project we performed a static analyis, it would be very interesting to see how a dynamic approach compares to our results.

After having downloaded all the latest releases in the previous part, the goal was to additionally get the following information for all of them:

1. Number of microservices
2. Size of each microservice
3. Dependencies between microservices

Here, we would like to point out that the size of a project does not necessarily correcty describe the project complexity because certain images might be simply bigger because of the underlying technology, not the code itself. In case of a dynamic analyis approach, there could be some other interesting indicators for complexity, such as number of API calls between the services for example. 

In order to get the actual size of all the microservices for each project, the docker image directory was changed to an external hard drive. That way we could prevent our machine from running out of memory and we did not have to delete all the images after each project, which would have been very inefficient in case of docker (because internally it uses a hashing mechanism for efficien storage of docker images). On Ubuntu, the default location for storing docker images can be changed by creating the following file: /etc/docker/deamon.json. Add the following code snippet to the file, where "/mnt/hdd/docker" is replaced by your desired destination path:

```json
{
    "data-root": "/mnt/hdd/docker"
}
```

Note however, that for the amount of projects we analyzed, 2TB of storage was not enough and thus we had to clean up our docker images after some time in order to be able to continue the analysis.

Our script runs an analysis on the docker-compose.yml file for each project. This file stores all the relevant information we need. What is most important in our case are the fields "image", "build", and "depends_on" inside "services". A complete specification of the docker-compose file can be found [here](https://docs.docker.com/compose/). An example of such a file looks like this:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
    - "5000:5000"
    volumes:
    - .:/code
    - logvolume01:/var/log
    links:
    - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```

To obtain the correct image size, we distinguish the following cases:

1. Only "image" field is present: Pull the image
2. "build" field is present, either with or without subfields: build the image 
   1. Subfields: Build the image at location specified in "context". If "dockerfile" present, append the name to the path, otherwise the default "Dockerfile" is used
   2. No subfields: Build the image located at "build"

During this process, one can encounter many different errors. We found the following reasons for errors that occurred in our dataset:
1. Private image -> cannot be download
2. Error during building
3. Image cannot be found
4. Variables inside path names (variables are specified in '{}')
5. No build or image was specified for a microservice
6. Could not download image (HTTP Error)

In all of the above cases, a value of -1 was returned from the get_service_size() function. Whenever there was a -1 response for at least one microservice in a project, the entire project was not considered for further analysis and was therefore deleted. Consequently, we only considered project with none of the above errors.

For building and pulling images [docker-py](https://github.com/docker/docker-py), which is a python wrapper for docker, was used. Both the pull and build functions return images which in turn have a size attribute. For each service listed, it was stored inside the pickled project object (inside the microservices field)  with the name and its size. Therefore, the number of microservices can be easily obtained by checking the length of this list.

To get the dependencies between microservices, we counted all the entries in "depends_on" fields inside each microservice. It should be noted that these dependencies are of static nature. Further research could also analyze a more dynamic view of the dependencies and compare them to our findings. 

#### Data
Out of the initially 6000 downloaded Github repositories, only 1626 were completely buildable, that is without any error occuring on any of the underlying microservices. This exteremely low ratio 27.1% was however expected from our side since similar results have been found for Helm Charts.

For each project there was a pickled python object stored onto disk. The project object has the following properties:

| Field Name | Description | Type |
|------------|-------------|------|
| name | github name of the project | string |
| url | api url to the repository | string |
| created | date of the creation | datetime |
| last_updated | date of the last update | datetime |
| microservices | List of all microservices in the project | list of dictionaries with fields: 'name' and 'size' |
| depends_on | Number of dependencies of all microservices combined | int |  
| language | Main language used in the project | string |
| contributors | Number of contributors to the project | int |
| commits | Number of commits in the project (not counting merge commits) | int |

#### Results

The following plots are only a selection of all the created ones. All plots can be found [here](Python/Docker/results).

In order to answer RQ2, we looked at the "last updated" timestamp of the Github repository. We found that there is only a slight trend towards newer projects having more microservices. However, there are more outliers on the upper bound in the year 2019. In that case, analyzing more projects could help to better understand whether those projects really are outliers. It should be noted that the plots for project size, average container size, and number of dependencies yield very similar result.

<img alt="Last updated" src="Python/Docker compose/results/last_updated_micro.png" width="400" />

A bit clearer results could be obtained by controlling for language: we observed that java had the most number of microservices and dependencies between microservices compared to all other chosen languages. We assume that this is the case because java is an established language and therefore often used in enterprise. Surprisingly, the same argument cannot be used for C#, which we expected to be used largely in enterprise as well. It should be noted,that even though Java was found to have the most dependencies among the other languages, all dependencies were treated as the same, thus no dependency types were dinstinguished. 

<img alt="Last updated lang" src="Python/Docker compose/results/last_updated_lang.png" width="400" />

In addition to the "last updated" timestamp, the same analysis was performed for the project duration . Intuitively, it makes a lot of sense that projects with longer developement durations tend to have more microservices and dependencies. Also, the size of both the entire project and the average container size grows with longer project duration. The following figure illustrates the relationship between the average container size and the project duration. Very similar findings were found for the other 3 values (microservices, dependencies and total size).

<img alt="Duration average size" src="Python/Docker compose/results/duration_avg_size.png" width="400" />

Also, contributors were analysed, however nothing interesting resulted. Looking at a measure that describes effort, such as commits, was more interesting. It seems that there is a trend for the project size to increase whereas dependencies remain more or less constant. It seems reasonable to us that dependencies are not dependent on the number of commits. The project architecture is often times defined in an early stage and later commits mainly add functionality to existing services. 

<img alt="Duration commits" src="Python/Docker compose/results/commits_size_deps.png" width="400" />

To answer RQ3, the following plot illustrates the relationship between the number of microservices in a project and the total dependencies between them. Against our expectations, there seems to be a more or less linear relationship between the two factors, if any. We expected the relationship to be exponential.

<img alt="Duration" src="Python/Docker compose/results/mirco_vs_deps.png" width="400" />

### Part 3 (RQ 4): Visualization

#### Introduction to MicroDepGraph

For answering RQ4 we focused on using the tool MicroDepGraph, this tool when used on a java project based on docker will present an output representing the architecture of the project based on the dependencies the project has.

#### Methodology

##### Searching for projects

The first hard task we encountered was to find projects that we could run on the tool and that had a propossed architecture by the developer of the project so we could compare the tool output.

For this we used [the following query](https://github.com/search?l=Java&p=14&q=java+docker+microservices&type=Repositories) which presented us 14 pages of github projects, we manually analyzed the repositories in order to find some information related to the architecture of the project.

With the propossed way to find projects we finally ended having 17 projects that we could run on the tool and had information related to the architecture. But for this projects we only could review 12 of them cause 5 gave an empty graph as output and another one is not useful at all cause it has too many nodes and relations.

##### Analysing/Reviewing

To analyze the data we focused on the information the graph presented (nodes,relations,names).

Since we want to know if the tool output is useful for understanding the architecture we asked computer science related people (mostly students) and we presented this 
> Hi, do you know about computer science? Then we need your help for a university project. 
>We are testing a tool that when used on a microservice based java project gives an image showing what is supposed to be the architecture of it based on its dependencies.
>For this test we are going to show you 12 pairs of images and ask you how similar/ how representative (from 1 to 5) is the second image (the tool result) from the first (proposed architecture).
>with the 12 pairs of images (the propossed architecture and the output of the tool)

#### Data

The analysis of the data gave us this result:

<img alt="Output analyzed" src="/MicroDepGraph/Data analysis.PNG" width="800" />

From this data we created the followign chart that shows the relation between the nodes and links from the original architecture and the tool output:

<img alt="Ratios chart" src="/MicroDepGraph/Data analysis ratios.PNG" width="500" />

And the reviews provided us this 1 to 5 based average chart:

<img alt="Reviews average" src="/MicroDepGraph/Average chart.png" width="500" />


#### Results

##### Data results

So to answer the question we want to know if the tool is useful to understand the architecture of the project, for this we will mostly base our results on the review part, because the main point is if people can understand the tool output as the architecture. For this we got 3 categories based on the results of the interviews: 

1. The projects that have an average below 3 are the not useful projects, this projects when analyzed with the tool we don't get an output that can help understand the architecture of the project
2. The projects with average between 3 and 4 we understand as projects that have an useful output on the tool but we don't fully get the architecture if we don't look at the propossed one, being this the "help to understand" projects.
3. The projects with an average over 4 we understand have an output good enough to understand the project architecture by itself without the need to look at the propossed architecture. This are the "useful" ones.

Based on this the 17 projects we analyzed (including the not reviewed as not useful) would give this results: (1) 

| Category | Number of projects |
|-----------|--------------------|
| Not useful | 10 |
| Help to understand | 4 |
| Useful | 3 |

(1) We included the project lelylan in the Useful category even though it has a average that would categorize it as "Not useful" cause this average is based on the project being similar to the original architecture, but in this case the output of the tool is much more detailed and useful than the original propossed

##### Comments before final results

Maybe the tool would have worked on more projects and gave useful output, but the amount of projects we could analyze was quite small and we will base the results on the data that we could gather.

##### Final Results

So, based on the results given we can say that at this moment at least with this tool it is not possible for most projects to have an architecture output by itself. Though for some projects we can have it and for some others it can be useful to understand the basics of the architecture.




