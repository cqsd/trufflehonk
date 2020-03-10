import codecs
import json

import boto3

from trufflehonk.outputs.base import BaseOutput

s3 = boto3.client('s3')


class S3Output(BaseOutput):
    def output(self, job, bucket, key):
        output_binary = codecs.encode(
            json.dumps(job.output(), indent='  '),
            'utf-8'
        )
        s3.put_object(
            Body=output_binary,
            Bucket=bucket,
            Key=key
        )
