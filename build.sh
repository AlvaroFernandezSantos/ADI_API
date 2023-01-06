#!/bin/bash

echo "Building the authentication system image..."

docker stop alpine-auth 2>/dev/null
docker rm -f alpine-auth 2>/dev/null
docker build --rm -f Docker/Dockerfile --tag alpine-auth Docker/ > /dev/null 2>&1

echo "Done!"
docker save alpine-auth:latest | gzip > auth_image.tar.gz
echo "Image saved in auth_image.tar.gz"
