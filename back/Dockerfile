FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# ENV FLASK_ENV development
ENV FLASK_DEBUG 1
ENV PYTHONUNBUFFERED=1

COPY . /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]