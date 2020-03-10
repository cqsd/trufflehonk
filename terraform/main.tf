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
