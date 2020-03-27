import os

import requests


def get_org_repos(identifier, user=False, repo_type=None):
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

    # TODO: pagination
    resp = requests.get(url, params={'per_page': 200})
    if resp.ok:
        names = [repo['name'] for repo in resp.json()]
        return names
    else:
        raise Exception(f'Github API Error {resp.reason}')
