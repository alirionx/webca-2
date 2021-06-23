FROM ubuntu:focal

RUN apt update && apt install -y \
  python3 \
  python3-pip

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./webapp /data
RUN pip3 install waitress

WORKDIR /data

#CMD waitress-serve --port=80 "heic2jpeg:app" 