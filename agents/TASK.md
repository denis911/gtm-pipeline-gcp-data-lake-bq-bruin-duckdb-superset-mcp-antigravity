# Project Implementation Checklist

## [ ] Phase 1: Infrastructure as Code
- [ ] Create `terraform/variables.tf` with `project_id` and `region`.
- [ ] Create `terraform/main.tf` with GCS bucket (standard, us-central1) and BQ dataset.
- [ ] Add Lifecycle Rule (30 days) to GCS bucket for cost-control.
- [ ] **Action:** Instruct user to run `terraform apply`, check the GCP console to verify that the resources are created and provide the output. When done, update README.md and  proceed to Phase 2.

## [ ] Phase 2: Pipeline Foundation
- [ ] Create `.env` file with `GCP_PROJECT_ID`.
- [ ] Create `bruin.yaml` defining the `bq_gtm` connection and `data_lake_bucket` variable.
- [ ] Run `bruin setup-check` to verify BQ permissions.

## [ ] Phase 3: Python Ingestion (GitHub Signals)
- [ ] Create `tasks/ingest_github_signals.py`.
- [ ] Implement BigQuery client to fetch `WatchEvent` from `githubarchive.day.20260321`.
- [ ] Upload results as Parquet to GCS using dynamic bucket naming: `f"{project_id}-data-lake"`.

## [ ] Phase 4: BigQuery Transformations
- [ ] Create `tasks/fct_growth_signals.sql`.
- [ ] Add Bruin headers for `@type: bq.sql` and `@depends: [ "ingest_github_signals" ]`.
- [ ] **Critical:** Add `@conf` for `partition_by` (date) and `cluster_by` (company_domain).
- [ ] Logic: Group signals by day/company and assign an `intent_priority` (High/Med/Low).

## [ ] Phase 5: Documentation & Final Polish
- [ ] Update `README.md` with the "Zero-Cost Infra" and "GTM Context" sections.
- [ ] Generate pipeline docs using `bruin doc`.
- [ ] Final end-to-end run: `bruin run`.

