# Dockerized MySQL server and phpmyadmin web interface
## Running the Container:
`docker-compose up -d`

The SQL script `init.sql` is defined as entrypoint, it creates the necessary tables.
## Using phpmyadmin web interface
open http://localhost:8081 and log in.

NOTE: root login doesn't work in web interface.