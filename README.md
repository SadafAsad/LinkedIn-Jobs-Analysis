# Data Engineering Job Market Analysis
The Banks MC ETL Pipeline is a Python project with the primary objective of automating the extraction, transformation, and loading (ETL) process for banks' market capital data. Leveraging web scraping capabilities through Requests and BeautifulSoup. Subsequently, Pandas, numpy, SQLite, and Apache Airflow are utilized to create the project. Docker is used to containerize Airflow, ensuring a simplified deployment.

<p align="center">
  <img src="tasks_graph.png" />
</p>

## ETL Pipeline
- Extract: It is initiated by leveraging web scraping capabilities through Requests and BeautifulSoup to extract market capital data from an archived Wikipedia page. This phase involves retrieving specific information related to banks' market capital from the source.
- Transform: Following data extraction, the pipeline utilizes Pandas and numpy to transform the raw data according to a predefined CSV file. This transformation involves calculating market capital in other currencies based on predefined conversion rates.
- Load: Once the data has been successfully transformed, the final step involves loading it into both a CSV file and an SQLite database. This is facilitated by incorporating SQLite for database management.
- Apache Airflow orchestrates these tasks, ensuring a systematic and automated execution of the entire ETL process. 

## Tools & Libraries
- Python
- Scrapy
- ScrapeOps
- AWS EC2
- AWS S3
- AWS Glue
- AWS Athena
- AWS QuickSight
