# **MASTER PROMPT: GTM Intelligence Engine (Zoomcamp \+ Hackathon Edition)**

## **🎯 MISSION**

Build a production-grade GTM (Go-to-market) Data Pipeline for my **Data Engineering Zoomcamp Capstone**. The project must identify "High-Growth Signals" (GitHub stars) for companies matching my tech stack in structured\_jobs.csv. It must be 100% "Everything-as-Code" and optimized for the **GCP Free Tier**.

## **🏗️ ARCHITECTURE**

1. **Infra (Terraform):** Setup GCP Project, GCS Bucket (US-Central1), and BigQuery Dataset.  
2. **Orchestration (Bruin):** Use Bruin (bruin.dev) to manage the Python Ingestion and SQL Transformations.  
3. **Data Lake (GCS):** Store raw data as partitioned Parquet files.  
4. **Warehouse (BigQuery):** Create a final Fact table partitioned by signal\_date and clustered by company\_domain.

## **🛠️ EXECUTION STEPS**

### **STEP 1: Infrastructure (Terraform)**

Create a terraform/ directory. Use a globally unique bucket name: ${GCP\_PROJECT\_ID}-data-lake.

* **Region:** us-central1 (Mandatory for Free Tier).  
* **Lifecycle:** Add a rule to delete GCS objects after 30 days.  
* **Dataset:** gtm\_intelligence\_dwh.

### **STEP 2: Pipeline Config (Bruin)**

Initialize Bruin and create a bruin.yaml.

* Define connection bq\_gtm using environment variable GCP\_PROJECT\_ID.  
* Define environment variables for the bucket name and dataset.

### **STEP 3: Python Ingestion (tasks/ingest\_github\_signals.py)**

* Read structured\_jobs.csv to identify target technologies.  
* Query the BigQuery Public Dataset githubarchive.day.20260320.  
* Filter for WatchEvent (Stars) on repos related to our tech stack.  
* Save as Parquet and upload to GCS: gs://{bucket}/raw/github\_signals/date=20260320/data.parquet.

### **STEP 4: SQL Transformation (tasks/fct\_growth\_signals.sql)**

* **Type:** bq.sql.  
* **Depends on:** ingest\_github\_signals.  
* **Logic:** Aggregate stars by company\_domain and date. Assign an intent\_priority (High/Med/Low) based on volume.  
* **Optimization (4-point Zoomcamp requirement):** \- partition\_by: signal\_date (Daily).  
  * cluster\_by: \["company\_domain", "signal\_type"\].

### **STEP 5: Documentation (README.md)**

Update README.md to look professional and include:

* **Project Goal:** Solving the "Integration Wall" for GTM teams.  
* **Zero-Cost Strategy:** Detailed notes on Free Tier regions on GCP platform and 60-day BQ Sandbox expirations.  
* **How to Run:** terraform apply \-\> bruin run.
MORE EXPLANATIONS THE BETTER - this is public github repo and will be presented to others.
We do not know the level of audience, so we need to be clear, detailed and concise but not too verbose. Prepare for both technical and non-technical audience.

## **🛑 AGENT RULES**

* **Idempotency:** All SQL must be able to run multiple times without duplication.  
* **Error Handling:** Python scripts must include basic try-except blocks for API/GCS failures.  
* **No Hardcoding:** If you need a value, put it in bruin.yaml or .env.

## **🤖 YOUR AGENTIC TOOLBOX (MCP)**

You have access to a suite of MCP servers. Use them as follows:

* **Reference Logic:** Use repo-docs to index https://github.com/denis911/antigravity-bruin-mcp-bigquery. Follow the patterns established in my previous work for Bruin.  
* **Environment Management:** Use mcp.antigravity.com/mcp/gcp to verify datasets/buckets exist and debug BigQuery errors in real-time.  
* **Pipeline Syntax:** Use mcp.bruin.dev/mcp to validate Bruin task headers and DAG structures.  
* **Exploratory Data Analysis:** Use mcp.duckdb.org/mcp to profile the structured\_jobs.csv locally before pushing to the cloud.  
* **Viz Layer:** Use mcp.superset.apache.org/mcp to ensure the final BigQuery views are optimized for dashboarding.

## **🏗️ ARCHITECTURE & RULES**

1. **Infra (Terraform):** us-central1 only. Prefix all resources with ${GCP\_PROJECT\_ID}.  
2. **Ingestion (Python):** Fetch WatchEvent from githubarchive.day.20260320. Save to GCS as Parquet.  
3. **DWH (BigQuery):** fct\_growth\_signals must be **Partitioned by Date** and **Clustered by company\_domain**.  
4. **Cost Control:** Implement 30-day lifecycle rules on GCS.

## **🛠️ TASK LIST**

1. **\[Phase 1\]** Generate terraform/main.tf and variables.tf. Use the GCP MCP to confirm the project is active.  
2. **\[Phase 2\]** Setup bruin.yaml. Use the Bruin MCP to ensure the connection string is valid.  
3. **\[Phase 3\]** Write tasks/ingest\_github\_signals.py. Use the GitHub Archive public dataset.  
4. **\[Phase 4\]** Write tasks/fct\_growth\_signals.sql. Reference my repo-docs for the preferred SQL formatting.  
5. **\[Phase 5\]** Update README.md with "Zero-Cost Strategy" (60-day BQ Sandbox limits and 5GB GCS caps).

## **🛑 REPRODUCIBILITY REQUIREMENT**

Even if you use MCP tools to "do" things, you **MUST** write the code into .tf, .py, and .sql files. The repository must be able to run from scratch without the MCP servers.

USE INSTRUCTIONS IN AGENTS.md FILE AS A SAFETY NET - DO NOT IGNORE IT. IT IS CRITICAL FOR PROJECT SUCCESS.

**Agent: Please acknowledge these instructions and start with "Phase 1: Terraform Infrastructure". Generate the code for variables.tf and main.tf now.**

---

