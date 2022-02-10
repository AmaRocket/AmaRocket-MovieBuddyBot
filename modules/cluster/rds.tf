resource "aws_db_subnet_group" "default" {
  name = "${var.name}-${var.env}-db-subnet-group"

  subnet_ids = aws_subnet.private.*.id

 
}

data "aws_ssm_parameter" "db_pass" {
  name = "/${var.name}/${var.env}/database/password/master"
}


resource "aws_db_instance" "default" {
  allocated_storage         = 20
  backup_window             = "03:00-04:00"
  ca_cert_identifier        = "rds-ca-2019"
  db_subnet_group_name      = aws_db_subnet_group.default.name
  engine_version            = "12.5"
  engine                    = "postgres"
  identifier                = var.env
  instance_class            = var.db_instance_type
  maintenance_window        = "sun:08:00-sun:09:00"
  name                      = var.name
  parameter_group_name      = "default.postgres12"
  password                  = data.aws_ssm_parameter.db_pass.value
  username                  = "postgres"
  vpc_security_group_ids  = [aws_security_group.DB_SG.id]
  skip_final_snapshot       = true
}

