import json

from trufflepawg.outputs.base import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, job):
        if hasattr(job, 'output_human'):
            print(job.output_human())
        else:
            print(json.dumps(job.output(), indent='  '))
