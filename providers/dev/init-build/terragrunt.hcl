terraform {
  source = "../../../modules//init-build"
}

include {
  path = find_in_parent_folders()
}




locals {
  secrets = read_terragrunt_config(find_in_parent_folders("secrets.hcl"))
}

inputs = local.secrets.inputs