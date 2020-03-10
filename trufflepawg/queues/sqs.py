import boto3

from trufflepawg.queues.base import BaseQueue

sqs = boto3.client('sqs')


class SqsQueue(BaseQueue):
    def __init__(self, queue_url):
        # this should come from an env var lol
        self.queue_url = queue_url

    def pop_job_from_sqs(self):
        '''Attempt to pop a job config from the queue, ie, receive a message,
        delete it from the queue, and retun the job config json as a dict.'''
        response = sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=5
        )

        if response and 'Messages' in response:
            job_message = response['Messages'][0]
            sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=job_message['ReceiptHandle']
            )
            return job_message['Body']  # ['Message']
        else:
            return None

    def pop(self):
        return self.pop_job_from_sqs()
