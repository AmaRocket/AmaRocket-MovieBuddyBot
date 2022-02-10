resource "aws_ssm_parameter" "db_pass" {
  name        = "/${var.name}/${var.env}/database/password/master"
  description = "The parameter description"
  type        = "SecureString"
  value       = var.db_pass
  overwrite =true
}

resource "aws_ssm_parameter" "token" {
  name        = "/${var.name}/${var.env}/telegramtoken"
  description = "The parameter description"
  type        = "SecureString"
  value       = var.token
  overwrite =true
}

resource "aws_ssm_parameter" "api_key" {
  name        = "/${var.name}/${var.env}/tmdbtoken"
  description = "The parameter description"
  type        = "SecureString"
  value       = var.api_key
  overwrite =true
}

resource "aws_ssm_parameter" "github_token" {
  name        = "/${var.name}/${var.env}/gittoken"
  description = "The parameter description"
  type        = "SecureString"
  value       = var.github_token
  overwrite =true
}

resource "aws_ssm_parameter" "ecr_url" {
  name        = "/${var.name}/${var.env}/ecrurl"
  description = "The parameter description"
  value       = aws_ecr_repository.ecr_repository.repository_url
  type        = "String"
  overwrite =true
  depends_on = [aws_ecr_repository.ecr_repository]
}

resource "aws_ssm_parameter" "admin_id" {
  name        = "/${var.name}/${var.env}/adminid"
  description = "The parameter description"
  value       = var.admin_id
  type        = "String"
  overwrite =true
  
}


