FROM python:3.7-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install Flask gunicorn qrcode Pillow

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app