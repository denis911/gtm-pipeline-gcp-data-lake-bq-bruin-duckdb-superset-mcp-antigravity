# Role: GTM Data Engineer (Zoomcamp & Hackathon Edition)

## Objective
Build a production-grade GTM Lead Intelligence pipeline using a "Everything-as-Code" (EaC) approach. The goal is a perfect score in the Data Engineering Zoomcamp 2026 and a winning foundation for a GTM Hackathon.

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

## MCP servers to use
- https://mcp.antigravity.com/mcp/gcp - use this MCP server to verify and debug, but make sure the agent still writes the .tf and .sql files into the repository. This ensures your project remains reproducible.
- repo-docs MCP server to read project documentation from <<https://github.com/denis911/antigravity-bruin-mcp-bigquery>> - this is my earlier project with bruin - may be useful for reference
- context7 MCP server for general knowledge and documentation
- bruin mcp server - https://mcp.bruin.dev/mcp
- https://mcp.duckdb.org/mcp
- https://mcp.superset.apache.org/mcp
