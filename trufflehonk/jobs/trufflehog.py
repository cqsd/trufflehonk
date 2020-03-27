import json

from trufflehonk.jobs.git import GitJob
from trufflehonk.utils import shell


class Trufflehog(GitJob):
    def __init__(self, *args, rules_file=None, **kwargs):
        self.rules_file = rules_file
        super().__init__(*args, **kwargs)

    def run(self):
        # easier than figuring out how to import trufflehog as a library, lol
        args = [
            *(['--rules', self.rules_file] if self.rules_file else []),
            '--regex',
            '--entropy', 'false',
            '--json',
            self.repo_path
        ]
        raw_output = shell.exec_timeout(['trufflehog', *args])

        acc = []
        for line in raw_output.splitlines():
            finding = json.loads(line.decode('utf-8'))

            # enrich with a direct link to the affected file
            commit_hash = finding['commitHash']
            file_path = finding['path']
            commit_link = f'{self.repo_url}/blob/{commit_hash}/{file_path}'
            finding['commitLink'] = commit_link

            acc.append(finding)

        self.output = acc

    @property
    def output_human(self):
        return output_human(self.output)


def output_human(secrets):
    acc = ''

    # lol
    def print(s='', end='\n'):
        nonlocal acc
        acc += s + end

    fields = [
        'reason',
        'date',
        'path',
        'commitHash',
        'commitLink',
        'stringsFound'
    ]
    field_left_pad = max(len(field) for field in fields)

    def print_field(secret, field):
        value = secret.get(field)
        print(f'{field:{field_left_pad}} {value}')

    # hack to only print newlines between secrets
    hack = False
    for secret in secrets:
        if not hack:
            hack = True
        else:
            print()
        for field in fields:
            print_field(secret, field)

    return acc
