import collections
import logging
import os
import subprocess

import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# lol https://stackoverflow.com/posts/6027615/revisions
def flatten_dict_keys(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict_keys(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


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


def exec_timeout(exec_args, timeout=600):
    stdout, _ = subprocess.Popen(
        exec_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    ).communicate(timeout=timeout)

    return stdout


def github_org_repos(identifier, user=False, repo_type=None):
    '''Return the names of the repos in a given org/user account.

    identifier (str): username or org name
    user(bool) False: if specified, tries to fetch repos for a user. Default
    tries to fetch for an org. This is a Github API limitation.
    repo_type(str): sources, forks, public, private, etc. See Github docs. Only
                    works for orgs
    '''
    GH_BASE_URL = 'https://api.github.com/'  # orgs/<org>/repos?per_page=200'
    kind = 'users' if user else 'orgs'
    url = os.path.join(GH_BASE_URL, kind, identifier, 'repos')
    if repo_type:
        url += f'?type={repo_type}'

    logger.info(f'Getting repos for [{identifier}]: [{url}]')

    # TODO: pagination
    resp = requests.get(url, params={'per_page': 200})
    if resp.ok:
        names = [repo['name'] for repo in resp.json()]
        logger.info(f'Found [{len(names)}] repos')
        return names
    else:
        raise Exception(f'Github API Error {resp.reason}')
