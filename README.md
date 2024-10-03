# Customers Behavior Analysis

This project aims to analyze customer behavior, helping businesses understand customer preferences, patterns, and trends. The insights derived from this analysis can assist in improving customer engagement strategies, enhancing user experiences, and driving business growth.

## Background

Customer behavior analysis is crucial for businesses looking to optimize their marketing strategies and improve customer satisfaction. This project focuses on understanding customer interactions, purchase patterns, and preferences through data analysis, providing actionable insights for data-driven decision-making. It caters to:

- **Marketing Teams**: To target customers more effectively based on their behavior and preferences.
- **Business Analysts**: To understand market segmentation and customer lifetime value.
- **Product Teams**: To identify customer needs and improve product offerings.

## Data Scource

- [Dataset Source]( https://www.kaggle.com/datasets/lovishbansal123/sales-of-a-supermarket) 

## Tools 
[<img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white" alt="Apache Airflow" />](https://airflow.apache.org/)
[<img src="https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch" />](https://www.elastic.co/elasticsearch/)
[<img src="https://img.shields.io/badge/Kibana-005571?style=for-the-badge&logo=kibana&logoColor=white" alt="Kibana" />](https://www.elastic.co/kibana/)
[<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />](https://www.docker.com/)
[<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />](https://www.postgresql.org/)

## Workflow

Problem Identification → Data Understanding → Data Cleaning → Data Exploration → Feature Engineering → Modeling → Insights & Recommendations

## Output

Output and Insight are in the Image Folder


## Files Overview

1. **`DAG.py`**: Script containing the ETL (Extract, Transform, Load) pipeline used to extract customer data, transform it for analysis, and load it into a structured format for further use. This includes data preprocessing and transformation steps.

2. **`GX.ipynb`**: A Jupyter Notebook that performs exploratory data analysis (EDA) on customer data. It includes data visualization and customer behavior insights, providing detailed analysis of customer preferences and trends.

3. **`data_raw.csv`**: The raw dataset containing unprocessed customer behavior data, serving as the initial input for analysis.

4. **`data_clean.csv`**: A cleaned and preprocessed version of the dataset, produced after removing inconsistencies, handling missing values, and normalizing the data for analysis.

5. **`ddl.txt`**: SQL file containing the Data Definition Language (DDL) statements that define the schema and structure of the database used for storing customer behavior data.


