FROM python:3.10-slim-buster

WORKDIR /LATEST_NEWS_BOT

COPY requirements.txt ./

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "run.py"]