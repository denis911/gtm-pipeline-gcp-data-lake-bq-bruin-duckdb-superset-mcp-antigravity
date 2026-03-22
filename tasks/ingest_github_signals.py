"""
Ingest GitHub signals from the public GitHub Archive dataset in BigQuery.
This task identifies 'WatchEvent' (stars) for repositories related to the tech stack 
defined in structured_jobs.csv and saves the results to GCS as Parquet.

@type: python
@name: ingest_github_signals
@image: python:3.12
"""

import os
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import logging
import ast

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_tech_keywords(csv_path: str) -> list[str]:
    """
    Extract unique tech keywords from the structured_jobs.csv file.
    """
    df = pd.read_csv(csv_path)
    all_tech = []
    
    if 'tech_stack' in df.columns:
        for stack in df['tech_stack'].dropna():
            try:
                # Assuming the stack is a string representation of a list
                keywords = ast.literal_eval(stack)
                if isinstance(keywords, list):
                    all_tech.extend(keywords)
                else:
                    all_tech.append(str(keywords))
            except (ValueError, SyntaxError):
                all_tech.append(str(stack))
                
    unique_tech = sorted(list(set([t.strip().lower() for t in all_tech if t])))
    logger.info(f"Extracted {len(unique_tech)} unique tech keywords.")
    return unique_tech

def ingest_github_data(project_id: str, bucket_name: str, target_date: str):
    """
    Query GitHub Archive and save to GCS.
    """
    client = bigquery.Client(project=project_id)
    
    # Format date for BQ table: githubarchive.day.YYYYMMDD
    bq_date = target_date.replace("-", "")
    table_id = f"githubarchive.day.{bq_date}"
    
    import re
    keywords = get_tech_keywords("structured_jobs.csv")
    # Escape special characters for RE2 regex (used by BigQuery)
    # We use \\ to escape since it's inside a string in SQL.
    escaped_keywords = [re.escape(k) for k in keywords]
    regex_pattern = "|".join([rf"\b{k}\b" for k in escaped_keywords])
    
    query = f"""
    SELECT 
        repo.name as repo_name,
        repo.url as repo_url,
        actor.login as actor_login,
        created_at,
        type as event_type
    FROM `{table_id}`
    WHERE type = 'WatchEvent'
    AND REGEXP_CONTAINS(LOWER(repo.name), r'{regex_pattern}')
    LIMIT 10000
    """
    
    logger.info(f"Running query on {table_id}...")
    query_job = client.query(query)
    results = query_job.to_dataframe()
    
    if results.empty:
        logger.warning(f"No results found for {target_date} with current keywords.")
        return

    logger.info(f"Fetched {len(results)} rows. Saving to GCS...")
    
    # Add ingestion metadata
    results['ingestion_date'] = pd.to_datetime('today').date()
    results['signal_date'] = pd.to_datetime(target_date).date()
    
    # Save locally first then upload (or use gcsfs if preferred)
    local_path = "temp_signals.parquet"
    results.to_parquet(local_path, index=False)
    
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    gcs_path = f"raw/github_signals/date={target_date}/data.parquet"
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    
    os.remove(local_path)
    logger.info(f"Successfully uploaded to gs://{bucket_name}/{gcs_path}")

if __name__ == "__main__":
    # These would typically come from environment variables or Bruin parameters
    project_id = os.getenv("GCP_PROJECT_ID", "evident-axle-339820")
    bucket_name = os.getenv("DATA_LAKE_BUCKET", f"{project_id}-data-lake")
    target_date = "2026-03-19" # Target date as requested
    
    ingest_github_data(project_id, bucket_name, target_date)
