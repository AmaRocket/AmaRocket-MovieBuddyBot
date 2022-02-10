variable "vpc_id" {
  
}

variable "subnet_id" {
type        = list(string)
  default     = null
  
}
variable "aws_profile" {} 
variable "name" {
  
}

variable "env" {
  
}

variable "aws_region" {} 

variable "repo_url"{}
variable "branch_pattern" {
  
}

variable "git_trigger_event" {
  
}

variable "ecr_url" {}
 
variable "build_spec_file"{}
#variable "github_token" {}

