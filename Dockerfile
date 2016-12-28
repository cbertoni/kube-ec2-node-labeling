FROM alpine:3.4

RUN apk update && apk add python py-pip

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt /opt/app

RUN /usr/bin/pip install -r requirements.txt

COPY . /opt/app

CMD ["/usr/bin/python", "app.py"]
