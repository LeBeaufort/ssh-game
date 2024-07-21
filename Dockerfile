FROM debian:stable-20240701-slim

#  Installing ssh server
RUN apt-get update && apt-get install openssh-server -y

# Installing python
RUN apt install python3 -y

# creating new user
RUN useradd -m game && echo game:game | chpasswd

# setting up ssh server
RUN echo "" > /log.txt
COPY ./docker/ssh-banner /etc/ssh-banner
COPY ./docker/AuthorizedKeyScript.sh /
COPY ./docker/sshd_config /etc/ssh/sshd_config
RUN chmod 777 /AuthorizedKeyScript.sh && chmod 777 /log.txt

WORKDIR /home/game/
COPY ./game/* game/

#  setting the .profile so the game is started when ssh connection start
RUN echo "python3 ./game/game.py" >> .profile && echo "exit" >> .profile

RUN service ssh start

CMD ["/usr/sbin/sshd","-D"]