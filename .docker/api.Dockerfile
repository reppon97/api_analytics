FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
RUN apt-get update && apt-get install make postgresql-client -y
RUN chmod +x .docker/wait_for_postgres.sh
ENTRYPOINT .docker/wait_for_postgres.sh make init-docker