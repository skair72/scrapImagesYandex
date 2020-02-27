FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY . /app/


## Add the wait script to the image
#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
#RUN chmod +x /wait