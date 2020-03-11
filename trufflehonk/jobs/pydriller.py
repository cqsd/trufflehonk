from pydriller import RepositoryMining

from trufflehonk.jobs.git import GitJob


class PyDriller(GitJob):
    def run(self):
        repo = RepositoryMining(self.repo_path)
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
