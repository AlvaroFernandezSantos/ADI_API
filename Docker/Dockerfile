FROM alpine

RUN apk -U upgrade
RUN apk add python3
RUN apk add py3-pip


COPY entrypoint.sh /entrypoint.sh
COPY authService /home/authService

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]