FROM python:3

ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install --upgrade pip
RUN pip install urllib3 --upgrade
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]
