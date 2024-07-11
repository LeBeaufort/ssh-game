FROM debian:stable-20240701-slim

#  Installing ssh server
RUN apt-get update && apt-get install openssh-server -y

# Installing python
RUN apt install python3 -y

# creating new user
RUN useradd -m game && echo game:PSWD | chpasswd

WORKDIR /home/game/
COPY ./game/* game/

#  setting the .profile so the game is started when ssh connection start
RUN echo "We ran this cool line of script"
RUN echo "python3 ./game/game.py" >> .profile
RUN echo "exit" >> .profile

RUN service ssh start

CMD ["/usr/sbin/sshd","-D"]