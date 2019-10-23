# Motivation

1. With the increase in popularity of microservices, dependency analysis
in that field becomes important

# Introduction to Helm, Kubernetes and Docker

In order to understand what Helm does, you need to look into two other technologies, namely Kubernetes and Containers. 

Briefly, Kubernetes (https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is an open-source platform for deploying and managing containerised applications. An example of a containerised application is a docker image of a MySQL Server. With the help of a Docker Container this application runs in a closed environment, much like a Virtual Machine, yet it is implemented completely differently.
Instead of allocating resources to each Virtual Machine and not sharing those across others,
Docker containers run in the same operating system as its host. This way different containers can have access
to a lot of the operating system resources, which leads to very lightweight containers.

For large projects deploying applications on Kubernetes can be quiet tedious, since configuration files become extremely large very quickly. For this reason a tool called Helm (https://github.com/helm/helm) was created to simplify and streamline this process.

Helm (https://helm.sh/) is a package manager for Kubernetes. You can think of it as apt-get or homebrew for cloud applications. To install a package on a Kubernetes cluster using Helm, you just run helm install <package-name> and Helm takes care of deploying your application on the cluster.

Helm uses a packaging format called charts. A chart is a collection of files that describe a related set of Kubernetes resources. A single chart might be used to deploy something simple, like a memcached pod, or something complex, like a full web app stack with HTTP servers, databases, caches, and so on. (https://docs.helm.sh/developing_charts)
Now that we know what Kubernetes, Helm, and charts are, let’s talk about managing dependencies with Helm.

In Helm, one chart may depend on any number of other charts. For example, you may have a web server (that’s a chart) that depends on a MySQL database (another chart). The Helm docs tells us that we can define dependencies in two ways:

1. Dynamically, using the requirements.yaml file (example: https://github.com/jfrog/charts/blob/master/stable/artifactory-ha/requirements.yaml), or
2. Manually, by copying a chart and putting it in the charts/ directory of the Helm chart (example: https://github.com/helm/charts/tree/master/stable/weave-scope/charts)

# Data

# Methodology

# Results

# Disucssion