import json
from pydriller import RepositoryMining

from trufflehonk.jobs.base import BaseJob
from trufflehonk.jobs import mixins


# TODO: need a teardown that removes the repo from disk
class GithubJob(BaseJob, mixins.GithubMixin):
    def __init__(self, org, repo, *args, **kwargs):
        self.org = org
        self.repo = repo
        # only used for enriching output
        self.repo_url = f'https://github.com/{self.org}/{self.repo}'
        self.meta = {
            'repo_is_fork': Trufflehog._get_repo(org, repo)['fork']
        }
        self._output = None
        super().__init__(*args, **kwargs)

    def repo_path(self):
        return self._repo_path(self.org, self.repo)


class Trufflehog(GithubJob):
    def run(self):
        args = [
            '--regex',
            '--entropy', 'false',
            '--json',
            self.repo_path()
        ]
        raw_output = self.exec(['trufflehog', *args])

        acc = []
        for line in raw_output.splitlines():
            finding = json.loads(line.decode('utf-8'))

            # enrich with a direct link to the affected file
            commit_hash = finding['commitHash']
            file_path = finding['path']
            commit_link = f'{self.repo_url}/blob/{commit_hash}/{file_path}'

            # add some stuff to make it easier to search later
            meta = {**self.meta}
            meta['direct_link'] = commit_link
            finding['meta'] = meta

            # wish you could get the author but trufflehog is too haha for that
            acc.append(finding)

        self._output = acc

    def output(self):
        return self._output


class PyDriller(GithubJob):
    def run(self):
        repo = RepositoryMining(self.repo_path())
        authors = dict()
        for commit in repo.traverse_commits():
            ae = commit.author.email
            if ae is None:
                # this can happen, as it happens ;)
                ae = '*no-email*'
            an = commit.author.name
            if ae not in authors:
                authors[ae] = {an}
            else:
                authors[ae].add(an)

        # Sets are not JSON serializable, convert to lists first
        for email, names in authors.items():
            authors[email] = list(names)

        self._output = authors

    def output(self):
        return self._output
