from pydriller import RepositoryMining

from trufflehonk.jobs.git import GitJob


class PyDriller(GitJob):
    def run(self):
        repo = RepositoryMining(self.repo_path)
        authors = dict()
        for commit in repo.traverse_commits():
            ae = commit.author.email
            if not ae:
                # can be an empty string, sometimes it's just None
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

    @property
    def output_human(self):
        return output_human(self.output)


def output_human(authors):
    acc = ''

    def print(s, end='\n'):
        nonlocal acc
        acc += s + end

    email_left_pad = max(len(email) for email in authors)
    for email in authors:
        names = authors[email]
        print(f'{email:{email_left_pad}} {names}')

    return acc
