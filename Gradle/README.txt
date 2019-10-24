Introduction 

#What is Gradle?# 

Gradle is an open-source build-automation system that builds upon the concepts of Apache Ant and Apache Maven and introduces a Groovy-based domain-specific language (DSL) instead of the XML form used by Apache Maven for declaring the project configuration.[2] Gradle uses a directed acyclic graph ("DAG") to determine the order in which tasks can be run.

Gradle was designed for multi-project builds, which can grow to be quite large. It supports incremental builds by intelligently determining which parts of the build tree are up to date; any task dependent only on those parts does not need to be re-executed.

Both Maven and Gradle are able to cache dependencies locally and download them in parallel. As a library consumer, Maven allows one to override a dependency, but only by version. Gradle provides customizable dependency selection and substitution rules that can be declared once and handle unwanted dependencies project-wide.

#What is dependency management?#
Software projects rarely work in isolation. Projects relies on reusable functionality in the form of libraries or is divided in individual components to compose a modularized system. DM is a technique for declaring, resolving and using dependencies requiered by the project in an automated way. 