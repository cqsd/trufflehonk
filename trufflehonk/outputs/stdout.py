import json

from trufflehonk.outputs.base import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, job):
        print(json.dumps(job.output, indent='  '))
