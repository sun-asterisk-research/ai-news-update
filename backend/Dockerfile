# pull official base image
FROM brunneis/python:3.8.6-ubuntu-20.04

# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update package
RUN apt-get update && apt -y install git-all

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# copy entrypoint.sh
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
