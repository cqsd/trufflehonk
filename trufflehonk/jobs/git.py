import os

from urllib.parse import urlparse

from trufflehonk.jobs.base import BaseJob
from trufflehonk.jobs import mixins
from trufflehonk.utils import shell


def to_gopath(git_url):
    '''turn a URL into a go-style package path, or whatever they're called. you
    know what i mean.

    NB: this doesn't handle some (probably a lot of) things, notably redirects,
    or cnames or whatever. www.github.com is distinct from github.com, and
    cqsd/test.git is distinct from cqsd/test. It also does not give a fuck about
    your janky paths or whatever, cqsd//////test is distinct from cqsd/test
    '''
    parsed = urlparse(git_url)
    return os.path.join(parsed.netloc, parsed.path)


# we should move the s3 shit to s3_files.py. then add a context manager so we
# can do something like:
# with s3_files.open_directory(to_gopath(repo_url)) as repo_path:
#   # update_git_repo(repo_path)  # cd in and git pull
#   # do shit
# context manager saves to s3 (TODO: asynchronously) when done and then removes
# the repo_path tempdir
class GitJob(BaseJob, mixins.TempFileMixin):
    def __init__(self, repo_url, repo_basedir=None,
                 restore_from_s3_bucket=None, restore_from_s3_key=None):
        self.repo_url = repo_url
        basedir = repo_basedir or self.tempdir
        self.clone_path = os.path.join(basedir, to_gopath(repo_url))
        super().__init__()

    # idea is you have to call this yourself. if you don't call this,
    # then it gets cloned fresh on first call to .repo_path
    def restore_repo_from_s3(self, clone_basedir=None, clone_dir=None):
        # get canonical repo path (go style)
        # check if the dir exists on disk
        # if not, check if the .tar exists in s3
        # download the tar, untar it to the destination
        # otherwise nothing happens and repo_path will clone fresh on first call
        pass

    def save_repo_to_s3(self):
        # tar to a tempdir, s3_client.upload_file
        pass

    def clone_repo(self):
        # fyi: `ValueError: Reference at 'refs/heads/master' does not exist`
        # can be raised when cloning an empty repo
        git_args = ['clone', self.repo_url, self.clone_path]
        # git clone creates dirs
        shell.exec_timeout(['git', *git_args])

    def update_repo(self):
        # cd to repo_path and git fetch origin? or git pull origin?
        pass

    @property
    def repo_path(self):
        '''Clone a git repo if it doesn't exist locally. Return local path to
        repo.'''
        if not os.path.exists(self.clone_path):
            self.clone_repo()
        self.update_repo()

        return self.clone_path
