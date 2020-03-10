import json
import os

from pydriller import RepositoryMining

from trufflehonk.jobs.base import BaseJob
from trufflehonk.jobs import mixins
from trufflehonk.utils import exec_timeout


# TODO: need a teardown that removes the repo from disk
class GithubJob(BaseJob, mixins.TempFileMixin):
    def __init__(self, org, repo):
        self.org = org
        self.repo = repo
        # only used for enriching output
        self.repo_url = f'https://github.com/{self.org}/{self.repo}'
        super().__init__()

    # 1 - make me a generic git version of this
    # 2 - instead of a random tempdir, use a common base directory for all
    #     instances of this class (?) or at least a fixed common base dir
    #     to prevent re-cloning
    def repo_path(self):
        '''Clone a github repo if it doesn't exist locally. Return local path
        to repo.'''
        repo_abs_path = f'{self.tempdir}/{self.org}/{self.repo}'

        if not os.path.exists(repo_abs_path):
            # XXX: ValueError: Reference at 'refs/heads/master' does not exist
            # raised when cloning an empty repo
            git_args = ['clone', self.repo_url, repo_abs_path]
            # git clone creates dirs
            exec_timeout(['git', *git_args])

        return repo_abs_path


class Trufflehog(GithubJob):
    def run(self):
        args = [
            '--regex',
            '--entropy', 'false',
            '--json',
            self.repo_path()
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

        self.output = authors
