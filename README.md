# Telegram bot for python learning
My Telegram bot for python learning

## Docker commands:
### Build an image:
`docker build . -t bot`
### Build and run a new container:
`docker run --name bot bot`
### Run the existing container:
`docker start bot`
### Stop the container:
`docker stop bot`
### Delete the container:
`docker rm bot`
#### You **have NOT** to delete an old **IMAGE** when creating a new one with the same name.
#### You **HAVE TO DELETE** an old **CONTAINER** when creating a new one with the same name.
### List of running containers:
`docker ps`
### List of all containers:
`docker ps -a`
### List of all images:
`docker image ls or docker images`