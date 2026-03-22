variable "project_id" {
  description = "The GCP project ID to deploy to."
  type        = string
}

variable "region" {
  description = "The region to deploy resources to."
  type        = string
  default     = "us-central1"
}
