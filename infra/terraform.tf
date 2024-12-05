terraform {
  required_version = ">= 1.9.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.57.0"
    }
  }

  backend "s3" {
    bucket = "tf-state-st"
    key    = "jidi/cngrs-mailer"
    region = "us-west-2"
  }
}

provider "aws" {
  region  = "us-west-2"
  profile = "jidi"
  default_tags {
    tags = {
      Environment = "Production"
      Project     = "CNGRS"
      App         = "cngrs-mailer"
    }
  }
}
