# Dronelab Logging App

Logging application for persisting and analyzing drone flight paths from the Dronelab.  

Streamlit web app and custom python backend with DB connection.

## Building locally
Create a Personal Access Token with API scope. This access token will be passed as argument to docker-compose or the Dockerfile, to install the dronelab-db-lib - see [dronelab-db-lib](https://gitlab.web.fh-kufstein.ac.at/golecpatrik/dronelab-db-lib/-/blob/master/README.md).

Build with docker-compose:  
`docker-compose build --build-arg GITLAB_TOKEN="<personal_access_token>"`

Build Dockerfile:  
`docker build -t dronelab-logging-app --build-arg GITLAB_TOKEN="<personal_access_token>" .`

## Run locally
Run in detached mode:  
`docker-compose up -d`