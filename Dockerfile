FROM python:2.7

COPY . /src

WORKDIR /src

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./app.py"]
