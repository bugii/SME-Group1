# An Empirical Investigation on the Evoultion of Project Dependencies in Modern Software Systems

### Part 1: Traditional Ecosystems

#### What is Gradle?

Gradle is an open-source build-automation system that builds upon the concepts of Apache Ant and Apache Maven and introduces a Groovy-based domain-specific language (DSL) instead of the XML form used by Apache Maven for declaring the project configuration.[2] Gradle uses a directed acyclic graph ("DAG") to determine the order in which tasks can be run.

Gradle was designed for multi-project builds, which can grow to be quite large. It supports incremental builds by intelligently determining which parts of the build tree are up to date; any task dependent only on those parts does not need to be re-executed.

Both Maven and Gradle are able to cache dependencies locally and download them in parallel. As a library consumer, Maven allows one to override a dependency, but only by version. Gradle provides customizable dependency selection and substitution rules that can be declared once and handle unwanted dependencies project-wide.

#### What is dependency management?

Software projects rarely work in isolation. Projects relies on reusable functionality in the form of libraries or is divided in individual components to compose a modularized system. DM is a technique for declaring, resolving and using dependencies requiered by the project in an automated way. 

Gradle has build-in support for dependency management. A developer can declare dependecies for different scopes (just for compilation of code or fot executing test). In Gradle, the scope of a dependency is called a configuration.

tipically dependencies come in form of MODULES. You need to tell Gradle where to find the modules so they can be consume by the build. The place we keep the modules is call REPOSITORY. By declaring repositories for a build, Gradle will know how to find and retireve modules. ##Repositories (local directory or remote repository).

#### Dependency resolution 

At runtime, Gradle will locate the declared dependencies if needed for operating a specific task. The dependencies might need to be downloaded from a remote repository, retrieved from a local directory or requires another project to be built in a multi-project setting. 

Once resolved, the resolution mechanism stores the underlying files of a dependency in a local cache --> dependency cache. Future builds will reuse the files stored in the cache to avoid network calls. 

Modules can provide addictional metadata as the coordinates for finding it in a repository, information about the project... A module can define that other modules are needed for it to work properly. --> Transitive dependencies. 

Gradle provide tools to visualize, navigate and analyze the dependency graph of a project either with the help of a build scan or built-in tasks.

#### How dependency resolution works (brief outline of how this work)

1.Given a required dependency, Gradle attempts to resolve the dependency by searching for the module the dependency points at. Each repository is inspected in order. Gradle looks for metadata files describing the module (module, .pom or ivy.xml file) or directly for artifact files. 

  *If the dependency is declared as a dynamic version, Gradle will resolve this to the highest available concrete version in the repository. For Maven repositories, this is done using the maven-metadata.xml file, while for Ivy repositories this is done by directory listing.
  
  *If the module metadata is a POM file that has a parent POM declared, Gradle will recusively attempt to resolve each of the parent modules for the POM.
    
2. Once each repository has been inspected for the module, Gradle will choose the best one to use by using the following criteria: 
  *For a dynamic version, a 'higher' concrete version is preferred over a 'lower' version.
  
  *Modules declared by a module metadata file (.module, .pom or ivy.xml file) are preferred over modules that have an artifact file only.
  
  *Modules from earlier repositories are preferred over modules in later repositories.
  
  *When the dependency is declared by a concrete version and a module metadata file is found in a repository, there is no need to continue searching later repositories and the remainder of the process is short-circuited.

3. All of the artifacts for the module are then requested from the same repository that was chosen in the process above.

#### Dependencies in Apache projects

In order to find out whether dependencies destabilize code, we built a tool to analyze Apache projects on Github.
This tool, a python script, simply scans all Apache source projects for pom.xml (contain the dependencies of Maven projects) or build.gradle (Gradle projects) files.
It then clones the repositories one by one, checks out all dependency files sequentially and stores the number of dependencies (including their date) in a text file in the Dependencies folder.
Afterwards, it extracts all release dates and, based on those dates, sends a request to Jira to obtain the number of bugs following that release in a specified time window (i.e. two weeks).
The raw data (dependencies, release date and bug count) is then written into a text file in the Timelines folder for further use.

### Part 2: Microservices

#### Introduction to Docker and docker compose files

An example of a containerised application is a docker image of a MySQL Server. 
With the help of a Docker Container this application runs in a closed environment, 
much like a Virtual Machine, yet it is implemented completely differently.
Instead of allocating resources to each Virtual Machine and not sharing those across others,
Docker containers run in the same operating system as its host. This way different containers can have access
to a lot of the operating system resources, which leads to very lightweight containers.

Image a system with many different containers, running them all manually can be very tedious. This is where a docker compose file
comes into play. It allows to give all the required instructions in a single file. This file can be run with a single command
and starts up all the required containers automatically. 

Docker compose files contain a lot of valuable information and is the main resource for this section.

#### Getting data

Note: Before running the script make sure that you have all the dependencies installed. Do:

```python
pip install -r Python/Docker/requirements.txt
```

The data can be fetched using the following command:

```shell script
python Python/Docker/repo_fetching.py
```

Note, that you change the API_KEY variable to one of your own Github API keys before running the script and that
you have all dependencies installed specified in the requirements.txt file.

In a bit more detail, this script queries the Github API for repositories containing docker-compose.yml files in their
root directory. This makes further analysis easier since you don't have to search for the file inside the repository.
Furthermore, out of all the matching repositories, only the first 1000 were downloaded and will be analyzed in the next
steps. 

```python
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

That way, most of the important data for later was
extracted from the repository responses. The following data was extracted:

1. Project name
1. Creation & last updated date, which were then used to calculate the duration of the project
2. Main language of the project
3. Number of contributors to the project

Those metrics were stored in pickle files, which is the python way of storing objects to disk.
Also, in order to be able to analyze the microservices of each project, the content of the repositories have to be looked at.
The first step included downloading all the latest releases of the projects.

### Obtaining information about microservices

The goal was to get the following information for all projects:
1. Number of microservices
2. Size of each microservice

In order to get the actual size of all the microservices for each project, the docker image directory was changed to an
external hard drive. That way we could prevent our machine from running out of memory and not delete all the images
after each project, which would have been very inefficient in case of docker. On Ubuntu, the default location for storing
docker images can be changed by creating the following file:
/etc/docker/deamon.json. Put into the file:

```json
{
    "data-root": "/mnt/hdd/docker"
}
```

After that, we ran the analysis with the following command:

```shell script
python Python/Docker/analysis.py
```

This script runs an analysis on the docker-compose.yml file for each project. This file stores all the relevant information.
What is most important in our case, are the fields "image", "build", and "depends_on" inside "services". A complete specification of the docker-compose file can be
found [here](https://docs.docker.com/compose/). An example of such a file looks like this:

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

1. If the file does not list any services: microservices = 0, size = -1
2. Only "image" field is present: Pull the image
3. "build" field is present, either with or without subfields: build the image 
   1. Subfields: Build the image at location specified in "context". If "dockerfile" present, append the name to the path, otherwise the default "Dockerfile" is used
   2. No subfields: Build the image located at "build"

For building and pulling images [docker-py](https://github.com/docker/docker-py) was used. Both the pull and build functions return
images which have a size attribute. For each service listed, it was stored inside the pickled project object (inside the microservices list) 
with the name and its size. Therefore the number of microservices can be easily obtained by checking the length of this list.

To get the dependencies between microservices, we counted all the entries in "depends_on" fields inside each microservice. It should be noted
that these dependencies are of static nature.

Note: In order to be able to run the script, it may be required to allow docker to run commands as a non-root user. In
Linux this is done via the following commands:

```shell script
sudo groupadd docker
sudo usermod -aG docker $USER
```

### Results

Plots and stuff

### Part 3: Visualization

#### Requirements

Java jdk8 or higher.

#### How to use

1. Get the tool from [MicroDepGraph](https://github.com/clowee/MicroDepGraph) and the jar file [here](https://wetransfer.com/downloads/2f0d080c8e9d09c814416a1f33d2cf6c20191011064223/3bcf007c7411057b72491349f8fa6c1a20191011064223/75c663).
2. Get the java project developed with a microservice architectural style based on docker configuration to your local drive.
3. Execute : java -jar microservices.comm.pattern.check-1.0-SNAPSHOT-jar-with-dependencies.jar  <absolute_path_of_the_cloned_repository> <project_name>

#### Output

It gives output in 2 folders:

* in ../neo4jData/<project_name> a neo4j graph database
* in ../<project_name> a DOT file describing the graph, a graphml file and a svg file.

#### Dataset

There are a list of projects analyzed on the Microservice Dataset repository [view](https://github.com/clowee/MicroserviceDataset)


