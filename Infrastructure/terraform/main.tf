# IBM's module.
# It will download the module when run "terraform init"

terraform {
required_providers {
    ibm = {
    source = "IBM-Cloud/ibm"
    }
 }
}

provider "ibm" {
    ibmcloud_api_key   = var.ibmcloud_api_key
    region = var.region
}

## This will create a resource group
## It separates the resources used inside IBM's cloud

data "ibm_resource_group" "group" {
    name = var.resource_group_name
  }

 # This part will deploy a Watson machine learning resource

  resource "ibm_resource_instance" "WML_ml1" {
    name              = "WML_ml1"
    service           = "pm-20"
    plan              = "lite"
    location          = "us-south"
    resource_group_id = data.ibm_resource_group.group.id
    tags              = ["TEST", "TERRAFORM"]

  }



 # This deploys a IBM Cloud Object Storage resource

  resource "ibm_resource_instance" "COS_ml1" {
    name              = "COS_ml1"
    service           = "cloud-object-storage"
    plan              = "lite"
    location          = "global"
    resource_group_id = data.ibm_resource_group.group.id
    tags              = ["TERRAFORM", "TEST"]

  }