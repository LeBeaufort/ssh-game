FROM python:3.9.19-slim-bullseye

#  Installing ssh server
RUN apt-get update && apt-get install openssh-server -y

RUN mkdir /game/

# Installing libs
COPY ./docker/requirements.txt /
RUN pip install -r /requirements.txt

# creating file containing git info
WORKDIR /temp/
COPY ./docker/commit_info.py ./
COPY .git/ ./.git/
RUN python3 commit_info.py "/game/commit_info"


# creating new user
RUN useradd -m game && passwd -d game

# setting up ssh server
COPY ./docker/ssh-banner /etc/ssh-banner
COPY ./docker/sshd_config /etc/ssh/sshd_config

WORKDIR /game/
COPY ./game/* .

RUN service ssh start

CMD ["/usr/sbin/sshd","-D"]