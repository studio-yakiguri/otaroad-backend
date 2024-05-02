FROM python:3.11.4-slim-bookworm
LABEL name='otaroad-backend'
LABEL version="0.0.2"
LABEL builder="LeeDongHyeong"
LABEL builddate="2024.05.03-01:53:46"
LABEL env="beta"
LABEL description="Docker image for Otaroad Backend for BETA"

RUN apt update
RUN apt install -y git pkg-config default-libmysqlclient-dev build-essential curl
RUN apt install -y python3 python3-pip python3-venv
RUN git clone -b beta https://github.com/studio-yakiguri/otaroad-backend
WORKDIR /otaroad-backend
RUN pip install -r requirements.txt
# RUN curl http://100.107.194.104:8585/s/ftYfNwWGQtLmpEB/download/otaroad-key-files.tar --output secure.tar
# RUN tar -xvf secure.tar
RUN python3 manage.py collectstatic

EXPOSE 7500

CMD ["gunicorn", "--bind", "0:7500", "otaroad.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]