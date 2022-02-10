#create role for ecs-tasks
resource "aws_iam_role" "role_for_ecs_tasks" {
  name               = "${var.name}-${var.env}-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": ["ecs-tasks.amazonaws.com"]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}
# create policy to access  ECR and logs
resource "aws_iam_policy" "policy_for_ecs" {
  name = "${var.name}-${var.env}-ecr-access-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ssm:GetParameters"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}
 
 
# attaching policy to role
resource "aws_iam_policy_attachment" "attach_for_ecs" {
  name       = "${var.name}-${var.env}-attach"
  roles      = [aws_iam_role.role_for_ecs_tasks.name]
  policy_arn = aws_iam_policy.policy_for_ecs.arn
}


#####################################EC2


resource "aws_iam_role" "role_for_EC2" {
  name               = "${var.name}-${var.env}-EC2-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": ["ec2.amazonaws.com"]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

resource "aws_iam_policy" "policy_for_EC2" {
  name = "${var.name}-${var.env}-ec2-access-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:DescribeTags",
                "ecs:CreateCluster",
                "ecs:DeregisterContainerInstance",
                "ecs:DiscoverPollEndpoint",
                "ecs:Poll",
                "ecs:RegisterContainerInstance",
                "ecs:StartTelemetrySession",
                "ecs:UpdateContainerInstancesState",
                "ecs:Submit*",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ssm:GetParameters"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "attach_for_EC2" {
  name       = "${var.name}-attach"
  roles      = [aws_iam_role.role_for_EC2.name]
  policy_arn = aws_iam_policy.policy_for_EC2.arn
}

resource "aws_iam_instance_profile" "profile_for_EC2" {
  name = "${var.name}--instance-profile"
  role = aws_iam_role.role_for_EC2.name

}
