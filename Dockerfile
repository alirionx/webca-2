FROM ubuntu:focal

RUN apt update && apt install -y \
  python3 \
  python3-pip \
  python-dev \
  libsasl2-dev \
  libldap2-dev \
  libssl-dev

COPY ./webapp/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./webapp /data
RUN pip3 install waitress

WORKDIR /data
EXPOSE 80

CMD waitress-serve --port=80 "main:app" 