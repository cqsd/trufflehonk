from trufflehonk.jobs.github import PyDriller, Trufflehog
from trufflehonk.outputs.stdout import StdoutOutput
from trufflehonk.utils import github_org_repos


org = 'cqsd'
repos = github_org_repos(org, user=False)


for repo in repos[:1]:
    tf = Trufflehog(org, repo)
    pd = PyDriller(org, repo)

    tf.run()
    pd.run()

    stdout = StdoutOutput()
    stdout.output(tf)
    stdout.output(pd)
