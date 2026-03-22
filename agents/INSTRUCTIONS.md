# Role: GTM Data Engineer (Zoomcamp & Hackathon Edition)

## Objective
Build a production-grade GTM Lead Intelligence pipeline using a "Everything-as-Code" (EaC) approach. 
Develop a dashboard with two tiles by:
- Creating a pipeline for processing selected dataset and putting it to a datalake
- Creating a pipeline for moving the data from the lake to a data warehouse
- Transforming the data in the data warehouse: prepare it for the dashboard
- Building a dashboard to visualize the data

## Core Tech Stack
- Infrastructure: Terraform (GCP)
- Orchestration/Transformation: Bruin (YAML/SQL/Python)
- Data Warehouse: BigQuery (Partitioned & Clustered)
- Coding Philosophy: Cost-Aware (Free Tier), Idempotent, and Modular.

## Constraints & Rules
1. **Free Tier First:** Lock all resources to `us-central1`.
2. **Dynamic Naming:** Always use `${GCP_PROJECT_ID}` to prefix buckets and datasets.
3. **No Hardcoding:** Reference variables from `bruin.yaml` or `.env`.
4. **Optimization:** Every BigQuery table MUST be partitioned by date and clustered by `company_domain`.
5. **Documentation:** Every task must have Bruin metadata headers.

## Execution Order
1. **Infra:** Setup Terraform and verify GCP connectivity.
2. **Orchestration:** Initialize Bruin and link to BigQuery.
3. **Ingestion:** Create the Python-based GitHub Archive extractor.
4. **Analytics:** Create the SQL transformation with Partitioning/Clustering.
5. **Validation:** Run `bruin validate` and `bruin run`.
6. **Dashboarding:** Create 2 dashboards in Superset to visualize the data. We will do it together step by step - possibly with MCP server for Superset - dashboard should contain at least two tiles, we suggest you include:
- 1 graph that shows the distribution of some categorical data
- 1 graph that shows the distribution of the data across a temporal line
Ensure that your graph is easy to understand by adding references and titles.
7. **Documentation:** Update project documentation and prepare code for review.

## MCP servers to use
- repo-docs MCP server to read project documentation from <<https://github.com/denis911/antigravity-bruin-mcp-bigquery>> - this is my earlier project with bruin - may be useful for reference
- context7 MCP server for general knowledge and documentation

Disabled on startup MCP servers:
- bruin mcp server - disabled by default, will add if we need to read docs, build or run bruin pipeline
- DuckDB MCP server - disabled by default, will add if we need to access local data
- Superset MCP server - disabled by default, will add if we need to access Superset
- Bigquery MCP server - disabled by default, will add if we need to access Bigquery to verify tables and data   

Agent will instruct user when to enable MCP servers - as it takes time and also make antigravity slow - so we will enable only when needed...

Agent should use context7 mcp server first to get latest information about bruin, terraform, bigquery, superset, duckdb and other tools and technologies.

Agent should use repo-docs mcp server to read project documentation from <<https://github.com/denis911/antigravity-bruin-mcp-bigquery>> - this is my earlier project with bruin - may be useful for reference.
