FROM python:3-alpine

RUN apk update && apk add git

RUN adduser -D -s /bin/nologin aha

WORKDIR /trufflehonk

RUN chown -R aha:aha /trufflehonk

USER aha

ADD --chown=aha:aha requirements.txt .

ENV PATH $PATH:/home/aha/.local/bin

RUN pip install --user -r requirements.txt

ADD --chown=aha:aha . .

RUN pip install --user .

CMD python3 ./cli/trufflehonk-worker
