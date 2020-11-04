#!/usr/bin/env bash

# IF statements from https://stackoverflow.com/a/6482403

if [ $# -eq 0 ]
  then
    echo "No DB File Path arguement supplied."
    exit
fi

if [ -z "$1" ]
  then
    echo "No DB File Path argument supplied."
    exit
fi

# Set VOLUMENAME
VOLUMENAME="graph"

# Create docker volume
docker volume create $VOLUMENAME

# Build and run docker volume, then get the container ID of the last ran container
docker build . -t code
docker run -v $VOLUMENAME:/metrics -p 5000:5000 code $1

CONTAINERID="$(docker ps -q -n 1)"

# Remove created docker containers and volumes after the container has been stopped
echo "Stopping docker container" $CONTAINERID
docker stop $CONTAINERID

echo "Deleting container with ID:" $CONTAINERID
docker rm $CONTAINERID

echo "Deleting volume with NAME:" $VOLUMENAME
docker volume rm $VOLUMENAME

# echo "Deleting ALL DOCKER CONTAINERS AND VOLUMES"
# docker system prune -a --volumes
