FROM python:3.9

RUN apt-get update

RUN mkdir /code
WORKDIR /code

COPY . /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

ENV FLASK_APP=${FLASK_APP}

EXPOSE 5000

COPY docker-entrypoint.sh /code/docker-entrypoint.sh
