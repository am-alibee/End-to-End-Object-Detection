from python:3.10-slim-buster

RUN apt update -y && app install awscli -y
WORKDIR /app

COPY ./app .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "app.py" ]