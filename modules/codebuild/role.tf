resource "aws_iam_role" "role_for_code_build" {
  name               = "codebulild-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}


resource "aws_iam_policy" "policy_for_codeBuild" {
  name = "${var.name}-codebuild-access-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:CompleteLayerUpload",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeVpcs",
                "ec2:DescribeAvailabilityZones ",
                "ec2:CreateNetworkInterfacePermission",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "logs:ListTagsLogGroup",
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "codebuild:CreateReportGroup",
                "codebuild:CreateReport",
                "codebuild:UpdateReport",
                "codebuild:BatchPutTestCases",
                "codebuild:BatchPutCodeCoverages",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:PassRole",
                "iam:ListInstanceProfilesForRole",
                "iam:ListRolePolicies",
                "iam:ListAttachedRolePolicies",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:ListEntitiesForPolicy",
                "iam:GetInstanceProfile",
                "iam:*",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",                
                "autoscaling:DescribeTags",
                "autoscaling:SetDesiredCapacity",
                "autoscaling:*",
                              
                "ssm:*",
                "dynamodb:*",
                "rds:*",
                "s3:*",
                "ecs:*",
                "ec2:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      },

{
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterfacePermission"
            ],
            "Resource": "arn:aws:ec2:${var.aws_region}:*:network-interface/*",
            "Condition": {
                "StringEquals": {
                  "ec2:AuthorizedService": "codebuild.amazonaws.com"
                },
                "ArnEquals": {
                  "ec2:Subnet": [
                    "arn:aws:ec2:${var.aws_region}:*:subnet/*"
                  ]
                }
            }
        }


    ]
  })
}

resource "aws_iam_policy_attachment" "attach_for_ecs" {
  name       = "attach-attach"
  roles      = [aws_iam_role.role_for_code_build.name]
  policy_arn = aws_iam_policy.policy_for_codeBuild.arn
}
