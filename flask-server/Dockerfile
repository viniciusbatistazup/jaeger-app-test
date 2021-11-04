FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV JAEGER_HOST=jaeger-agent
ENV JAEGER_PORT=6831

COPY flask-server.py .

CMD [ "python3", "flask-server.py"]