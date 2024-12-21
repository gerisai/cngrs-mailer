resource "aws_sqs_queue" "cngrs_mail_queue" {
  name                       = "${local.app_name}-queue.fifo"
  max_message_size           = 2048
  visibility_timeout_seconds = 120
  message_retention_seconds  = 3600
  receive_wait_time_seconds  = 10
  fifo_queue                 = true
}