FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN python3 -m pip install --upgrade pip
RUN pip install wheel
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn kubstu_alisa.wsgi:application --bind 0:8000