from trufflehonk.queues.stdin import StdinQueue

from trufflehonk.jobs.trufflehog import Trufflehog
from trufflehonk.jobs.pydriller import PyDriller

for job in StdinQueue():
    org, repo = job.strip().split(' ')
    repo_url = f'https://github.com/{org}/{repo}'
    clone_path = f'/tmp/{repo}'
    tf = Trufflehog(repo_url, clone_path)
    pd = PyDriller(repo_url, clone_path)

    tf.run()
    pd.run()

    print(tf.output_human)
    print(pd.output_human)
