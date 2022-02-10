variable "name" {
    description = " Enter name"
    default = "test"
    
}
variable "env"{
    description = " Enter env"
   
}

variable "aws_region" {
    description = " Enter region"
    default = "eu-central-1"
    
}
# variable "app_image" {
#     default = "000000000000.dkr.ecr.eu-west-1.amazonaws.com/image"
  
# }

#ECS

#variable "ecr_repository_url"{} 
variable "image_tag"{}



variable "port" {
    description = "Enter port of image"
    default = "80"
  
}


#ASG

variable "inst_number" {
    description = "enter number of tasks"
    default = 1 
}
variable "instance_type"{
    description = " Enter instance type"
    default          = "t2.micro"
}

variable "task_cpu" {
    default = "768"
  
}

variable "task_memory" {
    default = "768"
  
}

#SG
variable "allow_ports"{
    description = "list of open ports"
    type = list
    default = ["80","22"]
}

#VPC

variable "Sub_count"{
    description = "count of subnets and av.zones" 
    default = "2"   
   
}


variable "VPC_Sidr_block"{
    description = "enter cidr block"
    type = string
    default = "10.0.0.0/16"
}

variable "aws_profile" {} 

#RDS
variable "db_instance_type"{
    default= "db.t2.micro"
}


#SSM
# variable "db_pass"{
#    # default = "test1324678"
# }

# variable "token"{
    
# }

# variable "api_key"{
    
# }