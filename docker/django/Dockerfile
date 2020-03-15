FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY ./docker/django/req.txt /requirements/req.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements/req.txt

RUN apt-get update -y \
    && apt-get install -y gettext

RUN apt-get install -y \
    postgresql-server-dev-all \
    libgeos-dev \
    libgdal-dev \
    postgresql-client \
    mc

COPY ./diplom /app
COPY ./docker/django/entrypoint.sh /django/entrypoint.sh

RUN sed -i 's/\r//' /django/entrypoint.sh \
  && chmod +x /django/entrypoint.sh

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/django/entrypoint.sh"]
