# CyPDP Docker Workshop May 2024

## Introduction to the core concepts of Docker and containerisation

### Note
docker-compose V1 has been deprecated by the new docker compose V2. They are very similar and the V1 commands map directly to V2 without further modification. We will be basing this tutorial on the newer docker compose.

### What is Docker?
Docker is a platform for developing, shipping and running packaged applications, it enables you to manage your infrastructure in the same way you manage your application, with code, reducing the complexity between writing code in development and running it in production.

### What is a container?
A container is a lightweight, self-contained, portable, packaged application environment. It is an executable environment instance, containing everything your code needs to run, packaged up separately from other containers and the underlying operating system that it is running on. The container will incorporate a specific  version of languages, tools, files, libraries and configurations.

Containers enable you to share copies of containers while you develop your application, ensuring everyone you share with gets the same container that works in the same way, also ensuring consistency in the CI/CD pipeline and production environment. Each container should do one single thing, for example it should run the frontend application code, OR run the database, OR run an API, etc. Containers encourage applications to be developed using microservices, as each part of an application can be wrapped in it's own complete environment package. Containers are much more lightweight than virtual machines, making it viable to run many containers at once.

Configuration options can be provided to a container when it is created or started.

It is possible to create, start, stop, rebuild, move and delete containers using the CLI or the Docker extension in VS Code. You can create a network to connect a container to, so it can communicate with other containers on the same network. When a container is removed, any changes to it's state that aren't stored in persistent storage (such as a volume) will disappear, and you can also attach persistent storage to a container if desired.

### Containers vs VMs
A VM is an entire OS with it's own kernel, hardware drivers, programs and applications, running on top of the host OS.

A container is an isolated process with all of the files needed to run the application. Containers share the underlying OS kernel, allowing you to run more applications on less infrastructure. 

![Containers vs VMs](./Containers%20vs%20VMs.png)

### What is an Image?
An image is a read-only template containing the instructions for creating a container, it is basically a tar file with associated metadata. Once you instantiate an image, it becomes a container. Creating an image of a container allows us to share containers. 

Images can be based on other images with additional customisations. For example you could build a custom image which is based on the alpine (minimal) or ubuntu (feature rich) base image and installs the apache web server and your application, as well as configuration details needed to make your application run. It is likely that your application will be run using a combination of public images from a registry, plus images you have created yourself that run your application code.

### What is a Dockerfile?
A Dockerfile is a text file containing the steps needed to build your custom container image. Docker will build the image by reading the instructions in the Dockerfile. You will start with a base image and then use further commands to customise the image you want to create.

A Dockerfile accepts the following commands (and more):
- FROM \<base image\> - create a new build stage from a base image
- ADD - files and directories
- COPY - files and directories
- ARG - build-time variables
- ENV - environment variables
- RUN - execute build commands
- ENTRYPOINT ["command"] - the default executable
    - This is the most important command, it is the default start command for the container
    - If not specified, /bin/sh -c is executed as the default command
- CMD ["arg1", "arg2"] - commands to run
    - Another possible start command to use in place of ENTRYPOINT
- EXPOSE - which ports your application is listening on
- VOLUME - create volume mounts

Environment variables can be used throughout the file, for example:

Set the environment variable example:
- ENV foo=/bar

Use the environment variable example:
- WORKDIR ${foo}

The ADD, COPY, ENTRYPOINT and CMD arguments can be set using:
- shell form
    - list of items ie ADD /my/file /mydir
    - docker wraps the command in a /bin/sh -c shell
- exec form (preferred)
    - json array of items ie ADD ["/my/file", "/mydir"]

### What is the .dockerignore file?
This file specifies which files and directories to exclude from the build context, so these files will not be included inside the built container. You will likely want to exclude files and directories such as IDE config files, node_modules or dist directories etc.

### What are image layers?
Each layer in an image contains a set of filesystem changes, for example:
- start with a base image
- add some basic commands and apt
- install Python runtime and pip
- copy in application specific requirements.txt file
- install application dependencies
- copy in source code

Each instruction in a Dockerfile adds additional layers to the image, so it is best practice not to run multiple RUN commands, but instead connect them using &&, ie RUN yum --something --somethingelse && yum update -y && yum install tool

Layers can be reused between images. Docker manages caching each layer for reuse.

### What is a Docker registry?
A Docker registry stores and provides access to container images, enabling distribution. Docker Hub is a public registry that anyone can use, and Docker looks for images on Docker Hub by default. You can, if you wish, run your own private registry.

### What is an image tag?
You can assign tags to images, allowing you to assign names to the different image versions. "Latest" is the default tag. Tags are also used to identify the registry to push the image to: \<registry url\>/\<image name\>:\<tag name\>

### What is docker compose?
Docker compose is a tool for defining and running multi-container applications. It simplifies the control of your entire application stack, making it easy to manage services, networks and volumes. Instead of calling multiple "docker run" commands to start multiple containers, you can define all of your containers and their configuration in a single YAML file. With a single command, you can create and start all the services for your application from your configuration file. If you include this file in your code repository, anyone who clones your repository can get up and running with a single command, ensuring they are using the same environment to run the application that you are developing in.

### Dockerfile vs docker compose
A Dockerfile provides instructions to build a single container image, while a docker compose file defines the running containers, and will often reference one or more Dockerfiles to build images to use for a particular service defined within.

### What is a Network?
By default, containers run in isolation and don't know anything about other processes or containers on the same machine. Networking allows one container to talk to another container, if you put two containers on the same network, they are able to talk to each other.
By default, Docker compose sets up a single network for your application. Each container joins the default network and is reachable by other containers on that network and they are discoverable by the container's name. Each container can look up another container's name and get back that container's IP address. 

You can also create your own networks in the docker compose file, and add groups of containers to specific networks.

### How do I make a container accessible outside the internal Docker network?
In the docker compose file, you can map which ports a container is accessible on, via HOST_PORT:CONTAINER_PORT, or PORT_OUTSIDE_CONTAINER:PORT_INSIDE_CONTAINER. When two networked containers communicate service-to-service, they will use the internal CONTAINER_PORT, and the service is accessible outside the swarm, for example via your browser, using the external HOST_PORT.

### What are Volumes?
Docker isolates all content, code and data in a container from your local filesystem, so when you delete a container, Docker deletes all the content within that container. Sometimes, you may want to persist the data that a container generates. To do this, we use volumes. The volume is a reference to the underlying file system on the host machine, allowing a directory on the host filesystem to feed into a directory inside the container. If you mount a directory in the container, the changes are also seen in the directory on the host machine, so when you destroy the container, the changed files are persisted on the host. When you restart the container, the changed files are available inside the container again, ensuring data persistence. Volumes can also be shared amongst multiple containers. 

### How do I send code updates into a container for development?
To serve your changing development code into the container to enable development, you can create a volume between the local filesystem code, and the container filesystem code. This means any code changes in your local filesystem are fed into the container filesystem, without having to rebuild the container every time you wish to see the effects of your code changes.

Alternately, the watch attribute in a compose file automatically updates and previews your running compose containers as you edit and save your code locally. Watch allows for greater granularity than a volume, also allowing you to set rules to ignore specific files or entire directories within the watch tree.

The watch attribute specifies an action attribute. Action has multiple options:
- sync - any changes made to files on your host automatically match with the corresponding files inside the container, and is ideal for frameworks that support "hot reload" functionality, and can be used in place of volumes for development in most use cases.
- rebuild - any changes made to files on your host causes Docker to automatically build a new image and replace the running container, it is ideal for compiled languages or for particular files that require a full image rebuild.
- sync+restart - any changes made to files on your host causes Docker to sync the corresponding files inside the container and then restart the container, ideal for config file changes where you don't need to rebuild the whole image.
