import codecs
import json
import os

import boto3

from trufflehonk.outputs.base import BaseOutput

s3 = boto3.client('s3')


class S3Output(BaseOutput):
    def __init__(self, bucket=None):
        self.bucket = bucket or os.environ['TRUFFLEHONK_OUTPUT_S3_BUCKET_NAME']

    def output(self, job, bucket, key):
        output_binary = codecs.encode(
            json.dumps(job.output),
            'utf-8'
        )
        s3.put_object(
            Body=output_binary,
            Bucket=bucket,
            Key=key
        )
