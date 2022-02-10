/*
data "aws_ami" "latest_amazon" {
    owners = ["amazon"]
    most_recent = true
    filter {
      name="name"
      values =["amzn-ami-*-amazon-ecs-optimized"]
    }
  
}
*/
data "aws_ssm_parameter" "ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
}



#~~~~~~~~~~~~~~~~~~~~~~launch config~~~~~~~~~~~~~~~~~~~~~~~~
resource "aws_launch_configuration" "web" {
  
  name_prefix =    "${var.name}-${var.env}-"
  image_id      = data.aws_ssm_parameter.ami.value
  instance_type = var.instance_type
  security_groups = [aws_security_group.SG.id]
  user_data = "#!/bin/bash\necho ECS_CLUSTER=${var.name}-${var.env} >> /etc/ecs/ecs.config"
  key_name = "axel-key-frankfurt"
  iam_instance_profile        = aws_iam_instance_profile.profile_for_EC2.name 
  lifecycle {
    create_before_destroy =true
  }
  
}

#~~~~~~~~~~~~~~~~~~~~~~ASG~~~~~~~~~~~~~~~~~~~~~~~~

resource "aws_autoscaling_group" "my_web_asg" {
    depends_on                = ["aws_launch_configuration.web"]
      name          = "${var.name}_${var.env}_ASG_${aws_launch_configuration.web.name}"
     
      launch_configuration = aws_launch_configuration.web.name
      min_size = 1
      max_size =4
      desired_capacity   = 1
      #min_elb_capacity =2
      vpc_zone_identifier = [for subnet in aws_subnet.private : subnet.id] 
      health_check_type = "EC2"
     # target_group_arns = [aws_lb_target_group.my_web_tg.arn]
      dynamic "tag"{
          for_each={
              Name = "${var.name}-${var.env}-ASG"
             
          }
     content {
           key =tag.key
           value = tag.value
           propagate_at_launch = true

           }
      }

    lifecycle {
    create_before_destroy =true
  }
  
        
}

/*
resource "aws_autoscaling_attachment" "asg_attachment_to_lb" {
  autoscaling_group_name = aws_autoscaling_group.my_web_asg.id
  alb_target_group_arn   = aws_lb_target_group.my_web_tg.arn
   lifecycle {
    create_before_destroy =true
  }
  
}
*/