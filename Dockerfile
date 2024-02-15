FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y libxml2-dev libxslt1-dev build-essential python3-lxml zlib1g-dev
RUN apt-get install -y default-mysql-client default-libmysqlclient-dev
RUN apt-get install redis-server  -y
RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY . .
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]