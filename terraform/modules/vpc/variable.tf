variable "vpc_cidr" {
  description = "CIDR block for the ShopFlow VPC"
  type        = string
}

variable "environment" {
  description = "Environment name (production)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "shopflow"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "Availability zones for ShopFlow"
  type        = list(string)
}