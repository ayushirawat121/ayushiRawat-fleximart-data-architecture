# FlexiMart Data Architecture Project

**Student Name:** Ayushi Rawat
**Student ID:** bitsom_ba_25071683
**Email:** ayushirawat121@gmail.com
**Date:** 04/01/2026

## Project Overview
This project demonstrates the end-to-end design and implementation of a modern data architecture for FlexiMart, an e-commerce platform. It includes transactional data processing using ETL, NoSQL modeling for flexible product catalogs, and a data warehouse built using a star schema to support analytical reporting and business insights.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0
- SQL


## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

a. Understood how to design and implement ETL pipelines for structured data
b. Learned the strengths and limitations of relational vs NoSQL databases
c. Gained hands-on experience with star schema modeling for analytics
d. Improved SQL skills for aggregation, window functions, and segmentation analysis

## Challenges Faced

1. Handling data formats
2. Understanding star schema design