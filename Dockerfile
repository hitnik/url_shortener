FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

#copy project
COPY . .

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=main


#install dependencies
RUN pip install -U pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir