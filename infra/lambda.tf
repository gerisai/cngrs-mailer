resource "aws_lambda_function" "cngrs_mailer" {
  function_name = local.app_name
  role          = aws_iam_role.cngrs_mailer_role.arn

  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.cngrs-mailer.repository_url}:${var.image_tag}"
  architectures = ["x86_64"]

  timeout = 120

  ephemeral_storage {
    size = 512
  }

  environment {
    variables = {
      ENV            = "Production"
      LOG_LEVEL      = "INFO"
      SENDER_ADDRESS = var.sender_address
      ASSETS_URL     = var.assets_url
      BASE_CNGRS_URL = var.base_cngrs_url
    }
  }
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.cngrs_mail_queue.arn
  function_name    = aws_lambda_function.cngrs_mailer.arn
}
