# use the python 3.8 image
FROM python:3.8

# set a working directory for the app
WORKDIR /


# copy all app code to the app directory
COPY ./app app/

# install all requirements
RUN pip install -r app/requirements.txt

# copy the config file to the respective place in the dockerfile 
COPY config.toml /root/.streamlit/config.toml

# expose the port
EXPOSE 8501

# define an endpoint to be executed
ENTRYPOINT ["streamlit", "run"]
CMD ["app/logApp.py"]

