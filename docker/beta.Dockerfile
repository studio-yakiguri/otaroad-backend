FROM python:3.11.4-slim-bookworm
LABEL name='otaroad-backend'
LABEL version="0.0.1"
LABEL builder="LeeDongHyeong"
LABEL builddate="2023.07.16-05:04:40"
LABEL env="beta"
LABEL description="Docker image for Otaroad Backend for BETA"

RUN apt update
RUN apt install -y git pkg-config default-libmysqlclient-dev build-essential curl
RUN apt install -y python3 python3-pip python3-venv
RUN git clone -b beta https://github.com/subculture-map/subculture-map-backend
WORKDIR /subculture-map-backend
RUN pip install -r requirements.txt
RUN curl -k -X GET https://100.107.194.104/s/Rx7FsP4znMBgNjn/download --output secure.tar
RUN tar -xvf secure.tar
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", "0:8000", "otaroad.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]