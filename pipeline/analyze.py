import os
import pandas as pd
from sqlalchemy import create_engine

# Database Connection
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cms_data")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_top_procedures():
    """Query 1: Top 10 Most Expensive Procedures in Texas by Avg Medicare Payment"""
    query = """
    SELECT procedure_desc,
           ROUND(AVG(avg_medicare_pmt), 2) AS avg_pmt,
           SUM(total_services)              AS total_utilization
    FROM cms_procedures
    WHERE provider_state = 'TX'
    GROUP BY procedure_desc
    ORDER BY avg_pmt DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_city_variance():
    """Query 2: Cost Variance by City (Houston vs Dallas vs Austin vs San Antonio)"""
    query = """
    SELECT provider_city,
           ROUND(AVG(avg_medicare_pmt), 2)  AS avg_payment,
           ROUND(AVG(avg_submitted_chrg), 2) AS avg_billed,
           SUM(total_services)               AS total_services
    FROM cms_procedures
    WHERE provider_city IN ('HOUSTON', 'DALLAS', 'AUSTIN', 'SAN ANTONIO')
    GROUP BY provider_city
    ORDER BY avg_payment DESC;
    """
    return pd.read_sql(query, engine)

def get_charge_ratio():
    """Query 3: Charge-to-Payment Ratio (identifies billing efficiency gaps)"""
    query = """
    SELECT procedure_desc,
           ROUND(AVG(avg_submitted_chrg / NULLIF(avg_medicare_pmt, 0)), 2) AS charge_ratio,
           SUM(total_services) AS volume
    FROM cms_procedures
    WHERE provider_state = 'TX'
    GROUP BY procedure_desc
    HAVING SUM(total_services) > 1000
    ORDER BY charge_ratio DESC
    LIMIT 15;
    """
    return pd.read_sql(query, engine)

if __name__ == "__main__":
    print("Executing Analytical Queries...\n")
    
    print("--- Top 10 Most Expensive Procedures in TX ---")
    print(get_top_procedures().to_string(index=False))
    
    print("\n--- Cost Variance by City ---")
    print(get_city_variance().to_string(index=False))
    
    print("\n--- Top 15 Highest Charge-to-Payment Ratios (Volume > 1000) ---")
    print(get_charge_ratio().to_string(index=False))