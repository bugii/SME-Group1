# Requirements

Java jdk8 or higher.

# How to use

1. Get the tool from [MicroDepGraph](https://github.com/clowee/MicroDepGraph) and the jar file [here](https://wetransfer.com/downloads/2f0d080c8e9d09c814416a1f33d2cf6c20191011064223/3bcf007c7411057b72491349f8fa6c1a20191011064223/75c663).
2. Get the java project developed with a microservice architectural style based on docker configuration to your local drive.
3. Execute : java -jar microservices.comm.pattern.check-1.0-SNAPSHOT-jar-with-dependencies.jar  <absolute_path_of_the_cloned_repository> <project_name>

# Output

It gives output in 2 folders:

* in ../neo4jData/<project_name> a neo4j graph database
* in ../<project_name> a DOT file describing the graph, a graphml file and a svg file.

# Dataset

There are a list of projects analyzed on the MicroserviceDataset repository [view](https://github.com/clowee/MicroserviceDataset)


