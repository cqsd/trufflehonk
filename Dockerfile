FROM python:3-alpine

RUN apk update && apk add git

RUN adduser -D -s /bin/nologin aha

WORKDIR /trufflehonk

USER aha

ADD --chown=aha:aha requirements.txt .

RUN pip install --user -r requirements.txt

ENV PATH $PATH:/home/aha/.local/bin

ADD --chown=aha:aha . .

RUN pip install --user .

ENV TRUFFLEHONK_QUEUE_SQS_URL='https://sqs.us-west-1.whatever.example.com' \
    TRUFFLEHONK_S3_FILES_BUCKET_NAME='example' \
    TRUFFLEHONK_WEBHOOK_URL='http://localhost:4150'

CMD python3 ./cli/trufflehonk-worker start
