my_server = '172.17.0.2 auth.local'

all: remove build container

build:
	docker build --rm -f Docker/Dockerfile --tag alpine-auth Docker/

container:
	docker run --privileged -ti -d --name alpine-auth --hostname auth alpine-auth

remove:
	-docker stop alpine-auth
	docker rm -f alpine-auth

tests:
	-pip install tox
	tox -c Docker/authService

clean:
	find . -name "*~" -delete	

add_server:
	sudo -- sh -c "echo $(my_server) >> /etc/hosts"

remove_server:
	sudo -- sh -c "sed -i '/$(my_server)/d' /etc/hosts"