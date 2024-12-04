resource "aws_ecr_repository" "cngrs-mailer" {
  name                 = "cngrs-mailer"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
