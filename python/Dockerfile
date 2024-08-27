FROM python:3
USER root

RUN apt-get update
RUN apt-get install -y vim less curl
RUN pip install --upgrade pip
RUN pip install 'fonttools[ufo,woff,unicode]' zopfli brotli requests

WORKDIR /python
CMD ["./bin/gen_webfonts"]
