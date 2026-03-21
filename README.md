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

