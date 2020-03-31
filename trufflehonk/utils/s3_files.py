import logging
import tarfile
import tempfile

import boto3

from botocore.exceptions import ClientError

from trufflehonk.utils import git  # XXX


s3 = boto3.client('s3')


def restore_dir_from_s3(bucket, key, path):
    '''Retrieve a .tar.gz from S3 and untar to a path.

    :bucket s3 bucket name
    :key s3 object key. the object should be a gzipped tar archive
    :path path to dir to untar to
    '''
    # potential untar path vuln
    logging.info(f'restoring dir from s3://{bucket}/{key}')
    with tempfile.NamedTemporaryFile(suffix='tar.gz') as f:
        s3.download_fileobj(bucket, key, f)
        f.file.seek(0)  # sigh
        with tarfile.open(fileobj=f, mode='r:gz') as archive:
            logging.info(f'extracting to {path}')
            archive.extractall(path=path)
    return path


def save_dir_to_s3(bucket, key, path):
    '''tar and gzip the *contents of* a directory and store it in S3. This
    means the tar archive starts INSIDE the directory. hope this makes sense to
    my future self i have to look this shit up every time i use it i stg
    '''
    logging.info(f'saving dir to s3://{bucket}/{key}')
    with tempfile.NamedTemporaryFile(suffix='tar.gz') as f:
        with tarfile.open(fileobj=f, mode='w:gz') as archive:
            archive.add(path, arcname='.')
            logging.info(f'archiving into {f.name}')
        f.file.seek(0)  # sigh
        s3.upload_fileobj(f, bucket, key)
    return path


class S3Dir:
    '''Open a context that fetches a "dir" in S3 to the local disk, returning
    a path to the directory. Save the (potentially modified) directory back to
    S3 as a gzipped tar archive on close. Optionally remove the local copy. If
    the key corresponding to the dir does not exist in S3, the local copy will
    be initially empty.

    Directory paths map to S3 "paths" but with the assumption that directories
    ares represented as .tar.gz in S3. For example, opening the directory
    "work/dir/one" fetches and untars the key work/dir/one.tar.gz. Other
    archive formats are not currently supported, though it's possible to
    specify alternate extensions by passing a whole :key.

    Example usage:
    >>> with S3Dir(bucket, 'git/github.com/cqsd/test', temp=True) as repo:
            update_repository(repo)
            publish('osint/emails', items=get_contributor_emails(repo))

    FYI: I suspect there's some S3 consistency issues with doing this, but the
    primary use is as a VCS cache to reduce (but not necessarily eliminate)
    load on external VCS servers. Immediate consistency and race conditions
    don't really matter.

    :bucket str name of bucket
    :path str dirname to open
    :key str specific key to fetch. overrides the :path option
    :restore (True) attempt to restore the directory from s3
    :temp (True) delete the directory on exiting the context
    :save (True) tar and save the directory to s3 on exiting the context
    '''
    def __init__(self, bucket=None, path=None, key=None, restore=True, save=True, temp=True):
        self.bucket = bucket
        self.key = key if key else path + '.tar.gz'
        self.save = save
        self.temp = temp
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = self.tempdir.name
        if restore:
            self.restore()

    def restore(self):
        try:
            restore_dir_from_s3(self.bucket, self.key, self.tempdir.name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logging.info('First time using this dir!')
            else:
                raise

    def cleanup(self):
        if self.save:
            save_dir_to_s3(self.bucket, self.key, self.tempdir.name)
        if self.temp:
            self.tempdir.cleanup()

    def __enter__(self) -> str:
        return self.path

    def __exit__(self, *_):
        self.cleanup()


class S3GitRepo(S3Dir):
    def __init__(self, repo_url, *args, update=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo_url = repo_url

        if not git.is_repo(self.path):
            git.clone(repo_url, self.path)
        if update:
            git.update(self.path)
