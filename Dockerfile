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
    TRUFFLEHONK_OUTPUT_S3_BUCKET_NAME='example'

CMD python3 ./cli/trufflehonk-worker scan \
    --queue=from=sqs \
    --output=to=stdout,format=human \
    --output=to=s3,format=json
