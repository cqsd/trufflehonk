import os
from trufflehonk.jobs.github import PyDriller, Trufflehog
from trufflehonk.outputs.stdout import StdoutOutput
from trufflehonk.outputs.s3 import S3Output
from trufflehonk.queues.sqs import SqsQueue

BUCKET = os.environ['S3_BUCKET_NAME']

for job in SqsQueue():
    org, repo = job.strip().split(' ')
    tf = Trufflehog(org, repo)
    pd = PyDriller(org, repo)

    tf.run()
    pd.run()

    # TODO need a cleaner way to do the outputs that can be done with config
    # rather than code
    stdout = StdoutOutput()
    s3 = S3Output()

    stdout.output(tf)
    stdout.output(pd)

    s3.output(tf, bucket=BUCKET, key=f'trufflehog/{org}/{repo}')
    s3.output(pd, bucket=BUCKET, key=f'pydriller/{org}/{repo}')
