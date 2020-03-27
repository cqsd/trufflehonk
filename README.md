> i was asked to automate trufflehog (sort of) so here,
```bash
# requires: jq, git, truffleHog, curl
kind=users
org=cqsd
for repo in $(curl -Ls "https://api.github.com/$kind/$org/repos?per_page=200" \
    | jq '.[].name' \
    | tr -d \"); do
    truffleHog --entropy=false --regex https://github.com/$org/${repo}.git
done
```

## local usage
`./cli/trufflehonk` is intended for use on your local machine
```bash
python3 -m venv /tmp/epicgamermoment
source /tmp/epicgamermoment/bin/activate
pip install -e .
trufflehonk scan cqsd --repos test,trufflehonk
```

for all repos in an org/user account
```bash
# github limitation: you have to spec whether you're looking for a user or an org
trufflehonk scan cqsd --user
trufflehonk scan wpengine
```

## worker
`./cli/trufflehonk-worker` is intended for use as a Docker entrypoint

```bash
queue_url='https://sqs.us-west-2.amazonaws.com/012345678901/trufflehonk-jobs-01'
for msg in $(sc github list-repos users cqsd); do
    # it reads urls straight off the queue, as you can see
    aws sqs send-message \
        --queue-url=$queue_url \
        --message-body="https://github.com/cqsd/$msg"  # FYI set cli_follow_urlparam = false in ~/.aws/config or you're in for a fucking surprise
done

# see Dockerfile ENV for config
./cli/trufflehonk-worker start
```

## docs
lol
