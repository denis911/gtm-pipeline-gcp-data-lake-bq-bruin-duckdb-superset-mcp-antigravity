provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS Bucket for Data Lake
resource "google_storage_bucket" "data_lake" {
  name                        = "${var.project_id}-data-lake"
  location                    = var.region
  storage_class               = "STANDARD"
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery Dataset for Data Warehouse
resource "google_bigquery_dataset" "gtm_dwh" {
  dataset_id                  = "gtm_intelligence_dwh"
  location                    = var.region
  description                 = "GTM Intelligence Data Warehouse"
  delete_contents_on_destroy  = true
}
