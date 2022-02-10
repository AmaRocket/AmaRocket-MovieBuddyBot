terraform {
  source = "../../../modules//cluster"
}

include {
  path = find_in_parent_folders()
}


dependencies {
    paths = ["../init-build"]
}