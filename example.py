from trufflepawg.jobs.github import PyDriller, Trufflehog
from trufflepawg.queues.stdin import StdinQueue
from trufflepawg.outputs.stdout import StdoutOutput

for job in StdinQueue():
    org, repo = job.strip().split(' ')
    tf = Trufflehog(org, repo)
    pd = PyDriller(org, repo)

    tf.run()
    pd.run()

    stdout = StdoutOutput()

    stdout.output(tf)
    stdout.output(pd)
