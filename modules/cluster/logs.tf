#creating  loggin group
resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/ecs/${var.name}-${var.env}"
  retention_in_days = 30

  tags = {
    Name = "cb-log-group"
  }
}