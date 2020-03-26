import os

import boto3

from trufflehonk.queues.base import BaseQueue


class SqsQueue(BaseQueue):
    def __init__(self, queue_url=None):
        self.client = boto3.client('sqs')
        self.queue_url = queue_url or os.environ['TRUFFLEHONK_QUEUE_SQS_URL']

    # TODO
    def push(self, message):
        return self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message
        )

    def pop(self, visibility_timeout=30, wait_timeout=5):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=visibility_timeout,
            WaitTimeSeconds=wait_timeout
        )

        if response and 'Messages' in response:
            # only fetch 1 at a time, so hardcode index 0
            message = response['Messages'][0]
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            return message['Body']
        else:
            return None
