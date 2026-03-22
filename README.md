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

### Superset Deployment (Preset.io)
We use [Preset.io](https://preset.io) (Managed Superset) to make our dashboards public.

#### 1. Create GCP Service Account
For Preset to access BigQuery, you need a Service Account JSON key:
1. Go to **IAM & Admin > Service Accounts** in GCP Console.
2. Click **Create Service Account** (e.g., `superset-viewer`).
3. Grant roles: `BigQuery Data Viewer` and `BigQuery Job User`.
4. Click into the new account > **Keys** tab > **Add Key** > **Create New Key** (JSON).
5. **DO NOT COMMIT THIS FILE**. Save it locally to upload to Preset.

#### 2. Connect Preset to BigQuery
1. Sign up for a free Preset account.
2. Go to **Settings > Database Connections > New Database**.
3. Select **Google BigQuery**.
4. Upload your Service Account JSON file.
5. Set `Project ID` to `evident-axle-339820` and `Dataset` to `gtm_intelligence_dwh`.

### Dashboard-as-Code
Superset allows exporting dashboards as YAML/ZIP files. Once you design your dashboard in Preset:
1. Select your dashboard > **Export**.
2. Save the resulting file in the `dashboards/` directory of this repo.
3. This ensures the visual layer is versioned alongside your data pipeline.

---
Happy Building! For more information on Bruin concepts, visit the [Bruin Documentation](https://getbruin.com/docs/).
