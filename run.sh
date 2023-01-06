#!/bin/bash

echo "Starting the authentication system..."

docker stop alpine-auth > /dev/null 2>&1
docker rm -f alpine-auth > /dev/null 2>&1
docker load < auth_image.tar.gz > /dev/null 2>&1
docker run --privileged -ti -d --name alpine-auth -p 3001:3001 --hostname auth alpine-auth:latest > /dev/null 2>&1

echo "Authentication service is listening on port 3001"