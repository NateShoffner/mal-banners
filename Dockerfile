FROM python:3.9-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

WORKDIR /srv/flask_app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --src /usr/local/src

COPY assets/ ./assets
COPY app/ ./app
COPY start.sh uwsgi.ini  ./

RUN chown -R www-data:www-data /srv/flask_app

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
