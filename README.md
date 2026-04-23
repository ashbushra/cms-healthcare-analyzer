# CMS Healthcare Cost Analyzer

An end-to-end Python ETL pipeline that ingests publicly available CMS Medicare procedure cost data, loads it into a PostgreSQL database, and executes analytical SQL queries to surface regional cost variances and utilization trends across Texas cities. 

## 1. Executive Summary & Problem Statement
**The Problem:** Medicare billing and payment amounts vary significantly by geography, facility, and procedure. For healthcare administrators, consultants, and analysts, identifying these variances is critical for competitive pricing, revenue cycle management, and operational efficiency. 

**The Solution:** This pipeline automates the ingestion of public CMS data, normalizes it, and outputs a business-ready HTML report identifying the most expensive procedures, highest billing discrepancies, and geographical cost variances across major Texas hubs.

## 2. Key Findings (2023 CMS Data)
Based on the execution of the analytical queries against the Texas provider dataset:
* **Cost Variance by City:** Dallas exhibits the highest average Medicare payment at **$113.50**, noticeably outpacing Houston (**$83.12**) and San Antonio (**$77.48**).
* **Top Expenditure:** The single most expensive procedure by average payment is the *Insertion of spinal neurostimulator generator* at **$17,536.55**.
* **Billing Discrepancies:** Low osmolar contrast material (used in imaging) shows the highest charge-to-payment ratio, with providers billing Medicare up to **215x** the actual allowable payment amount.

## 3. Architecture & Tech Stack
* **Language:** Python 3.11
* **Data Ingestion:** `requests` API extraction & `pandas` data normalization
* **Database:** PostgreSQL 15 (Containerized via Docker)
* **Analysis:** Analytical SQL via `SQLAlchemy`
* **Reporting:** Automated HTML report generation via `Jinja2`
* **Cloud Deployment:** AWS S3 Static Website Hosting via `boto3` (SAA-C03 Architecture)
* **CI/CD:** GitHub Actions (`ruff` linting + `pytest`)

## 4. Setup & Execution
**Prerequisites:** Docker, Docker Compose, and Python 3.11.

