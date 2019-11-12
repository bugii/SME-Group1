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

#### Data 

Note: Before running the script make sure that you have all the dependencies installed. Do:

```python
pip install -r Python/Docker/requirements.txt
```

The data can be fetched using the following command:

```
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
                  params={'q': 'path:/ filename:docker-compose.yml',
                          'sort': 'stars',
                          'order': 'desc',
                          'per_page': '100',
                          'page': 1 })
```

This request is sent for all as many pages as wished, 10 times in our case.
From this response the repository urls can be extracted and fetched in the next step. Downloading all the latest releases and
extracting the last-updated date are then achieved.

In order to get the actual size of all the microservices for each project, the docker image directory was changed to an
external hard drive. That way we could prevent our machine from running out of memory and not delete all the images
after each project, which would have been very inefficient in case of docker. For Ubuntu, create a file inside:
/etc/docker/deamon.json. Put into the file:

```json
{
    "data-root": "/mnt/hdd/docker"
}
```

When it comes to getting the size of the images, the following cases have been distinguished:
1. only "image" field
2. only "build" field, either with or without subfields: build the image at the specified location. 
   If it has subfields: build the image at location specified in "context". If "dockerfile" present, append the name to the path,
   otherwise default to Dockerfile.
3. "image" and "build": build as before, image is just the name
4. If field contains variables: ignore
5. If does not have any services: ignore 

Note: In order to be able to run the script, it may be required to allow docker to run commands as a non-root user. In
Linux this is done via the following commands:

```python
sudo groupadd docker
sudo usermod -aG docker $USER
```

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


