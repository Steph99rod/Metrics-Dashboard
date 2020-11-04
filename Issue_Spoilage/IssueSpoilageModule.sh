#!/usr/bin/env bash

# IF statements from https://stackoverflow.com/a/6482403

if [ $# -eq 0 ]
  then
    echo "No URL, Personal Access Token, or Export Location arguments supplied."
    exit
fi

if [ -z "$1" ]
  then
    echo "No URL argument supplied."
    exit
fi

if [ -z "$2" ]
  then
    echo "No Personal Access Token argument supplied."
    exit
fi


if [ -z "$3" ]
  then
    echo "No Export Location argument supplied."
    exit
fi

# Set VOLUMENAME
VOLUMENAME="issuespoilage"

# Create docker volume
docker volume create $VOLUMENAME

# Build and run docker volume, then get the container ID of the last ran container
docker build . -t code
docker run -v $VOLUMENAME:/metrics code $1 $2

CONTAINERID="$(docker ps -q -n 1)"

# Copy volume data to the CWD
docker container cp $CONTAINERID:/metrics $3

# Remove created docker containers and volumes after the container has been stopped
echo "Stopping docker container" $CONTAINERID
docker stop $CONTAINERID

echo "Deleting container with ID:" $CONTAINERID
docker rm $CONTAINERID

echo "Deleting volume with NAME:" $VOLUMENAME
docker volume rm $VOLUMENAME

# echo "Deleting ALL DOCKER CONTAINERS AND VOLUMES"
# docker system prune -a --volumes

echo "Metrics created and stored in" $3"/metrics"
