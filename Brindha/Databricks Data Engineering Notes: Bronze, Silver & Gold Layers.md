# Databricks Data Engineering Notes: Bronze, Silver & Gold Layers

PySpark • Databricks • Delta Tables • Medallion Architecture

These notes explain your code line by line, using simple examples so you understand what each layer does, why it is needed, and how the data flows from raw files to business reports.

## 1. Understand the overall architecture

In data engineering, we often use a pattern called the Medallion Architecture. Data passes through three layers, becoming cleaner and more useful at each stage.

## 1. BRONZE LAYER

Raw data ingestion

Read CSV files and store the source data

## 2. SILVER LAYER

Cleaned and validated data

Remove duplicate rows and invalid records

## 3. GOLD LAYER

Business-ready aggregated data

Calculate sales and quantities by product

### Simple example

Imagine an e-commerce company receives thousands of order records every day.

- Bronze: Store the incoming order records.
- Silver: Remove duplicate records and orders without a quantity.
- Gold: Calculate total sales and quantities for each product.

The final result helps business teams answer questions such as, “Which product generated the highest sales?”

## 2. Understand the table names

Your code uses these tables:

| Layer          | Table name                                     | Purpose                           |
| -------------- | ---------------------------------------------- | --------------------------------- |
| Bronze         | `ecommerce_catalog.bronze.sales_raw`           | Stores ingested sales data        |
| Silver         | `ecommerce_catalog.silver.sales_clean`         | Stores cleaned sales data         |
| Gold, intended | `ecommerce_catalog.gold.sales_reportable_data` | Stores aggregated sales summaries |

Your current Gold code writes to `ecommerce_catalog.silver.reporatble_data`. That table is actually in the Silver schema, despite containing Gold-style aggregated data. We will correct this in the final version below.

The table names follow the three-part naming convention commonly used in Databricks Unity Catalog:

`catalog_name.schema_name.table_name`

For example:

- `ecommerce_catalog` is the catalog.
- `bronze` is the schema.
- `sales_raw` is the table.

# 3. Bronze Layer: Ingest Raw Data

## Objective

Read raw CSV files from a Databricks Volume, convert the sales amount into a numeric type, and save the resulting DataFrame as a table.

### Your Bronze code, explained

```
from pyspark.sql.functions import coldf = spark.read.format("csv") \    .option("header", "true") \    .option("inferSchema", "true") \    .load("/Volumes/ecommerce_catalog/bronze/raw_order_files/*.csv")df = df.withColumn(    "sales_amount",    col("sales_amount").cast("double"))df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.bronze.sales_raw")display(df)
```

### Step 1: Import `col`

```
from pyspark.sql.functions import col
```

`col()` lets you reference a column in a PySpark DataFrame.

For example:

```
col("sales_amount")
```

means you want to work with the `sales_amount` column.

### Step 2: Read the CSV files

```
df = spark.read.format("csv") \    .option("header", "true") \    .option("inferSchema", "true") \    .load("/Volumes/ecommerce_catalog/bronze/raw_order_files/*.csv")
```

Let's break this down.

| Code                             | Meaning                                     |
| -------------------------------- | ------------------------------------------- |
| `spark.read`                     | Starts reading data with Spark              |
| `.format("csv")`                 | Specifies that the source files are CSV     |
| `.option("header", "true")`      | Treats the first row as column names        |
| `.option("inferSchema", "true")` | Asks Spark to infer column data types       |
| `.load(...)`                     | Reads the files from the specified location |
| `*.csv`                          | Matches CSV files in that directory         |

The path is a Databricks Volume path. It assumes that the catalog, schema, volume, and permissions are correctly configured.

Example input CSV:

| order_id | product_name | quantity | sales_amount |
| -------- | ------------ | -------- | ------------ |
| 101      | Laptop       | 2        | 1200.50      |
| 102      | Mouse        | 5        | 125.00       |
| 103      | Keyboard     | 3        | 210.75       |

Spark reads the matching files and creates a DataFrame called `df`.

### Step 3: Convert `sales_amount` to a numeric type

```
df = df.withColumn(    "sales_amount",    col("sales_amount").cast("double"))
```

Why? Sales amounts need to be numeric so that Spark can calculate totals and averages.

For example:

- `"1200.50"` is text.
- `1200.50` is a numeric value.

`withColumn()` creates or replaces a column. Here, it replaces `sales_amount` with its value cast to the `double` data type.

Note that if a value cannot be converted to a number, Spark may return `NULL`. This code does not explicitly flag those invalid values.

### Step 4: Save the Bronze table

```
df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.bronze.sales_raw")
```

| Code                 | Meaning                          |
| -------------------- | -------------------------------- |
| `df.write`           | Starts writing the DataFrame     |
| `.mode("overwrite")` | Replaces the existing table data |
| `.saveAsTable(...)`  | Saves the data as a named table  |

Important: `overwrite` replaces the existing table's data on each run. This is appropriate for a simple full refresh, but you would typically use a different strategy for incremental ingestion in a production pipeline.

### Step 5: Display the data

```
display(df)
```

This displays the DataFrame in a Databricks notebook so you can inspect the ingested records.

### Bronze layer summary

- Input: Raw CSV files.
- Processing: Read files, infer schema, cast sales amount.
- Output: `ecommerce_catalog.bronze.sales_raw`.
- Purpose: Make incoming data available for downstream processing.

# 4. Silver Layer: Clean the Data

## Objective

Read the Bronze table, remove duplicate rows, remove records where `quantity` is missing, and save the cleaned data to the Silver table.

### Your Silver code, explained

```
from pyspark.sql.functions import colbronze_df = spark.table("ecommerce_catalog.bronze.sales_raw")silver_df = bronze_df.dropDuplicates()silver_df = silver_df.filter(    col("quantity").isNotNull())silver_df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.silver.sales_clean")display(silver_df)
```

### Step 1: Read data from Bronze

```
bronze_df = spark.table("ecommerce_catalog.bronze.sales_raw")
```

This reads the table created by your Bronze notebook.

You are no longer reading the CSV files directly. Instead, you are reading the data stored in the Bronze table.

Think of it this way:

CSV files → Bronze table → Silver processing

### Step 2: Remove duplicate rows

```
silver_df = bronze_df.dropDuplicates()
```

`dropDuplicates()` removes rows that have identical values across all columns.

Example:

Before removing duplicates:

| order_id | product_name | quantity | sales_amount |
| -------- | ------------ | -------- | ------------ |
| 101      | Laptop       | 2        | 1200.50      |
| 101      | Laptop       | 2        | 1200.50      |
| 102      | Mouse        | 5        | 125.00       |

After removing duplicates:

| order_id | product_name | quantity | sales_amount |
| -------- | ------------ | -------- | ------------ |
| 101      | Laptop       | 2        | 1200.50      |
| 102      | Mouse        | 5        | 125.00       |

The duplicate Laptop row is removed.

Important: This removes only rows identical across all columns. If you want one row per `order_id`, you would instead use `dropDuplicates(["order_id"])`, provided that `order_id` uniquely identifies a record in your data.

### Step 3: Remove records with missing quantities

```
silver_df = silver_df.filter(    col("quantity").isNotNull())
```

This keeps only records where `quantity` is not `NULL`.

Example:

Before filtering:

| order_id | product_name | quantity |
| -------- | ------------ | -------- |
| 101      | Laptop       | 2        |
| 102      | Mouse        | NULL     |
| 103      | Keyboard     | 3        |

After filtering:

| order_id | product_name | quantity |
| -------- | ------------ | -------- |
| 101      | Laptop       | 2        |
| 103      | Keyboard     | 3        |

The Mouse record is removed because its quantity is missing.

Remember: `isNotNull()` does not remove zero quantities or empty strings. It only filters out SQL `NULL` values.

### Step 4: Save the Silver table

```
silver_df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.silver.sales_clean")
```

This saves the cleaned records to the Silver schema.

The overwrite mode replaces the existing table data whenever the notebook runs.

### Step 5: Display the cleaned data

```
display(silver_df)
```

Use this to verify the result and confirm that duplicate rows and rows with missing quantities have been removed.

### Silver layer summary

- Input: `ecommerce_catalog.bronze.sales_raw`
- Processing: Remove duplicate rows and records with null quantities.
- Output: `ecommerce_catalog.silver.sales_clean`
- Purpose: Provide cleaner, more reliable data for analysis.

# 5. Gold Layer: Create Business Reports

## Objective

Read the cleaned Silver data and calculate sales metrics for each product.

Your Gold logic groups records by `product_name` and calculates:

1. Total sales amount.
2. Total quantity sold.
3. Number of rows counted as orders.

### Your Gold code, explained

```
from pyspark.sql.functions import sum, count, meansilver_df = spark.table("ecommerce_catalog.silver.sales_clean")gold_df = silver_df.groupBy("product_name").agg(    sum("sales_amount").alias("total_sales"),    sum("quantity").alias("total_quantity"),    count("*").alias("total_orders"))gold_df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.silver.reporatble_data")display(gold_df)
```

### Step 1: Read the Silver table

```
silver_df = spark.table("ecommerce_catalog.silver.sales_clean")
```

This loads the cleaned records prepared by the Silver layer.

### Step 2: Group records by product

```
gold_df = silver_df.groupBy("product_name").agg(
```

`groupBy("product_name")` groups all rows with the same product name together.

For example, if Laptop appears 100 times, Spark groups those Laptop records and calculates the requested metrics for that group.

### Step 3: Calculate total sales

```
sum("sales_amount").alias("total_sales")
```

`sum()` adds the sales amounts for each product.

Example:

| product_name | sales_amount |
| ------------ | ------------ |
| Laptop       | 1200.50      |
| Laptop       | 800.00       |
| Laptop       | 500.00       |

Total Laptop sales = ₹2,500.50, assuming these amounts are denominated in Indian rupees.

The `.alias("total_sales")` gives the resulting column a readable name.

### Step 4: Calculate total quantity

```
sum("quantity").alias("total_quantity")
```

This adds the quantity values for each product.

For example, if Laptop quantities are 2, 1 and 3:

Total quantity = 2 + 1 + 3 = 6 laptops.

### Step 5: Count the rows

```
count("*").alias("total_orders")
```

This counts the number of rows in each product group.

For example, if there are three Laptop rows, the result is `3`.

Important: This is a row count, not necessarily a distinct order count. If one order contains multiple rows, or an order is split into multiple product lines, the count will not equal the number of unique orders. Use `countDistinct("order_id")` if you need a distinct order count and `order_id` is the correct identifier for that purpose.

### Step 6: Save the aggregated table

```
gold_df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.silver.reporatble_data")
```

Your code currently saves the aggregated data into the Silver schema. For a clearer Bronze/Silver/Gold architecture, save it to a table in the Gold schema instead:

`ecommerce_catalog.gold.sales_reportable_data`

The Gold schema must already exist, or you must create it before saving.

### Step 7: Display the report

```
display(gold_df)
```

This displays the product-level sales summary.

### Example Gold output

Using the sample records from earlier, the output might look like this:

| product_name | total_sales | total_quantity | total_orders |
| ------------ | ----------- | -------------- | ------------ |
| Laptop       | 1200.50     | 2              | 1            |
| Mouse        | 125.00      | 5              | 1            |
| Keyboard     | 210.75      | 3              | 1            |

These numbers are illustrative. Your actual results depend on the contents of your CSV files.

### Gold layer summary

- Input: `ecommerce_catalog.silver.sales_clean`
- Processing: Group by product and aggregate sales metrics.
- Output: `ecommerce_catalog.gold.sales_reportable_data` (recommended).
- Purpose: Provide business-ready data for dashboards, reporting and analytics.

# 6. Corrected Gold Layer Code

Here is the cleaned-up version of your Gold code. I removed the unused `mean` import and corrected the destination table name.

```
from pyspark.sql.functions import sum, count# Read cleaned data from the Silver layersilver_df = spark.table(    "ecommerce_catalog.silver.sales_clean")# Aggregate sales data by productgold_df = silver_df.groupBy("product_name").agg(    sum("sales_amount").alias("total_sales"),    sum("quantity").alias("total_quantity"),    count("*").alias("total_orders"))# Save the report to the Gold layergold_df.write.mode("overwrite").saveAsTable(    "ecommerce_catalog.gold.sales_reportable_data")# Display the final reportdisplay(gold_df)
```

Note: The `gold` schema must exist in `ecommerce_catalog` before running this code. Also, the imported `mean` function in your original code was not being used.

# 7. Complete Data Pipeline at a Glance

Raw CSV files

Source: Databricks Volume

Incoming sales and order records.

Bronze: `sales_raw`

Read CSVs, infer column types, cast `sales_amount`, save raw ingested data.

Silver: `sales_clean`

Remove exact duplicate rows and records where quantity is null.

Gold: `sales_reportable_data`

Group by product and calculate total sales, total quantity and row count.

Business consumption

Power BI dashboards, reports, analytics and business decisions.

## 8. Important PySpark Functions to Remember

| Function           | What it does                                                |
| ------------------ | ----------------------------------------------------------- |
| `spark.read`       | Reads source data                                           |
| `spark.table()`    | Reads an existing table                                     |
| `col()`            | References a column                                         |
| `withColumn()`     | Creates or replaces a column                                |
| `cast()`           | Converts a column's data type                               |
| `dropDuplicates()` | Removes duplicate rows                                      |
| `filter()`         | Keeps rows matching a condition                             |
| `isNotNull()`      | Checks that a value is not null                             |
| `groupBy()`        | Groups rows by one or more columns                          |
| `agg()`            | Calculates aggregate values for each group                  |
| `sum()`            | Adds numeric values                                         |
| `count()`          | Counts rows or non-null values, depending on the expression |
| `saveAsTable()`    | Saves a DataFrame as a named table                          |
| `display()`        | Displays data in a Databricks notebook                      |

## 9. Quick Revision Quiz

1\. Which layer stores the initially ingested data?

Bronze

Silver

Gold

2\. What does dropDuplicates() do in your Silver code?

Removes null values

Removes rows identical across all columns

Groups products

3\. Which function groups sales by product?

filter()

withColumn()

groupBy()

4\. What does count('\*') measure in your Gold code?

Distinct customers

Distinct order IDs

Number of rows per product

5\. Where should aggregated reporting data normally be stored in this design?

Bronze schema

Silver schema

Gold schema

Try again

The main concept to remember: Bronze ingests the data, Silver cleans the data, and Gold transforms it into meaningful business metrics. Once you understand that flow, the PySpark code becomes much easier to follow.
