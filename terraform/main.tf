
terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
    config = {
      source = "alabuel/config"
      version = "0.2.8"  
    }
  }
}
provider "config" {}

data "config_ini" "cfg" {
  ini = file("../config.ini")
}

locals {
  value = jsondecode(data.config_ini.cfg.json)["GCP"]
}



provider "google" {
  project = local.value["project"]
  region = local.value["region"]
  credentials = file(local.value["GCP_KEY"])  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.value["data_lake_bucket"]}_${local.value["project"]}" # Concatenating DL bucket & Project name for unique naming
  location      = local.value["region"]

  # Optional, but recommended settings:
  storage_class = local.value["storage_class"]
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = local.value["BQ_DATASET"]
  project    = local.value["project"]
  location   = local.value["region"]
}
