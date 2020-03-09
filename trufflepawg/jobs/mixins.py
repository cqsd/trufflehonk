import os
import subprocess
import tempfile
import typing

import requests


class ExecMixin:
    def exec(self, exec_args: typing.List[str]) -> bytes:
        stdout, _ = subprocess.Popen(
            exec_args,
            stdout=subprocess.PIPE
        ).communicate(timeout=self.timeout)

        return stdout


# this one might be too limiting
class TempFileMixin:
    def tempfile(self):
        if not hasattr(self, '_tempfile'):
            self._tempfile = tempfile.mktemp()
        return self._tempfile

    def tempdir(self):
        if not hasattr(self, '_tempdir'):
            self._tempdir = tempfile.mkdtemp()
        print(self._tempdir)
        return self._tempdir


class GithubMixin(ExecMixin, TempFileMixin):
    @classmethod
    def _get_repo(cls, org, repo):
        base_url = 'https://api.github.com/'
        resp = requests.get(os.path.join(base_url, 'repos', org, repo))

        if resp.ok:
            return resp.json()
        else:
            raise Exception(f'Github API Error {resp.reason}')

    def _repo_path(self, org, repo):
        '''Clones a git repo if it doesn't exist. Return path to repo.'''
        repo_abs_path = f'{self.tempdir()}/{org}/{repo}'
        self.repo_url = f'https://github.com/{self.org}/{self.repo}'

        if not os.path.exists(repo_abs_path):
            git_args = ['clone', self.repo_url, repo_abs_path]
            # git clone creates dirs
            self.exec(['git', *git_args])

        return repo_abs_path
