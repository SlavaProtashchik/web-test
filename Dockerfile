FROM python:3.11-alpine

ENV HOME_DIR=/home/app

WORKDIR $HOME_DIR

COPY requirements.txt requirements.txt
COPY src/ $HOME_DIR/

RUN pip install -r requirements.txt

ENV FLASK_APP=$HOME_DIR/app.py \
    FLASK_ENV=development

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]