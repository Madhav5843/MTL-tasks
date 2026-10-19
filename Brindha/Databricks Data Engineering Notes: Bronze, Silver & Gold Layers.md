# Databricks Medallion Architecture: Complete Notes

These notes cover the Bronze, Silver, and Gold layers using PySpark in Databricks. Each section includes the complete code, explanations, input/output tables, and execution order.

## Architecture overview

1. **Bronze layer:** Read CSV files and store ingested data.
2. **Silver layer:** Remove duplicate rows and records with missing quantities.
3. **Gold layer:** Calculate sales totals, quantities, and row counts by product.

---

## 1. Bronze Layer: Raw Data Ingestion

**Objective:** Read CSV files from a Databricks Volume, convert `sales_amount` to a numeric type, and save the data into a Bronze table.

### Full code

```python
# ==========================================
# BRONZE LAYER: RAW DATA INGESTION
# ==========================================

from pyspark.sql.functions import col

# Step 1: Read CSV files from the Databricks Volume
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/Volumes/ecommerce_catalog/bronze/raw_order_files/*.csv")

# Step 2: Convert sales_amount to double
df = df.withColumn(
    "sales_amount",
    col("sales_amount").cast("double")
)

# Step 3: Save data to the Bronze table
df.write.mode("overwrite").saveAsTable(
    "ecommerce_catalog.bronze.sales_raw"
)

# Step 4: Display the data
display(df)
```

### Understand the code

| Code | Purpose |
|---|---|
| `spark.read.format("csv")` | Reads CSV files |
| `.option("header", "true")` | Uses the first row as column names |
| `.option("inferSchema", "true")` | Asks Spark to infer column data types |
| `.load(...)` | Reads matching CSV files from the Volume |
| `withColumn()` | Creates or replaces a column |
| `cast("double")` | Converts sales amount to a numeric type |
| `mode("overwrite")` | Replaces existing table data |
| `saveAsTable()` | Saves data as a named table |
| `display(df)` | Displays the DataFrame in Databricks |

**Input:** CSV files in the Databricks Volume.

**Output table:** `ecommerce_catalog.bronze.sales_raw`

**Remember:** Bronze is where source data enters the pipeline. This example performs a type conversion during ingestion. If a value cannot be converted to a number, the cast can produce `NULL`.

---

## 2. Silver Layer: Data Cleaning

**Objective:** Read the Bronze table, remove exact duplicate rows, filter out records where `quantity` is null, and save the cleaned data.

### Full code

```python
# ==========================================
# SILVER LAYER: DATA CLEANING
# ==========================================

from pyspark.sql.functions import col

# Step 1: Read data from the Bronze table
bronze_df = spark.table(
    "ecommerce_catalog.bronze.sales_raw"
)

# Step 2: Remove exact duplicate rows
silver_df = bronze_df.dropDuplicates()

# Step 3: Remove records where quantity is NULL
silver_df = silver_df.filter(
    col("quantity").isNotNull()
)

# Step 4: Save cleaned data to the Silver table
silver_df.write.mode("overwrite").saveAsTable(
    "ecommerce_catalog.silver.sales_clean"
)

# Step 5: Display cleaned data
display(silver_df)
```

### Understand the code

| Code | Purpose |
|---|---|
| `spark.table()` | Reads an existing table |
| `dropDuplicates()` | Removes rows identical across all columns |
| `filter()` | Keeps records that satisfy a condition |
| `isNotNull()` | Checks that quantity is not null |
| `saveAsTable()` | Saves the cleaned records |

**Input table:** `ecommerce_catalog.bronze.sales_raw`

**Output table:** `ecommerce_catalog.silver.sales_clean`

**Remember:** `dropDuplicates()` removes exact duplicate rows across all columns. It does not necessarily remove multiple records sharing the same order ID if other column values differ. `isNotNull()` removes null quantities, but it does not remove zero or negative quantities.

---

## 3. Gold Layer: Business Aggregation

**Objective:** Read the Silver table, group data by product, and calculate three business metrics.

### Full code

```python
# ==========================================
# GOLD LAYER: BUSINESS AGGREGATION
# ==========================================

from pyspark.sql.functions import sum, count

# Step 1: Read cleaned data from the Silver table
silver_df = spark.table(
    "ecommerce_catalog.silver.sales_clean"
)

# Step 2: Group data by product and calculate metrics
gold_df = silver_df.groupBy("product_name").agg(
    sum("sales_amount").alias("total_sales"),
    sum("quantity").alias("total_quantity"),
    count("*").alias("total_orders")
)

# Step 3: Save the aggregated data to the Gold table
gold_df.write.mode("overwrite").saveAsTable(
    "ecommerce_catalog.gold.sales_reportable_data"
)

# Step 4: Display the final report
display(gold_df)
```

### Understand the code

| Code | Purpose |
|---|---|
| `groupBy("product_name")` | Groups records by product |
| `sum("sales_amount")` | Calculates total sales per product |
| `sum("quantity")` | Calculates total quantity per product |
| `count("*")` | Counts rows per product |
| `alias()` | Renames output columns |
| `saveAsTable()` | Saves the aggregated table |

**Input table:** `ecommerce_catalog.silver.sales_clean`

**Output table:** `ecommerce_catalog.gold.sales_reportable_data`

**Important:** The Gold schema must exist before saving the table. The original code wrote to `ecommerce_catalog.silver.reporatble_data`, which placed aggregated data in the Silver schema and contained a spelling error. This version uses a Gold schema and the clearer table name `sales_reportable_data`.

`count("*")` counts rows per product, not necessarily distinct orders. If each order can contain multiple rows and you need a unique order count, use `countDistinct("order_id")` instead, provided `order_id` is the correct identifier.

---

## 4. Final Table Flow

```text
CSV files in Databricks Volume
            |
            v
BRONZE: ecommerce_catalog.bronze.sales_raw
Read and ingest source data
            |
            v
SILVER: ecommerce_catalog.silver.sales_clean
Remove exact duplicates and null quantities
            |
            v
GOLD: ecommerce_catalog.gold.sales_reportable_data
Aggregate sales and quantities by product
            |
            v
Business reports, dashboards, and analytics
```

---

## 5. How to Run the Notebooks

Run each layer in order:

1. **Bronze notebook:** Read the CSV files and create `sales_raw`.
2. **Silver notebook:** Read `sales_raw`, clean the records, and create `sales_clean`.
3. **Gold notebook:** Read `sales_clean`, calculate the metrics, and create `sales_reportable_data`.

Before running the Gold notebook, create the Gold schema if it does not already exist and you have the necessary permissions:

```sql
CREATE SCHEMA IF NOT EXISTS ecommerce_catalog.gold;
```

Run this SQL in a Databricks SQL cell or query editor. Confirm that the catalog, schema, Volume, and table permissions are configured correctly.

---

## 6. Quick Revision Notes

| Layer | Main operation | Output |
|---|---|---|
| Bronze | Read and ingest | Raw sales table |
| Silver | Clean and filter | Clean sales table |
| Gold | Group and aggregate | Product-level sales report |

### One-line interview explanation

> I built a PySpark Medallion pipeline in Databricks that ingests raw CSV sales data into Bronze, cleans duplicate and invalid records in Silver, and aggregates product-level sales metrics in Gold for reporting and analytics.

---

## 7. Key PySpark Functions

| Function | Meaning |
|---|---|
| `spark.read` | Reads source data |
| `spark.table()` | Reads an existing table |
| `col()` | References a column |
| `withColumn()` | Creates or replaces a column |
| `cast()` | Converts a column's data type |
| `dropDuplicates()` | Removes duplicate rows |
| `filter()` | Filters rows based on a condition |
| `isNotNull()` | Checks for non-null values |
| `groupBy()` | Groups records |
| `agg()` | Calculates aggregate values |
| `sum()` | Adds numeric values |
| `count()` | Counts rows or non-null values, depending on the expression |
| `saveAsTable()` | Saves a DataFrame as a table |
| `display()` | Displays results in a Databricks notebook |

## Important note about overwrite mode

All three examples use `.mode("overwrite")`. Each run replaces the existing table data. This is suitable for a simple full-refresh learning exercise, but a production pipeline may require incremental processing, validation, and a more deliberate write strategy.
