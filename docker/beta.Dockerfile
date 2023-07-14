FROM python:3.11.4-slim-bookworm
LABEL name='otaroad-backend'
LABEL version="0.0.1"
LABEL builder="LeeDongHyeong"
LABEL builddate="2023.07.14-01:19:40"
LABEL env="beta"
LABEL description="Docker image for Otaroad Backend for BETA"

RUN apt update && apt install -y git pkg-config default-libmysqlclient-dev build-essential
RUN mkdir data
WORKDIR /data
RUN git clone -b beta https://github.com/subculture-map/subculture-map-backend
RUN mkdir .secure
WORKDIR /data/subculture-map-backend/.secure
WORKDIR /data/subculture-map-backend
RUN pip3 install -r requirements.txt

VOLUME [ "/data" ]

EXPOSE 9000

CMD [ "./docker/beta-runserver.sh" ]
