## overview
```
[[  QUEUE  ]]  # stdin, sqs
      |
[[   JOB   ]]  # trufflehog, pydriller
     /|\
[[ OUTPUTS ]]  # stdout, s3
```

## examples
install deps
```bash
python3 -m venv /tmp/epicgamermoment
source /tmp/epicgamermoment/bin/activate
pip install -r requirements.txt
```

`stdin -> trufflehog + pydriller -> stdout`
```
echo cqsd test | python3 example-stdin.py
```

`sqs -> trufflehog + pydriller -> s3`
Prerequisites: SQS queue and S3 bucket (see `./terraform/`)
```bash
for msg in $(github list-repos user cqsd); do
    aws sqs send-message \
        --queue-url "${QUEUE_URL}" \
        --message-body="$msg"
done

python3 example-sqs.py
aws s3 ls --recursive "s3://${BUCKET_NAME}"
```

goobernetes example in `./manifests/`
```bash
docker build -t trufflehonk:v0.1.1 .
kubectl apply -f manifests/sqs-job-example.yaml
```

## docs
lol
