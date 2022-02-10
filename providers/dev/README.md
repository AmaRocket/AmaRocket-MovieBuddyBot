Tools versions:

    Terraform - 1.0.11
    Terragrunt - 0.36.1
    AWS Cli - 2.0.42


repo contains the next components:

    Application itself
    Terragrunt deployment configuration
    Terraform modules
        Cluster - Creates a ECS Cluster and related services
        Codebuild - Creates an AWS Codebuild job which starts automatically when code pushed to "develop" branch
        Init-Build - Creats variables  for cluster

Configuration

Main configuration files are the next:

/providers/dev/terragrunt.hcl - Contains main variables for Terragrunt & Terraform:

    remote_state_bucket - S3 bucket for Terraform states
    envorinment - Environment name (dev, prod, etc)
    app_name - Name of Application (will be used for naming AWS resources)
    image_tag - Default value for Docker image tag. Will be used for initial build
    repo_url - GitHub repo URL
    aws_profile - The name of AWS Profile
    aws_account - AWS Account ID
    aws_region - AWS Region for creating resources
    branch_pattern - Which branch changes should webhook watch on (e.g.: "^refs/heads/develop$")
    git_trigger_event - Event for git webhook
    app_count = Number of launched applications. In our case 1
    cluster_count = Number of cluster instances
    subnet_count = Number of avzones

Deployment
Preparation

    Install the required versions of Terragrunt and Terraform
    Configure AWS Cli for your account (see here)
    Download the repo content
    Update "locals" block in providers/dev/terragrunt.hcl file
    Create "secrets.hcl" file and add db password tmdi_api and bot token:

inputs = {
  github_token = "Private Github token"
  token = "Telegram bot token"
  api_key = "TMDB API key"
  db_pass = "DB password"
  admin_id = "admin_id"
}

One command deployment

    Go to the /providers/dev directory and run:

terragrunt run-all init

    Then...

terragrunt run-all apply

Step by step deployment

Step by step deployment should be done in the next order:

    Initial build (providers/dev/init-build)
    Cluster creation (providers/dev/ecs-cluster)
    Codebuild job setup (providers/dev/codebuild)

Go to each folder one by one and run:

terragrunt plan

    When plan is completed run:

terragrunt apply

    Go to the next directory when deployment completed.

When resources creation is finished you can push a new version to "develop" branch of the repo you described in env.hcl file to initiate a new build
Destroy infrastructure

You can destroy everything you deployed with the next command which should be executed in dev/ directory:

terraform run-all destroy

Or you can destroy components step by step in reverse order from deployment. Go to the appropriate directory and run:

terragrunt destroy

Manual Version Rollback

In some cases you may need to rollback current version running on ECS. This can be done manually using Teraform & Terragrunt.

Before running Terragrunt you should go to Elastic Container Registry and select the tag of image you want to run on ECS. Then follow the next steps:

cd providers/dev/cluster && terragrunt plan --var image_tag="TAG_OF_REQUIRED_IMAGE"

Then review generated plan and if you agree to incoming changes, run:

terragrunt apply --var image_tag="TAG_OF_REQUIRED_IMAGE"

