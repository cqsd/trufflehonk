from urllib.parse import urlparse

from trufflehonk.utils import shell


def to_gopath(url):
    '''turn a URL into a go-style package path, or whatever they're called. you
    know what i mean.

    NB: this doesn't handle some (probably a lot of) things, notably redirects,
    or cnames or whatever. www.github.com is distinct from github.com, and
    example/test.git is distinct from example/test. It also does not give a
    fuck about your janky paths, example//////test is distinct from
    example/test
    '''
    parsed = urlparse(url)
    # can't use os path join or urljoin here neither does what you want due to
    # interpreting leading slashes in parsed.path in unproductive ways
    return parsed.netloc + parsed.path


def repo_url_meta(url):
    '''given a repo url like proto://github.com/user/repo, return
    {'service': 'github.com',
     'user': 'user',
     'repo': 'repo'}
     '''
    parsed = urlparse(url)
    try:
        user, repo = parsed.path.strip('/').split('/')
        return {
            'service': 'github.com',
            'user': user,
            'repo': repo
        }
    except ValueError:
        print(
            'this is brittle as fuck and something broke also this is obviously'
            ' functionally incorrect anyway so lmfao PRs welcome'
        )
        raise


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
