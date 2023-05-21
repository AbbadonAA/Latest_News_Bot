FROM python:3.10-slim-buster

RUN python -m pip install --upgrade pip

WORKDIR /LATEST_NEWS_BOT

COPY requirements.txt /LATEST_NEWS_BOT

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /LATEST_NEWS_BOT

ENTRYPOINT ["uvicorn"]

CMD ["run:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
