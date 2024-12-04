data "aws_iam_policy_document" "mailer_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_policy" "cngrs_mailer_policy" {
  name        = "cngrs_mailer_policy"
  path        = "/"
  description = "CNGRS Mailer Policy to consume AWS APIs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendRawEmail"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "cngrs_mailer_role" {
  name               = "${local.app_name}-role"
  assume_role_policy = data.aws_iam_policy_document.mailer_assume_role.json
}

resource "aws_iam_role_policy_attachment" "cngrs_mailer_sqs_policy_attachment" {
  role       = aws_iam_role.cngrs_mailer_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

resource "aws_iam_role_policy_attachment" "cngrs_mailer_ses_policy_attachment" {
  role       = aws_iam_role.cngrs_mailer_role.name
  policy_arn = aws_iam_policy.cngrs_mailer_policy.arn
}
