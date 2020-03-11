import os

from trufflehonk.jobs.base import BaseJob
from trufflehonk.jobs import mixins
from trufflehonk.utils import exec_timeout


# TODO: need a teardown that removes the repo from disk
class GitJob(BaseJob, mixins.TempFileMixin):
    '''dunno I honestly forgot what mixins are supposed to do
    :repo_url url of repo
    :clone_path_name dirname (relative or absolute) to clone to
    '''
    def __init__(self, repo_url: str, clone_path_name: str = ''):
        self.repo_url = repo_url

        # TODO cleanup lol
        if not clone_path_name:
            basedir = self.tempdir()
            basename = os.path.basename(repo_url)
            self.clone_path_name = os.path.join(basedir, basename)
        else:
            self.clone_path_name = clone_path_name

        print(self.clone_path_name)

        super().__init__()

    @property
    def repo_path(self):
        '''Clone a git repo if it doesn't exist locally. Return local path to
        repo.'''
        if not os.path.exists(self.clone_path_name):
            # XXX: ValueError: Reference at 'refs/heads/master' does not exist
            # raised when cloning an empty repo
            git_args = ['clone', self.repo_url, self.clone_path_name]
            # git clone creates dirs
            exec_timeout(['git', *git_args])

        return self.clone_path_name
