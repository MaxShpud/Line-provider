FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
COPY .env /app/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --default-timeout=300 -r requirements.txt

COPY src /app/

EXPOSE 8001