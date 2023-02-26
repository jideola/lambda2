# Terraform Settings Block
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      #version = "~> 3.21" # Optional but recommended in production
    }
  }
}

# Provider Block
provider "aws" {
  profile = "default" # AWS Credentials Profile configured on your local desktop terminal  $HOME/.aws/credentials
  region  = "us-east-1"
}


terraform {
  backend "s3" {
    bucket          = "cw-lambda-tf-state" ### for storing state file
    dynamodb_table  = "cw-lambda-tf-lock" ### For locking the state file
    key             = "cw-lambda/terraform.tfstate" # This specifies the a path, folder/name-of-state-file
    region          = "us-east-1"
    encrypt         = true
  }
}