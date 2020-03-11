from trufflehonk.jobs.trufflehog import Trufflehog
from trufflehonk.jobs.pydriller import PyDriller
from trufflehonk.outputs.stdout import StdoutOutput
from trufflehonk.utils import github_org_repos


org = 'cqsd'
repos = github_org_repos(org, user=True)


for repo in repos[:4]:
    repo_url = f'https://github.com/{org}/{repo}'
    clone_path = f'/tmp/{repo}'

    tf = Trufflehog(repo_url, clone_path)
    pd = PyDriller(repo_url, clone_path)

    print(f'processing {repo_url}')
    tf.run()
    pd.run()

    stdout = StdoutOutput()
    stdout.output(tf)
    stdout.output(pd)
