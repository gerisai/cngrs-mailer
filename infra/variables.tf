variable "image_tag" {
  type        = string
  description = "Docker image tag to use for CNGRS Mailer"
  default     = "latest"
}

variable "sender_address" {
  type        = string
  description = "From address"
}

variable "assets_url" {
  type        = string
  description = "Static assets URL to embed into emails"
}

variable "base_cngrs_url" {
  type        = string
  description = "Base CNGRS URL"
}
