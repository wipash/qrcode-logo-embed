FROM python:3.7

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
RUN pip install Flask gunicorn qrcode Pillow flask-weasyprint

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app