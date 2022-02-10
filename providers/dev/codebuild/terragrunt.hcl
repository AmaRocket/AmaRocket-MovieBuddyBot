terraform {
  source = "../../../modules//codebuild"
  #autorun code build after apply
after_hook "run_sums" {
    commands = [
      "apply"
    ]

    execute = [
      "aws",
      "codebuild",
      "start-build",
      "--project-name",
      "${dependency.init-build.outputs.app_name}"
     
    ]

    run_on_error = false
  }

 }

include {
  path = find_in_parent_folders()
}



dependency "init-build" {
  config_path = "../init-build"
  mock_outputs = {
      ecr_repository_url = "000000000000.dkr.ecr.eu-west-1.amazonaws.com/image"
  }
  
}


dependency "cluster" {
  config_path = "../cluster"
  mock_outputs = {
    vpc_id          = "vpc-000000000000"
    private_ids = ["subnet-00000000000", "subnet-111111111111"]
  }
}


inputs =  {
    ecr_url = dependency.init-build.outputs.ecr_repository_url
    vpc_id = dependency.cluster.outputs.vpc_id
    subnet_id = dependency.cluster.outputs.private_ids
    build_spec_file = "providers/dev/buildspec.yml"
  }
