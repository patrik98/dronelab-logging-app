# use the python 3.8 image
FROM python:3.8

# set a working directory for the app
WORKDIR /app

# copy the requirements.txt into the working directory
COPY app/requirements.txt ./requirements.txt

# install all requirements
RUN pip install -r ./requirements.txt

# copy the config file to the respective place in the dockerfile 
COPY config.toml /root/.streamlit/config.toml

# expose the port
EXPOSE 8501

# copy all app code in the working dir
COPY ./app .

# define an endpoint to be executed
ENTRYPOINT ["streamlit", "run"]
CMD ["logApp.py"]

