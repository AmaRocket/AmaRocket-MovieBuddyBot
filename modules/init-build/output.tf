
output "db_pass" {
  value = aws_ssm_parameter.db_pass.value
  sensitive = true
}

output "token"{
    value = aws_ssm_parameter.token.arn
    
}

output "api_key"{
    value = aws_ssm_parameter.api_key.arn
    
}

output "ecr_repository_url" {
  description = "Returns  url of created repository"
  value = aws_ecr_repository.ecr_repository.repository_url
}
output "app_name" {
  description = "Returns  name of created repository"
  value = local.repository_name
}

