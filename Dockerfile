FROM python:3-alpine

RUN apk update && apk add git

RUN adduser -D -s /bin/nologin aha

WORKDIR /trufflehonk

USER aha

ADD --chown=aha:aha requirements.txt .

RUN pip install --user -r requirements.txt

ENV PATH $PATH:/home/aha/.local/bin

ADD --chown=aha:aha . .

CMD python3 run.py
