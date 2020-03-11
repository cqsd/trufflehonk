import sys

from trufflehonk.jobs import trufflehog, pydriller
from trufflehonk.utils import github_org_repos


org = 'cqsd'
repos = github_org_repos(org, user=True)


secrets = []
author_emails = dict()


def update_dict_sets(d1, d2):
    '''Given two dicts d1, d2 mapping keys to sets, extend the sets in d1 using
    the sets in d2. Keys present in d2 but missing in d1 are added to d1.

    Warning: d1 is mutated, d2 is not.

    Example:

        >>> d1 = {'a': {1, 2}}
        >>> d2 = {'a': {1, 3}, 'b': {1}}
        >>> update_dict_sets(d1, d2)
        >>> d1
        {'a': {1, 2, 3}, 'b': {1}}
        >>> d2
        {'a': {1, 3}, 'b': {1}}
    '''
    for k, v in d2.items():
        if k in d1:
            d1[k].update(v)
        else:
            d1[k] = set(v)


for repo in repos:
    try:
        repo_url = f'https://github.com/{org}/{repo}'
        clone_path = f'/tmp/wee/{repo}'

        tf = trufflehog.Trufflehog(repo_url, clone_path)
        pd = pydriller.PyDriller(repo_url, clone_path)

        heading = f'processing {repo_url}'
        print(f'processing {repo_url}', file=sys.stderr)

        tf.run()
        pd.run()

        secrets += tf.output
        update_dict_sets(author_emails, pd.output)
    except KeyboardInterrupt:
        break
    except Exception as e:
        # I don't know what exceptions can happen tbh
        print(e)


print('secrets')
print('============================')
print(trufflehog.output_human(secrets))
print('commit authors')
print('============================')
print(pydriller.output_human(author_emails))
