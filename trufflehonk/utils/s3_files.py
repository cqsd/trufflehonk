# WARNING: THIS SHIT IN THIS DIR IS VERY DANGEROUS TO RUN ON YOUR
# LOCAL MACHINE LMFAOOOOO
import logging
import tarfile
import tempfile

import boto3

from botocore.exceptions import ClientError


s3 = boto3.client('s3')


def restore_dir_from_s3(bucket, key, path):
    '''Retrieve a .tar.gz from S3 and untar to a path.

    :bucket s3 bucket name
    :key s3 object key. the object should be a gzipped tar archive
    :path path to dir to untar to
    '''
    # 1: potential for untar vuln
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

    :bucket name of bucket
    :path dirname to open
    :s3_suffix defaults to .tar.gz, gets appended to :path to form the key to
    fetch
    :key specific key to open. overrides the :path option
    '''
    def __init__(self, bucket, path=None, key=None, temp=True):
        self.bucket = bucket
        assert path or key  # yeah, yeah
        self.key = key if key else path + '.tar.gz'
        self.temp = temp

    def __enter__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        try:
            return restore_dir_from_s3(self.bucket, self.key, self.tempdir.name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logging.info('First time using this dir!')
                return self.tempdir.name
            raise

    def __exit__(self, *_):
        save_dir_to_s3(self.bucket, self.key, self.tempdir.name)
        if self.temp:
            self.tempdir.cleanup()