FROM python:3.8.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements/*.txt /code/
RUN pip install -r develop.txt
COPY . /code/
