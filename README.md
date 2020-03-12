i was asked to automate trufflehog (sort of) so here

## examples
```bash
python3 -m venv /tmp/epicgamermoment
source /tmp/epicgamermoment/bin/activate
pip install -e .
trufflemog scan cqsd --repos test,trufflehonk
```

for all repos in an org/user account
```bash
# github limitation: you have to spec whether you're looking for a user or an org
trufflemog scan cqsd --user
trufflemog scan wpengine
```

consume off a queue why not `sqs -> trufflehog + pydriller -> s3`
Prerequisites: SQS queue and S3 bucket (see `./terraform/`)
```bash
for msg in $(github list-repos user cqsd); do
    aws sqs send-message \
        --queue-url "${QUEUE_URL}" \
        --message-body="$msg"
done

env TRUFFLEHONK_QUEUE_SQS_URL="${QUEUE_URL}" \
    TRUFFLEHONK_OUTPUT_S3_BUCKET_NAME="${BUCKET_NAME}" \
    python3 examples/example-sqs.py
aws s3 ls --recursive "s3://${BUCKET_NAME}"
```

goobernetes example in `./manifests/` won't work because the Dockerfile hasn't
been updated in a while you can fix that yourself lmao
```bash
# this is broken right now you can fix it yourself lmfao
docker build -t trufflehonk:v0.1.1 .
# example schedules 5 workers
kubectl apply -f manifests/sqs-job-example.yaml
```

## section 3 title
### queues
|path|description|requirements|
|-|-|-|
|`trufflehonk.queues.stdin.StdinQueue`|read args from stdin||
|`trufflehonk.queues.sqs.SqsQueue`|receive args from sqs|aws credentials and env `TRUFFLEHONK_QUEUE_SQS_URL`|

### jobs
|path|description|requirements|
|-|-|-|
|`trufflehonk.jobs.trufflehog.Trufflehog`|run trufflehog on a github repo|args: `org`, `repo`|
|`trufflehonk.jobs.pydriller.PyDriller`|run pydriller on a github repo|args: `org`, `repo`|

\* todo: generic git (there's no difference but i hardcoded a github base url)

### outputs
|path|description|requirements|
|-|-|-|
|`trufflehonk.outputs.stdout.StdoutOutput`|print output to stdout||
|`trufflehonk.outputs.s3.S3Output`|save output to a given key in a bucket|aws credentials, env `TRUFFLEHONK_OUTPUT_S3_BUCKET_NAME`, arg: `key`|

## fyi
there's trufflehog and pydriller example jobs just to make this useful out of
the box but this is really intended to be used as a generic job worker library
i should probably rename the project

## docs
lol?

## TODO
pass through the rest of the trufflehog options
