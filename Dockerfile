FROM debian:stable-20240701-slim

#  Installing ssh server
RUN apt-get update && apt-get install openssh-server -y

# Installing python
RUN apt install python3 -y

# creating new user
RUN useradd -m game && passwd -d game

# setting up ssh server
RUN echo "" > /log.txt
COPY ./docker/ssh-banner /etc/ssh-banner
COPY ./docker/AuthorizedKeyScript.sh /
COPY ./docker/sshd_config /etc/ssh/sshd_config
RUN chmod 777 /AuthorizedKeyScript.sh && chmod 777 /log.txt

WORKDIR /game/
COPY ./game/* .

RUN service ssh start

CMD ["/usr/sbin/sshd","-D"]