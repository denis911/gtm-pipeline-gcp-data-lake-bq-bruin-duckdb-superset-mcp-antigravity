# GTM Intelligence Pipeline (Github Signals)

This repository implements a production-ready GTM intelligence pipeline that extracts technology-related signals from Github Archive and materializes them into a structured BigQuery Fact table for analysis.

## 🚀 Accomplishments
- **Automated Ingestion**: Python script (`ingest_github_signals.py`) fetches Github Archive data, uploads it to GCS as Parquet, and automatically manages a BigQuery external table.
- **Robust Transformation**: SQL asset (`fct_growth_signals.sql`) transforms raw signals into a structured fact table with partitioning and clustering.
- **Variable Injection**: Resolved complex Jinja rendering issues in Bruin v0.11 by correctly using the `var` namespace.
- **Scalable Architecture**: Uses Hive partitioning on GCS, enabling efficient incremental processing.

## 📁 Pipeline Components
1. **Ingestion Layer**: `ingest_github_signals.py`
   - Fetches signals (WatchEvent, PushEvent, etc.) for tech keywords.
   - Saves to GCS with Hive Partitioning (`date=YYYY-MM-DD`).
   - Registers a BigQuery External Table `ext_github_signals`.
2. **Transformation Layer**: `fct_growth_signals.sql`
   - Quantifies signals and extracts company names from repository paths.
   - Materializes the `gtm_intelligence_dwh.fct_growth_signals` table.
   - Partitioned by `signal_date` and clustered by `company_name`.

## 🛠️ Execution Instructions
Set the following environment variables:
```bash
export GCP_PROJECT_ID="your-project"
export DATA_LAKE_BUCKET="your-bucket"
export BIGQUERY_DATASET="gtm_intelligence_dwh"
```

Run the pipeline:
```bash
# Validate
bruin validate .

# Run Full Pipeline
bruin run . --start-date 2026-03-19
```

## 📊 Exploration & Visualization
The final data resides in BigQuery: `gtm_intelligence_dwh.fct_growth_signals`.

### Superset Deployment (Planned)
We are currently evaluating deployment options for Apache Superset to make the signals visible to an external audience:
- **Cloud (Preset.io)**: Managed Superset with easy public dashboard sharing.
- **GCP Self-Hosted**: Deploying Superset via Docker on a Google Compute Engine VM.

---
Happy Building! For more information on Bruin concepts, visit the [Bruin Documentation](https://getbruin.com/docs/).
