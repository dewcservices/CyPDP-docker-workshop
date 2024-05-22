# CyPDP Docker Workshop May 2024

Be sure to prepare by reading [Pre-Workshop Preparation](./Pre-Workshop%20Preparation.md) and [Introduction to the core concepts of Docker and containerisation](./Introduction%20to%20the%20core%20concepts%20of%20Docker%20and%20containerisation.md).

## Part A - Create a Dockerfile and build an image for your local application

This workshop comes with a simple Python Flask To Do Application to use as a local application that we are going to containerise. If you have not done so already, clone this repo and download the source code for the application.
- cd /home/$USER/my-dev/dewc-docker-workshop
- git clone https://github.com/dewcservices/CyPDP-docker-workshop.git .
    - Ensure you capture the '.' at the end of this command, so we clone the files without an additional parent directory
- cd app

Create a Dockerfile and a .dockerignore file for the application image. Start with a base python image, set any environment variables, set the working directory, install any frameworks and tools you need, expose the application port inside the container, copy in the application files and run the application.

Build the image.
- docker build -t flask-todo-app .
    - -t \<image-name\>[:\<tag-name\>] specifies the name of the image with an optional tag name
    - . specifies the current directory as the context of the build

View the build image in Docker.
- docker image ls

## Part B - Run the image as a container

Run the application container from the image we just built.
- docker run -d -p 8000:5000 flask-todo-app
    - -d detaches the terminal from the Docker command once it has run
    - -p creates a port mapping between the host and the container, in the format \<HOST_PORT\>:\<CONTAINER_PORT\>
    - flask-todo-app specifies the name of the image we just built

View the running container in Docker.
- docker ps

Open your browser at http://localhost:8000 to see your running application.

Play around with the Docker container and image, the following commands may be useful:
- docker ps [-a]
- docker stop \<container-id\>
- docker restart \<container-id\>
- docker kill \<container-id\>
- docker rm \<container-id\>
- docker image ls
- docker image rm \<image-id\>

Attach a shell inside the Docker container and take a look at the files in the container. You will enter the container at the working directory that you specified in the Dockerfile. Take a look around and see that the files in the .dockerignore file are not included in the container.
- docker exec -it \<container-id\> sh
    - -it create an interactive shell for the specified container
    - sh specifies the command with which to enter the container, here is specifies a shell. We could also use `/bin/bash` if it is available in the image to enter in via a bash shell, or any other command we want, provided the container contains the corresponding functionality.
- ls
- ls templates
- ls ..
- exit

Take a look at the Docker extension in VSCode, you will be able to see the images, containers, networks and volumes (no networks and volumes yet). You can view the logs or attach a shell into a container here as well.

## Part C - Update the application code

Update some text in the file `templates/home.html`.

Rebuild the image.
- docker build -t flask-todo-app .

Stop and remove the old container.
- docker ps
- docker stop \<container-id\>
- docker rm \<container-id\>

Start the new application container.
- docker run -d -p 8000:5000 flask-todo-app

Refresh your browser and see the new code running, and see the items in your to do list will have disappeared.

## Part D - Do it all again using a Docker compose file

Create a compose.yaml file. We are going to break down the commands we used above to build and run the image container and contain them in the compose.yaml file. Remember our commands from above:
- docker build -t flask-todo-app .
- docker run -d -p 8000:5000 flask-todo-app
We could have had much more complicated commands to create and run the image container, and in that case, the compose file would have been more complex and resulted in simplifying a much more complex  build and run process, however, for this simple example, it is simple enough.

Stop and remove the old containers and images.
- docker ps
- docker stop \<container-id\>
- docker rm \<container-id\>
- docker image ls
- docker image rm \<image-id\>

Start the application stack.
- docker compose up -d
    - -d detaches the terminal from the Docker command once it has run

You will see the image being built, as before.

You can view the logs via:
- docker compose logs -f
    - this command will combine all of the logs from all of the starting containers
    - -f will follow the logs, showing more output as it is generated
- docker compose logs -f \<container-name\>
    - this command will show logs only from the specified container

Open your browser at http://localhost:8000 to see your running application.

Tear it all down with:
- docker compose down

## Part E - Add a watch attribute for application development

Update the compose.yaml file to use the watch attribute for development.

Ensure you use the --watch flag when you start the containers, note that this is not compatible with the -d flag.
- docker compose up --watch

Update some text in the file `templates/home.html`. 

Refresh your browser and see the new code running.

Note that the container image has not been updated with the new code, so if you tear down the container and restart it without the --watch flag, the application code will be at the point it was when Docker created the image, which is when you first built the container from the compose.yaml file. You will either need to ensure you use the --watch flag to see new code changes, or rebuild the application image, to see the new code inside the container.

## Part F - Create a database container from a public image

Create a mysql container in the compose.yaml file. We are going to use a public image from DockerHub, you can see here which tagged versions are available, how to use the image, details on any environment variables you need to send in etc.
- https://hub.docker.com/_/mysql

Start the application stack.
- docker compose up -d

To confirm the database is running, we can connect a shell into the database container and take a look around.
- docker ps
- docker exec -it \<mysql-container-id\> /bin/bash
- mysql -u root -p
    - and enter the password `secret`

This is the mysql shell, let's take a look and see if the todos database exists
- SHOW DATABASES;
- SHOW TABLES FROM todos;
- exit
- exit

## Part G - Connect your application to the database, via a Docker network

By default, Docker compose creates a single network for your application, so, if we are using Docker compose, we don't need to do anything further to enable the containers to talk to each other. If you are not using Docker compose, as per the beginning of this workshop, you will need to create a network and connect the containers to it.
- docker network create todo-app-network
- docker run ... --network todo-app-network ...

Docker will manage the network and resolve the correct IP address of the container via the container name.

Checkout the updated version of the Python Flask To Do Application, this one uses a database instead of a local array to store the to do list items.
- git checkout app-with-database

Update the application container in the compose.yaml file to send in the following environment variables:
- MYSQL_HOST
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DB

Note that using environmental variables for connection settings like this is fine for development, but in production we need a more secure mechanism. Docker secrets can be used but are beyond the scope of this workshop.

Start the application stack.
- docker compose up -d

Follow the logs and watch the application connect to the database.
- docker compose logs -f

Add some items to the todo list. Connect to the mysql database shell and see that the items have been added to the database table.
- docker ps
- docker exec -it \<mysql-container-id\> /bin/bash
- mysql -u root -p todos
    - and enter the password `secret`
- SELECT * FROM todo;
- exit

You will now also be able to see the network in Docker.
- docker network ls

## Part H - Create a volume for the database to persist the data

Your to do list is empty every time we start the container, this is because the container and all of it's changes are destroyed when we shut it down. We can persist the database data by creating a volume.

If you are not using Docker compose, as per the beginning of this workshop, you will need to create a volume and connect the containers to it.
- docker volume create todo-app-volume
- docker run ... --mount type=volume,src=todo-app-volume,target=/var/lib/mysql ...

Update the mysql container in the compose.yaml file to create a volume.

Start the application stack.
- docker compose up -d

Add some items to the todo list. Stop and remove the containers.
- docker ps
- docker stop \<container-id\>
- docker rm \<container-id\>
- docker image ls
- docker image rm \<image-id\>

Start the application stack again.
- docker compose up -d

Take a look at your to do list and see that the items have persisted.

You will now also be able to see the volume in Docker.
- docker volume ls

# Further Reading

- [Docker Secrets](https://docs.docker.com/compose/use-secrets/)
- [The Complete Guide to Docker Secrets](https://earthly.dev/blog/docker-secrets/)
