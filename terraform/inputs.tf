variable region {
  type = string
}

variable queue_name {
  type = string
}

variable max_message_size {
  type        = number
  default     = 2048
  description = "Maximum message size in KB"
}

variable message_retention_seconds {
  type    = number
  default = 3600 // 1 hour
}
