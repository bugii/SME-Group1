# **Introduction** 

## What is Gradle?

Gradle is an open-source build-automation system that builds upon the concepts of Apache Ant and Apache Maven and introduces a Groovy-based domain-specific language (DSL) instead of the XML form used by Apache Maven for declaring the project configuration.[2] Gradle uses a directed acyclic graph ("DAG") to determine the order in which tasks can be run.

Gradle was designed for multi-project builds, which can grow to be quite large. It supports incremental builds by intelligently determining which parts of the build tree are up to date; any task dependent only on those parts does not need to be re-executed.

Both Maven and Gradle are able to cache dependencies locally and download them in parallel. As a library consumer, Maven allows one to override a dependency, but only by version. Gradle provides customizable dependency selection and substitution rules that can be declared once and handle unwanted dependencies project-wide.

### What is dependency management?

Software projects rarely work in isolation. Projects relies on reusable functionality in the form of libraries or is divided in individual components to compose a modularized system. DM is a technique for declaring, resolving and using dependencies requiered by the project in an automated way. 

Gradle has build-in support for dependency management. A developer can declare dependecies for different scopes (just for compilation of code or fot executing test). In Gradle, the scope of a dependency is called a configuration.

tipically dependencies come in form of MODULES. You need to tell Gradle where to find the modules so they can be consume by the build. The place we keep the modules is call REPOSITORY. By declaring repositories for a build, Gradle will know how to find and retireve modules. ##Repositories (local directory or remote repository).

## Dependency resolution 

At runtime, Gradle will locate the declared dependencies if needed for operating a specific task. The dependencies might need to be downloaded from a remote repository, retrieved from a local directory or requires another project to be built in a multi-project setting. 

Once resolved, the resolution mechanism stores the underlying files of a dependency in a local cache --> dependency cache. Future builds will reuse the files stored in the cache to avoid network calls. 

Modules can provide addictional metadata as the coordinates for finding it in a repository, information about the project... A module can define that other modules are needed for it to work properly. --> Transitive dependencies. 

Gradle provide tools to visualize, navigate and analyze the dependency graph of a project either with the help of a build scan or built-in tasks.

### How dependency resolution works (brief outline of how this work)

1.Given a required dependency, Gradle attempts to resolve the dependency by searching for the module the dependency points at. Each repository is inspected in order. Gradle looks for metadata files describing the module (module, .pom or ivy.xml file) or directly for artifact files. 

  *If the dependency is declared as a dynamic version, Gradle will resolve this to the highest available concrete version in the repository. For Maven repositories, this is done using the maven-metadata.xml file, while for Ivy repositories this is done by directory listing.
  
   *If the module metadata is a POM file that has a parent POM declared, Gradle will recusively attempt to resolve each of the parent modules for the POM.
    
2. Once each repository has been inspected for the module, Gradle will choose the best one to use by using the following criteria: 
  *For a dynamic version, a 'higher' concrete version is preferred over a 'lower' version.
  
  *Modules declared by a module metadata file (.module, .pom or ivy.xml file) are preferred over modules that have an artifact file only.
  
  *Modules from earlier repositories are preferred over modules in later repositories.
  
  *When the dependency is declared by a concrete version and a module metadata file is found in a repository, there is no need to continue searching later repositories and the remainder of the process is short-circuited.

3. All of the artifacts for the module are then requested from the same repository that was chosen in the process above.






