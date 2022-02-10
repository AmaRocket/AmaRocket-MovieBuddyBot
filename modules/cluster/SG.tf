resource "aws_security_group" "SG" {
  name        = "${var.name}_${var.env}-_Sg"
  vpc_id      = aws_vpc.main.id



  dynamic "ingress"{
    for_each =var.allow_ports
    content{
      
    from_port   = ingress.value
    to_port     = ingress.value
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

    }
     }
      egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]

  }
 
  
}

resource "aws_security_group" "DB_SG" {
  name        = "${var.name}_${var.env}-_DB_Sg"
  vpc_id      = aws_vpc.main.id



  dynamic "ingress"{
    for_each =var.allow_ports
    content{
      
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

    }
     }
      egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]

  }
 
  
}