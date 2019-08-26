FROM python:3.7

MAINTAINER Daniel Palma <danivgy@gmail.com>

RUN apt-get update && apt-get install -y \
    build-essential python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr \
    flac lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev

RUN echo "deb http://www.deb-multimedia.org buster main non-free"  >> /etc/apt/sources.list \
    && apt-get update -oAcquire::AllowInsecureRepositories=true \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    --allow-unauthenticated deb-multimedia-keyring \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    --allow-unauthenticated ffmpeg=10:4.1.4-dmo1+deb10u1

RUN mkdir -p /code/doc2audiobook

COPY requirements.txt /code/doc2audiobook
RUN pip install -r /code/doc2audiobook/requirements.txt

COPY . /code/doc2audiobook

ENV GOOGLE_APPLICATION_CREDENTIALS /.secrets/client_secret.json

RUN mkdir /data /.secrets

ENTRYPOINT ["python", "/code/doc2audiobook/doc2audiobook.py"]
