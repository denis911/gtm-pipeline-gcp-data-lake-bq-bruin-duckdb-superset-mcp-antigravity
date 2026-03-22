# 🚀 GTM Intelligence Engine: High-Growth Signal Pipeline

Building GTM pipeline using GCP buckets, Bruin  and Bigquery or duckdb for local processing with superset MCP server and antigravity - everything-as-a-code

## 📖 The Problem: The "Signal-to-Noise" Gap
In modern Go-To-Market (GTM) operations, sales teams are drowning in lead lists that are "stale" or "generic." Standard databases (Apollo/ZoomInfo) often lag behind real-world growth events.

**This project solves the "Integration Wall"** by building a production-grade Data Engineering foundation that identifies **High-Growth Intent signals** (e.g., specific tech adoption or hiring surges) directly from raw datasets, preparing them for autonomous AI Agents.

--

## 🧠 The "Relational Grounding" Advantage
Unlike basic AI outreach tools that rely on generic company names, this engine uses a **Structured Intent CSV** as its source of truth.

### Why this matters for GTM:
* **Tech-Stack Alignment:** We don't just find "OpenAI"; we find "OpenAI's interest in distributed systems" by matching their hiring requirements (from the CSV) with their actual engineering activity (GitHub stars).
* **Composite Scoring:** The engine calculates a "High-Growth Score" by joining two distinct signals:
    1.  **Direct Intent:** Open job roles and salary benchmarks (Structured CSV).
    2.  **Implicit Intent:** Active repo engagement and tech adoption (GitHub Archive).
* **Precision Filtering:** By using the CSV as a lookup table, we reduce "API Noise" and ensure that enrichment credits (FullEnrich/Clay) are only spent on accounts with a proven hiring budget.

> **Why is this approach different from others:** This architecture solves the "Integration Wall" by ensuring the AI Agent has a structured "memory" of the target market before it ever sends an email.

--

## 🛠 The 2026 Tech Stack (Everything-as-Code)
Unlike traditional stacks, this project uses a unified "as-code" approach to ensure 100% reproducibility and agent-friendliness:

* **Infrastructure:** Terraform (GCP) - Manages BigQuery & GCS.
* **Orchestration & Transformation:** [Bruin](https://getbruin.com/) - A single-binary tool replacing both Airflow and dbt.
* **Data Warehouse:** Google BigQuery (Partitioned by date, Clustered by Company).
* **Visualization:** Apache Superset (Preset) - Semantic-layer based dashboards.
* **Automation Layer:** Built for seamless integration with Clay, n8n, and Composio.

--

## 📐 Data Architecture
1.  **Ingestion (Datalake):** Raw data (GitHub Archive / Job Board CSVs) is pulled via Bruin Python tasks and stored as Parquet in **GCS**.
2.  **Warehouse (DWH):** Data is moved to **BigQuery** external tables.
3.  **Transformation:** Bruin SQL tasks calculate "Growth Velocity" (Company activity WoW/MoM).
4.  **Semantic Layer:** Data is exposed to Superset for visualization and Clay for GTM execution.

--

## 📊 Zoomcamp Compliance & Evaluation
This project meets all requirements for the Data Engineering Zoomcamp Capstone:
* **Cloud & IaC:** Full GCP deployment managed via Terraform.
* **Orchestration:** End-to-end DAG managed by Bruin.
* **DWH Optimization:** Tables are **Partitioned** by `ingestion_date` and **Clustered** by `company_domain` to optimize query costs (crucial for GTM scale).
* **Dashboard:** Two-tile Superset dashboard showing:
    1.  *Categorical:* Lead distribution by Industry/Tech Stack.
    2.  *Temporal:* Growth signal volume over a 30-day rolling window.

--

## 🚀 How to Run
1. **Infrastructure:** `cd terraform && terraform apply`
2. **Run Pipeline:** `bruin run`
3. **Visualize:** Connect Superset to your BigQuery `fct_growth_signals` table.

--

## 💰 Cost-Aware Engineering (Free Tier Strategy)
This project is architected to run **entirely within the Google Cloud "Always Free" tier**. It is designed for students, hackathon participants, and small startups who need production-grade infra without the bill.

### ⚖️ Technical Constraints & "Gotchas"
* **GCP Region:** Resources are locked to `us-central1`. This is mandatory to qualify for the GCS 5GB Free Storage tier.
* **BigQuery Sandbox:** If running without a credit card, BigQuery operates in "Sandbox Mode." 
    * *Limitation:* Tables will have a **60-day expiration date**. 
    * *Solution:* Our `bruin` pipeline is idempotent; you can simply re-run the pipeline to recreate tables if they expire.
* **Data Lake Lifecycle:** I have implemented a **30-day auto-delete rule** in Terraform for raw files. This ensures your storage never exceeds the 5GB limit while maintaining enough history for development.
* **Compute:** This project uses the **Bruin CLI** (local/CI runner) rather than a heavy managed service like Composer (managed Airflow), saving ~$350/month in idle costs.

### 🛠 How to keep it free:
1. Ensure your Terraform `project_id` matches a project with the BigQuery API enabled.
2. Do not change the `storage_class` from `STANDARD` in `main.tf`.
3. Stay within 1TB of query processing per month (virtually impossible to hit with this dataset).

--

## Setting up GCP credentials for local development

Before trying to set up a service account, run these three commands in your terminal:

```bash
# 1. Login to the CLI (as the person)
gcloud auth login
# after login the confirmation page opens at https://docs.cloud.google.com/sdk/auth_success
# << You are now authenticated with the gcloud CLI! >>
# run << gcloud components update >> from admin console if needed

# 2. Login for the Code (as the developer)
gcloud auth application-default login

# 3. Explicitly set your project (replaces your PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID
# set up quotas if needed:
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

Quick Check:

Go to the GCP Console BigQuery API page:
<<https://console.cloud.google.com/apis/library/bigquery.googleapis.com>>

Ensure it says "API Enabled."

Double check in the bash terminal too:

```bash
gcloud services enable bigquery.googleapis.com bigquerystorage.googleapis.com storage.googleapis.com storage-api.googleapis.com

gcloud services list --enabled | grep bigquery
```

```bash
gcloud services enable \
  bigquery.googleapis.com \
  bigquerystorage.googleapis.com \
  storage.googleapis.com \
  storage-api.googleapis.com \
  --project YOUR_PROJECT_ID
```

--

## 🛠 Infrastructure Commands (Phase 1)

This project uses **Terraform** to manage GCP resources. Follow these steps to deploy the infrastructure.

### 1. Initialize Terraform
This command downloads the necessary provider plugins (Google Cloud provider).
```bash
cd terraform
terraform init
```

### 2. Validate Configuration
Check for syntax errors and internal consistency.
```bash
terraform validate
```

### 3. Preview Changes (Plan)
Generate an execution plan to see exactly what will be created without making changes yet. Replace `YOUR_PROJECT_ID` with your actual GCP Project ID.
```bash
terraform plan -var="project_id=YOUR_PROJECT_ID" -out=tfplan
```

### 4. Deploy Infrastructure (Apply)
Apply the planned changes to your GCP project. This will create the GCS bucket and BigQuery dataset.

```bash
terraform apply "tfplan"
```

### 5. Cleanup (Destroy)
To avoid any unexpected costs when you're done testing, you can destroy all resources created by Terraform.
```bash
terraform destroy -var="project_id=YOUR_PROJECT_ID"
```

> [!IMPORTANT]
> - Ensure all tables in BigQuery are deleted (or `delete_contents_on_destroy = true` as set in our `main.tf`).
> - This command will remove the GCS bucket and all its contents.

> [!NOTE]
> Resources managed by this Terraform:
> - **GCS Bucket:** `${PROJECT_ID}-data-lake` (US-CENTRAL1, 30-day auto-delete).
> - **BigQuery Dataset:** `gtm_intelligence_dwh` (US-CENTRAL1).

--

## ⚙️ Pipeline Setup (Phase 2 - Bruin)

After the infrastructure is ready, we set up the **Bruin** orchestration layer.

### 1. Environment Variables (`.env`)
Create a `.env` file in the root directory to store your project details. This file is ignored by git for security.

```bash
GCP_PROJECT_ID=YOUR_PROJECT_ID
DATA_LAKE_BUCKET=YOUR_PROJECT_ID-data-lake
BIGQUERY_DATASET=gtm_intelligence_dwh
```

### 2. Bruin Configuration (`bruin.yaml`)
The pipeline uses the environment variables to connect to BigQuery. The connection is named `bq_gtm` and uses **Application Default Credentials (ADC)**.

To verify your Bruin setup:
```bash
bruin --version
```

To validate your pipeline (once tasks are added):
```bash
bruin validate .
```

--

## Terraform

NB - to use Terraform properly we need to make sure services enabled as per above:

```bash
gcloud services enable bigquery.googleapis.com bigquerystorage.googleapis.com storage.googleapis.com storage-api.googleapis.com

# or for specific project
gcloud services enable \
  bigquery.googleapis.com \
  bigquerystorage.googleapis.com \
  storage.googleapis.com \
  storage-api.googleapis.com \
  --project YOUR_PROJECT_ID
```
