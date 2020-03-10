from trufflehonk.jobs.github import PyDriller, Trufflehog
from trufflehonk.queues.stdin import StdinQueue
from trufflehonk.outputs.stdout import StdoutOutput

for job in StdinQueue():
    org, repo = job.strip().split(' ')
    tf = Trufflehog(org, repo)
    pd = PyDriller(org, repo)

    tf.run()
    pd.run()

    stdout = StdoutOutput()

    stdout.output(tf)
    stdout.output(pd)
