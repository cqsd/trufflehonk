import codecs
import json
import os

import boto3

from trufflehonk.outputs.base import BaseOutput

s3 = boto3.client('s3')


class S3Output(BaseOutput):
    def __init__(self, *args, bucket=None, **kwargs):
        self.bucket = bucket or os.environ['TRUFFLEHONK_OUTPUT_S3_BUCKET_NAME']
        super().__init__(self, *args, **kwargs)

    def output(self, job):
        output_binary = codecs.encode(
            json.dumps(job.output),
            'utf-8'
        )
        s3.put_object(
            Body=output_binary,
            Bucket=self.bucket,
            Key=job.name  # FIXME
        )
