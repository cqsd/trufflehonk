from trufflehonk.outputs.base import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, job):
        print(job.format(self.format))
