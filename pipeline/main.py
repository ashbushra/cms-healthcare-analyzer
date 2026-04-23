import ingest
import analyze
import report
import upload

def run_pipeline(skip_upload=False):
    print("Starting CMS Healthcare Cost Analyzer Pipeline...\n")
    
    print("--- PHASE 2: INGEST ---")
    ingest.create_schema()
    ingest.extract_and_load()
    
    print("\n--- PHASE 3: ANALYZE ---")
    # Executing queries to ensure data loaded correctly
    analyze.get_top_procedures()
    analyze.get_city_variance()
    analyze.get_charge_ratio()
    print("SQL queries executed successfully.")
    
    print("\n--- PHASE 4: REPORT ---")
    report.generate_report()
    
    if not skip_upload:
        print("\n--- PHASE 5: UPLOAD ---")
        upload.upload_to_s3()
    else:
        print("\n--- SKIP: AWS Upload bypassed ---")
        
    print("\n Pipeline execution complete!")

if __name__ == "__main__":
    # Change to skip_upload=False when you are ready to push to S3
    run_pipeline(skip_upload=True)