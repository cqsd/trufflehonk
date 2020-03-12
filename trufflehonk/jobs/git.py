import os

from trufflehonk.jobs.base import BaseJob
from trufflehonk.jobs import mixins
from trufflehonk.utils import exec_timeout


# TODO: remove the repo from disk when using default tempdir
class GitJob(BaseJob, mixins.TempFileMixin):
    def __init__(self, repo_url, repo_basedir=None, repo_basename=None):
        self.repo_url = repo_url

        basedir = repo_basedir or self.tempdir
        basename = repo_basename or os.path.basename(repo_url)
        self.clone_path_name = os.path.join(basedir, basename)

        super().__init__()

    @property
    def repo_path(self):
        '''Clone a git repo if it doesn't exist locally. Return local path to
        repo.'''
        if not os.path.exists(self.clone_path_name):
            # fyi: ValueError: Reference at 'refs/heads/master' does not exist
            # raised when cloning an empty repo
            git_args = ['clone', self.repo_url, self.clone_path_name]
            # git clone creates dirs
            exec_timeout(['git', *git_args])

        return self.clone_path_name
