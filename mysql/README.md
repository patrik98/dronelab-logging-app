# Dockerized MySQL server and phpmyadmin web interface

## Building Docker Image:
`docker build -t dronelab_mysql .`

The SQL script `init.sql` is defined as entrypoint, it creates the tables.

## Running the Container:
`docker-compose up -d`

## Using phpmyadmin web interface
open http://localhost:8081 and log in.

NOTE: root login doesn't work in web interface.