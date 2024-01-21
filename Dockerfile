FROM python:3.11-alpine

ENV HOME_DIR=/home/app \
    FLASK_APP=/home/app/app.py \
    FLASK_ENV=development \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_DEBUG=1

WORKDIR /home/app

COPY requirements.txt requirements.txt
COPY app.py app.py

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]