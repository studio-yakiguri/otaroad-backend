FROM python:3.11.4-slim-bookworm
LABEL name='otaroad-backend'
LABEL version="0.0.1"
LABEL builder="LeeDongHyeong"
LABEL builddate="2023.07.14-01:19:40"
LABEL env="beta"
LABEL description="Docker image for Otaroad Backend for BETA"

RUN apt update && apt install -y git pkg-config default-libmysqlclient-dev build-essential
RUN apt install -y python3 python3-pip python3-venv
RUN git clone -b beta https://github.com/subculture-map/subculture-map-backend
WORKDIR /subculture-map-backend
RUN mkdir .secure
RUN pip install -r requirements.txt
RUN /subculture-map-backend/docker/setup-beta.sh

EXPOSE 9000

ENTRYPOINT [ "python3 -m gunicorn otaroad.asgi:application -k uvicorn.workers.UvicornWorker" ]