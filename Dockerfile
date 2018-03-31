FROM python:3.6

MAINTAINER Daniel Palma <danivgy@gmail.com>

RUN apt-get update && apt-get install -y \
    build-essential python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
    flac lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev

RUN echo "deb http://www.deb-multimedia.org jessie main non-free"  >> /etc/apt/sources.list \
    && echo "deb-src http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --force-yes deb-multimedia-keyring \
    && apt-get install -y --force-yes --no-install-recommends ffmpeg=10:2.6.9-dmo1

RUN mkdir -p /code/doc2audiobook

COPY requirements.txt /code/doc2audiobook
RUN pip install -r /code/doc2audiobook/requirements.txt

RUN pip install --upgrade chardet

COPY . /code/doc2audiobook

ENV GOOGLE_APPLICATION_CREDENTIALS /.secrets/client_secret.json

RUN mkdir /data /.secrets /log

ENTRYPOINT ["python", "/code/doc2audiobook/doc2audiobook.py"]
