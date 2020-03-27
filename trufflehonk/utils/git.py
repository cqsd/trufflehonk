from urllib.parse import urlparse

from trufflehonk.utils import shell


def to_gopath(url):
    '''turn a URL into a go-style package path, or whatever they're called. you
    know what i mean.

    NB: this doesn't handle some (probably a lot of) things, notably redirects,
    or cnames or whatever. www.github.com is distinct from github.com, and
    cqsd/test.git is distinct from cqsd/test. It also does not give a fuck about
    your janky paths or whatever, cqsd//////test is distinct from cqsd/test
    '''
    parsed = urlparse(url)
    # can't use os path join or urljoin here neither does what you want due to
    # interpreting leading slashes in parsed.path in not-useful-for-this-case
    # ways
    return parsed.netloc + parsed.path


def is_repo(path):
    '''cd to :path and `git status` to check if it's a git repo'''
    *_, status_code = shell.exec_timeout(['git', 'status'], cwd=path)
    return not status_code


def clone(url, path):
    # fyi: `ValueError: Reference at 'refs/heads/master' does not exist`
    # can be raised when cloning an empty repo
    git_args = ['clone', url, path]
    # git clone creates dirs by default
    return shell.exec_timeout(['git', *git_args])


def update(path, remote='origin', branch='master'):
    '''cd to :path and git pull :remote :branch'''
    git_args = ['pull', remote, branch]
    return shell.exec_timeout(['git', *git_args], cwd=path)
