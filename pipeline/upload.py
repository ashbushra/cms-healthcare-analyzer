import os
import boto3
from botocore.exceptions import ClientError

def upload_to_s3():
    print("Preparing S3 upload...")
    
    region = os.getenv("AWS_REGION", "us-east-1")
    bucket_name = os.getenv("S3_BUCKET")
    
    if not bucket_name or bucket_name == "your-portfolio-bucket-name":
        print(" Error: Please update your S3_BUCKET and AWS credentials in the .env file.")
        return

    # boto3 automatically picks up the credentials from your environment variables

    # boto3 automatically finds your credentials in ~/.aws/credentials
    s3 = boto3.client("s3", region_name=region)
   
    
    file_path = "outputs/report.html"
    
    if not os.path.exists(file_path):
        print(f" Error: {file_path} not found. Run the report script first.")
        return

    try:
        print(f"Uploading {file_path} to s3://{bucket_name}/index.html ...")
        
        # Uploads the file, sets the content type so browsers render it instead of downloading it, 
        # and applies the public-read ACL.
        s3.upload_file(
            file_path, 
            bucket_name, 
            "index.html",
            ExtraArgs={
                "ContentType": "text/html", 
                "ACL": "public-read"
            }
        )
        
        website_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
        
        print(" Upload successful!")
        print(f" Report is live at: {website_url}")
        
    except ClientError as e:
        print(f" AWS Error: {e}")
        print("Note: If you get an AccessDenied error, double check that 'Block all public access' is turned OFF on your bucket.")

if __name__ == "__main__":
    upload_to_s3()