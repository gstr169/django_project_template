FROM python:3

ENV PYTHONBUFFERED 1

ARG PGPASSWORD
ENV PGPASSWORD=${PGPASSWORD}

ARG PGDATABASE
ENV PGDATABASE=${POSTGRES_DB}

ARG WORKERS
ENV WORKERS=${WORKERS}

ARG APP_ENV
ENV APP_ENV=${APP_ENV}

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]
