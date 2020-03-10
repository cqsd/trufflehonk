import os

import boto3

from trufflehonk.queues.base import BaseQueue

sqs = boto3.client('sqs')


class SqsQueue(BaseQueue):
    def __init__(self, queue_url=None):
        self.queue_url = queue_url or os.environ['TRUFFLEHONK_QUEUE_SQS_URL']

    def pop(self, n=1, visibility_timeout=30, wait_timeout=5):
        response = sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=n,
            VisibilityTimeout=visibility_timeout,
            WaitTimeSeconds=wait_timeout
        )

        if response and 'Messages' in response:
            message = response['Messages'][0]  # ? don't remember why index 0
            sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            return message['Body']  # ['Message']
        else:
            return None
