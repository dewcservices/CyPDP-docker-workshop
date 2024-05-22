# Specify which image to base this image on.
# The python image from Docker Hub already has python and other tools installed,
# saving us from having to create an image from scratch.
FROM python:3.11-alpine

# Set some environment variables for the container build.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory for any further Dockerfile instructions
# to be run from. If it does not exist, it will be created.
WORKDIR /code

# Add some tools we may need.
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy the requirements.txt file into the container working directory.
COPY requirements.txt ./

# Run the pip install command to install the required tools into the container.
RUN pip install -r requirements.txt

# Expose the port number 5000 from within the container.
EXPOSE 5000

# Set which user to run as, it is best practice not to run your container as root (default).
RUN adduser -D -g '' flaskuser
USER flaskuser

# Copy files from the local filesystem into the container filesystem.
# The first '.' here represents the local current directory.
# The second '.' here represents the container current directory, which is the WORKDIR we set above.
# Note that any files in the .dockerignore file will not be included.
# Ensure the correct user has ownership so they can run the files.
COPY --chown=flaskuser:flaskuser . .

# Specify which command to run upon starting the container.
# Note that the container will only run for as long as this command takes to run.
CMD ["flask", "run", "--debug"]