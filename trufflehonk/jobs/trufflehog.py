import json

from trufflehonk.utils import shell


# easier than figuring out how to import trufflehog as a library, lol
def find_secrets(repo_path, repo_url=None, rules_file=None):
    args = [
        *(['--rules', rules_file] if rules_file else []),
        '--regex',
        '--entropy', 'false',
        '--json',
        repo_path
    ]
    raw_output, *_ = shell.exec_timeout(['trufflehog', *args])

    secrets = []
    for line in raw_output.splitlines():
        finding = json.loads(line.decode('utf-8'))

        # enrich with a direct link to the affected file
        commit_hash = finding['commitHash']
        file_path = finding['path']
        if repo_url:
            commit_link = f'{repo_url}/blob/{commit_hash}/{file_path}'
            finding['commitLink'] = commit_link

        secrets.append(finding)

    return secrets


def to_human_string(secrets):
    acc = ''
    fields = [
        'reason',
        'date',
        'path',
        'commitHash',
        'commitLink',
        'stringsFound'
    ]
    field_left_pad = max(len(field) for field in fields)

    # hack to only print newlines between secrets
    hack = False
    for secret in secrets:
        if not hack:
            hack = True
        else:
            acc += '\n'
        for field in fields:
            value = secret.get(field)
            acc += f'{field:{field_left_pad}} {value}\n'

    return acc
