resource aws_s3_bucket main {
  bucket = var.bucket_name
}

data aws_iam_policy_document main {
  statement {
    sid    = "a"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObjectAcl",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObjectAcl",
    ]
    resources = [
      "arn:aws:s3:::${var.bucket_name}",
      "arn:aws:s3:::${var.bucket_name}/*"
    ]
  }
}

resource aws_iam_policy main {
  name        = "trufflemog-${var.bucket_name}-rw"
  description = "trufflemog-${var.bucket_name}-rw"
  policy      = data.aws_iam_policy_document.main.json
}

resource aws_sqs_queue main {
  name                      = var.queue_name
  max_message_size          = var.max_message_size
  message_retention_seconds = var.message_retention_seconds
  // other options? don't care for now :)
}

data aws_iam_policy_document queue_rw {
  statement {
    sid    = "AllowSqsSendReceiveDelete"
    effect = "Allow"

    actions = [
      "sqs:ReceiveMessage",
      "sqs:SendMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]

    resources = [
      aws_sqs_queue.main.arn
    ]
  }
}

resource aws_iam_policy queue_rw {
  name        = "${var.queue_name}-sqs-rw"
  description = "Allow send/receive/delete messages in ${var.queue_name}"
  policy      = data.aws_iam_policy_document.queue_rw.json
}
