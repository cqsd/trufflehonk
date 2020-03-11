import json

from trufflehonk.jobs.git import GitJob
from trufflehonk.utils import exec_timeout


class Trufflehog(GitJob):
    def run(self):
        args = [
            '--regex',
            '--entropy', 'false',
            '--json',
            self.repo_path
        ]
        raw_output = exec_timeout(['trufflehog', *args])

        acc = []
        for line in raw_output.splitlines():
            finding = json.loads(line.decode('utf-8'))

            # enrich with a direct link to the affected file
            commit_hash = finding['commitHash']
            file_path = finding['path']
            commit_link = f'{self.repo_url}/blob/{commit_hash}/{file_path}'
            finding['commit_link'] = commit_link

            acc.append(finding)

        self.output = acc
