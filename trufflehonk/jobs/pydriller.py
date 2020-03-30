from pydriller import RepositoryMining


def find_authors(repo_path):
    repo = RepositoryMining(repo_path)
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
    return {email: list(names) for email, names in authors.items()}


def to_human_string(authors):
    acc = ''
    email_left_pad = max(len(email) for email in authors)
    for email in authors:
        names = ', '.join(authors[email])
        acc += f'{email:{email_left_pad}} {names}\n'

    return acc
