
terraform {
  required_version = ">= 1.10.0"


  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "shopflow-tfstate-390663897243-ap-southeast-2"
    key          = "shopflow/prod/terraform.tfstate"
    region       = "ap-southeast-2"
    use_lockfile = true
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr     = "10.0.0.0/16"
  environment  = "production"
  project_name = "shopflow"

  public_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]

  private_subnet_cidrs = [
    "10.0.11.0/24",
    "10.0.12.0/24"
  ]

  availability_zones = [
    "ap-southeast-2a",
    "ap-southeast-2b"
  ]

}

module "iam" {
  source = "../../modules/iam"

  project_name = "shopflow"
  environment  = "production"
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = "shopflow"

  services = [
    "product-service",
    "order-service",
    "payment-service",
    "notification-service",
    "nginx"
  ]
}


module "eks" {
  source = "../../modules/eks"

  project_name = "shopflow"
  environment  = "production"

  eks_cluster_role_arn = module.iam.eks_cluster_role_arn
  eks_node_role_arn    = module.iam.eks_node_role_arn

  private_subnet_ids = module.vpc.private_subnet_ids

  kubernetes_version = "1.33"

  node_instance_type = "t3.medium"

  desired_size = 1
  min_size     = 1
  max_size     = 2

  depends_on = [
    module.iam
  ]
}


