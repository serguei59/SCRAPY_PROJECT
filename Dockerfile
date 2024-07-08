FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

WORKDIR /app/filmscraper

CMD scrapy crawl allocinespider
CMD scrapy crawl allocine_serie_spider

