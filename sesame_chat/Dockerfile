FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /sesame_chat
COPY . .

RUN pip install --upgrade pip && pip install pip-tools && pip install -r requirements.txt 

# CMD python manage.py runserver
