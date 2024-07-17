# SSH Game
A project that aim to be a fully playable game in SSH

## Deployment
This project can be deployed using docker.
```commandline
git clone https://github.com/LeBeaufort/ssh-game.git
docker compose up -d
```
If you want to update :
```
docker compose down # shutdown container
git pull  # update locals files
docker compose up -d --build # rebuild docker image and deploy
```

## TODO list:
- [ ] Game
  - [x] finish it
  - [ ] some optimization (game "blink" in SSH)
- [ ] make it playable through SSH (using docker)
  - [x] start on SSH connection
  - [ ] SSH server accepting every user + password
