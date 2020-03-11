from trufflehonk.jobs.trufflehog import Trufflehog
from trufflehonk.jobs.pydriller import PyDriller
from trufflehonk.outputs.s3 import S3Output
from trufflehonk.queues.sqs import SqsQueue

# sqs has message visibility timeout (30s by default here) to help prevent race
# conditions with multiple queue consumers
for job in SqsQueue():
    org, repo = job.strip().split(' ')
    repo_url = f'https://github.com/{org}/{repo}'
    clone_path = f'/tmp/{repo}'
    tf = Trufflehog(repo_url, clone_path)
    pd = PyDriller(repo_url, clone_path)

    tf.run()
    pd.run()

    s3 = S3Output()

    print(tf.output_human)
    print(pd.output_human)

    s3.output(tf, key=f'trufflehog/{org}/{repo}')
    s3.output(pd, key=f'pydriller/{org}/{repo}')
