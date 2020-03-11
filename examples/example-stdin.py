from trufflehonk.queues.stdin import StdinQueue
from trufflehonk.outputs.stdout import StdoutOutput

from examples import trufflehog as tf_job
from examples import pydriller as pd_job

for job in StdinQueue():
    org, repo = job.strip().split(' ')
    repo_url = 'https://github.com/{org}/{repo}'
    tf = tf_job.Trufflehog(repo_url, '.')
    pd = pd_job.PyDriller(repo_url, '.')

    tf.run()
    pd.run()

    stdout = StdoutOutput()

    stdout.output(tf)
    stdout.output(pd)
