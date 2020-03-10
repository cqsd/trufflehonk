from trufflehonk.jobs.github import PyDriller, Trufflehog
from trufflehonk.outputs.stdout import StdoutOutput
from trufflehonk.outputs.s3 import S3Output
from trufflehonk.queues.sqs import SqsQueue

# sqs has message visibility timeout (30s by default here) to help prevent race
# conditions with multiple queue consumers
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

    s3.output(tf, key=f'trufflehog/{org}/{repo}')
    s3.output(pd, key=f'pydriller/{org}/{repo}')
