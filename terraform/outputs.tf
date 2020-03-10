output queue_arn {
  value = aws_sqs_queue.main.arn
}

output queue_url {
  value = aws_sqs_queue.main.id
}

output rw_policy_name {
  value       = aws_iam_policy.queue_rw.name
  description = "Name of a Policy that allows full access to queue messages"
}

output rw_policy_arn {
  value       = aws_iam_policy.queue_rw.arn
  description = "ARN of a Policy that allows full access to queue messages"
}
