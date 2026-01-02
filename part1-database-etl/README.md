
# Part 1 – Database ETL

## How to Run the ETL Pipeline

1. Navigate to the `part1-database-etl` folder.
2. Install the required Python packages:

pip install -r requirements.txt

3. Run the ETL script:
python etl_pipeline.py

## Database Connection Settings

The ETL pipeline connects to a MySQL database using SQLAlchemy.

Update the database connection string in `etl_pipeline.py`:

```python
engine = create_engine(
    "mysql+pymysql://USERNAME:PASSWORD@localhost:3306/fleximart"
)

After successful execution, the ETL pipeline generates the following files:

- `customers_cleaned.csv` – cleaned customer data
- `products_cleaned.csv` – cleaned product data
- `sales_cleaned.csv` – cleaned sales data
- `data_quality_report.txt` – summary of data quality metrics

output for the data quality report generated

DATA QUALITY REPORT
==================================================

CUSTOMERS FILE
Number of records processed          : 26
Number of duplicates removed         : 1
Number of missing values handled     : 5
Number of records loaded successfully: 25

PRODUCTS FILE
Number of records processed          : 20
Number of duplicates removed         : 0
Number of missing values handled     : 3
Number of records loaded successfully: 20

SALES FILE
Number of records processed          : 41
Number of duplicates removed         : 1
Number of missing values handled     : 5
Number of records loaded successfully: 35