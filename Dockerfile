FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /docker_django
WORKDIR /docker_django
COPY . /docker_django

RUN pip install --upgrade pip
RUN pip install -r requirements.txt