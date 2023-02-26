FROM python:3.8
ENV PYTHONUNBUFFERED 0
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt


COPY . .
WORKDIR /backend
