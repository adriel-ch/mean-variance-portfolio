FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get install -y python3

RUN apt-get install -y python3-pip

RUN apt-get install -y python3-requests
RUN apt-get install -y python3-urllib3
RUN apt-get install -y python3-numpy
RUN apt-get install -y python3-scipy
RUN apt-get install -y python3-pandas
RUN apt-get install -y python3-matplotlib

# RUN apt-get install -y pipenv
RUN pip install pipenv

RUN mkdir -p /mean-var
WORKDIR /mean-var

COPY . .

RUN pipenv --python 3.10
RUN pipenv install -r requirements.txt
RUN pipenv run python app/main.py
