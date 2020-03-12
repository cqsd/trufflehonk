import sys

from trufflehonk.jobs import trufflehog, pydriller
from trufflehonk.utils import github_org_repos, update_dict_sets


org = 'cqsd'
repos = github_org_repos(org, user=True)


secrets = []
author_emails = dict()


for repo in repos:
    try:
        repo_url = f'https://github.com/{org}/{repo}'
        clone_path = f'/tmp/wee/{repo}'

        tf = trufflehog.Trufflehog(repo_url, clone_path)
        pd = pydriller.PyDriller(repo_url, clone_path)

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
