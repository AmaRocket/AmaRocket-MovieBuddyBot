
## import secrets variables from ssm 
resource "aws_ecs_cluster" "main" {
  name = "${var.name}-${var.env}"
}

data "aws_ssm_parameter" "token" {
  name = "/${var.name}/${var.env}/telegramtoken"
}
data "aws_ssm_parameter" "api_key" {
  name = "/${var.name}/${var.env}/tmdbtoken"
}
data "aws_ssm_parameter" "ecrurl" {
  name = "/${var.name}/${var.env}/ecrurl"
}
data "aws_ssm_parameter" "admin_id" {
  name = "/${var.name}/${var.env}/adminid"
}


locals {
app_image = format("%s:%s", data.aws_ssm_parameter.ecrurl.value, var.image_tag)
  
}

resource "aws_ecs_service" "test"{
    name = "${var.name}-${var.env}"
    cluster = aws_ecs_cluster.main.arn
    #scheduling_strategy = "DAEMON"
     launch_type            = "EC2"  
    deployment_maximum_percent = 200
    deployment_minimum_healthy_percent = 0
    desired_count = var.inst_number
    
    task_definition = aws_ecs_task_definition.main.arn

    network_configuration {
        security_groups = [aws_security_group.SG.id]
        subnets =aws_subnet.private.*.id     
        
    }
   

}
######################## Task definition #############################
#  template for  conteiner, all external variables are entered at this stage
resource "aws_ecs_task_definition" "main" {
 
 
 
     family = "${var.name}-${var.env}"
     network_mode             = "awsvpc"
     requires_compatibilities = ["EC2"]
     execution_role_arn = aws_iam_role.role_for_ecs_tasks.arn 
     cpu         = var.task_cpu
     memory      = var.task_memory



      container_definitions = jsonencode([{
   name        = "first"
   image       = local.app_image
   essential   = true
   cpu         = "${tonumber(var.task_cpu)}"
   memory      = "${tonumber(var.task_memory)}"

   environment = [
     {
       name ="PGHOST"
       value = "${aws_db_instance.default.address}"
     },
     {
       name ="ADMIN_ID"
       value = "${data.aws_ssm_parameter.admin_id.value}"
     },

     {
       name ="PG_PORT"
       value = "${tostring(aws_db_instance.default.port)}"
     },

     {
       name ="PG_USER"
       value = "${aws_db_instance.default.username}"
     },

     {
       name ="DB_NAME"
       value = "${aws_db_instance.default.name}"
     }

     
   ]
   
   secrets = [
     {
       name ="PG_PASS"
       valueFrom = "${data.aws_ssm_parameter.db_pass.arn}"
     },
     {
       name ="TOKEN"
       valueFrom = "${data.aws_ssm_parameter.token.arn}"
     },
     {
       name ="API_KEY"
       valueFrom = "${data.aws_ssm_parameter.api_key.arn}"
     }

     
   ]

   logConfiguration =  {
       logDriver = "awslogs"
       options ={
           awslogs-group = "/ecs/${var.name}-${var.env}"
           awslogs-region = var.aws_region
           awslogs-stream-prefix ="ecs"
       }
   }
   
   
   
      }])
 

 }