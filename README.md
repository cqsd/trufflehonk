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

## examples
### local usage
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

### consuming from a queue
`./cli/trufflehonk-worker` is also usable locally, but it provides a lot of
additional (explicit) configuration that makes it suitable for use as (e.g.)
a Docker entrypoit in (say) a worker pool. For example:

```bash
queue_url='https://sqs.us-west-2.amazonaws.com/012345678901/trufflehonk-jobs-01'
for msg in $(sc github list-repos users cqsd); do
    aws sqs send-message \
        --queue-url=$queue_url \
        --message-body=" https://github.com/cqsd/$msg"  # space? do you know why? :/
done

./cli/trufflehonk-worker scan \
    --queue=from=sqs,queue_url=https://sqs.us-west-2.amazonaws.com/012345678901/trufflehonk-jobs-01 \
    --output=to=stdout,format=human \
    --output=to=s3,format=json,bucket=trufflehonk-example
```
will consume git urls off of the SQS queue `https://sqs.us-west-2.amazonaws.com/012345678901/trufflehonk-jobs-01`, run truffleHog and PyDriller, then send the results
 - to stdout in human-readable format
 - to the S3 bucket `trufflehonk-example` in json format

### goobernetes
you'll have to push the image and tweak the manifest a bit to use the right
image tag
```
docker build -t gcr.io/example/trufflehonk:v0.1.1 .
docker push gcr.io/example/trufflehonk:v0.1.1
# example starts 5 workers
kubectl apply -f manifests/sqs-job-example.yaml
```

## docs
lol?

## todo
(PRs welcome ie i will not do these)
 - pass through the rest of the trufflehog options
 - add timestamp or hash or something to job names
 - refactor lol
