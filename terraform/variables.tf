variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "db_username" {
  type        = string
  description = "Administrator username for RDS Postgres"
  default     = "storevault_admin"
}

variable "db_password" {
  type        = string
  description = "Database master password"
  sensitive   = true
}