import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cms_data")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def create_schema():
    schema_sql = """
    DROP TABLE IF EXISTS cms_procedures;
    
    CREATE TABLE cms_procedures (
        id                  SERIAL PRIMARY KEY,
        provider_city       VARCHAR(100),
        provider_state      VARCHAR(2),
        procedure_code      VARCHAR(20),
        procedure_desc      TEXT,              -- Changed from VARCHAR(255) to handle absurdly long CMS descriptions
        total_services      INTEGER,
        avg_medicare_pmt    NUMERIC(10, 2),
        avg_submitted_chrg  NUMERIC(10, 2),
        avg_allowed_amt     NUMERIC(10, 2),
        data_year           SMALLINT,
        loaded_at           TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_cms_state_proc ON cms_procedures(provider_state, procedure_code);
    CREATE INDEX idx_cms_city ON cms_procedures(provider_city);
    """
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
    print("Schema created successfully.")

def extract_and_load():
    print("Downloading CMS data...")
    
    # Updated CMS API Endpoint for the latest dataset
    api_url = "https://data.cms.gov/data-api/v1/dataset/92396110-2aed-4d63-a6a2-5d6207d46a29/data"
    
    params = {
        "filter[Rndrng_Prvdr_State_Abrvtn]": "TX",
        "size": "5000" 
    }
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    
    print("Processing data with pandas...")
    df = pd.DataFrame(response.json())
    
    # Force all incoming column names to lowercase to prevent KeyErrors
    df.columns = df.columns.str.lower()
    
    df_clean = pd.DataFrame({
        'provider_city': df['rndrng_prvdr_city'].str.upper(),
        'provider_state': df['rndrng_prvdr_state_abrvtn'],
        'procedure_code': df['hcpcs_cd'],
        'procedure_desc': df['hcpcs_desc'],
        'total_services': pd.to_numeric(df['tot_srvcs'], errors='coerce'),
        'avg_medicare_pmt': pd.to_numeric(df['avg_mdcr_pymt_amt'], errors='coerce'),
        'avg_submitted_chrg': pd.to_numeric(df['avg_sbmtd_chrg'], errors='coerce'),
        'avg_allowed_amt': pd.to_numeric(df['avg_mdcr_alowd_amt'], errors='coerce'),
        'data_year': 2023
    })
    
    df_clean = df_clean.dropna(subset=['procedure_code', 'avg_medicare_pmt', 'total_services'])
    
    print(f"Loading {len(df_clean)} records into PostgreSQL...")
    df_clean.to_sql('cms_procedures', engine, if_exists='append', index=False)
    print("Data ingestion complete!")

if __name__ == "__main__":
    create_schema()
    extract_and_load()