# Incremental Data Loading in Databricks with Delta Lake

> **Purpose:** Beginner-friendly study notes on initial loads, incremental loads, and upserts using Apache Spark, Delta Lake, and `MERGE INTO`.

---

## Table of Contents

1. [What Is Incremental Data Loading?](#1-what-is-incremental-data-loading)
2. [Initial Load](#2-initial-load)
3. [Incremental Load](#3-incremental-load)
4. [Understanding MERGE INTO](#4-understanding-merge-into)
5. [Complete Example](#5-complete-example)
6. [What Each Part Does](#6-what-each-part-does)
7. [Useful Commands and Concepts](#7-useful-commands-and-concepts)
8. [Delta Lake Benefits](#8-delta-lake-benefits)
9. [Real-Time Data Flow](#9-real-time-data-flow)
10. [Best Practices](#10-best-practices)
11. [Quick Revision](#11-quick-revision)
12. [Interview Answer](#12-interview-answer)
13. [Practice Questions](#13-practice-questions)
14. [Revision Checklist](#14-revision-checklist)

---

## 1. What Is Incremental Data Loading?

**Incremental data loading** processes records that are new or have changed since the previous load, rather than reloading the entire dataset every time.

### Example

The target table already contains:

| order_id | customer_name | amount |
|---:|---|---:|
| 101 | Arun | 500 |
| 102 | Priya | 750 |

A new source file arrives:

| order_id | customer_name | amount |
|---:|---|---:|
| 102 | Priya | 800 |
| 103 | Karthik | 300 |

After an upsert:

| order_id | customer_name | amount |
|---:|---|---:|
| 101 | Arun | 500 |
| 102 | Priya | 800 |
| 103 | Karthik | 300 |

- Order `102` already exists, so its amount is updated from `750` to `800`.
- Order `103` is new, so it is inserted.
- Order `101` remains unchanged.

> **Incremental load = process new and changed records without rebuilding the entire target dataset.**

---

## 2. Initial Load

The **initial load** creates or populates the target table with the first batch of source data.

```python
initial_df = spark.read.csv(
    "/Volumes/ecommerce_catalog/bronze/raw_order_files/orders_day1.csv",
    header=True,
    inferSchema=True
)

initial_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_db.orders")
```

### Explanation

- `spark.read.csv(...)`: Reads a CSV file into a Spark DataFrame.
- `header=True`: Uses the first row as column names.
- `inferSchema=True`: Asks Spark to infer column data types from the data.
- `.format("delta")`: Writes data in Delta Lake format.
- `.mode("overwrite")`: Replaces existing target data if the table already exists.
- `.saveAsTable("retail_db.orders")`: Saves the DataFrame as the `orders` table in the `retail_db` schema/database.

**Important:** `overwrite` can replace existing data. Use it intentionally, especially in production.

---

## 3. Incremental Load

An incremental load reads the next batch of arriving data.

```python
incremental_df = spark.read.csv(
    "/Volumes/ecommerce_catalog/bronze/raw_order_files/orders_day2.csv",
    header=True,
    inferSchema=True
)
```

This reads the new CSV into a DataFrame. It does not update the target table by itself.

### Create a temporary view

```python
incremental_df.createOrReplaceTempView("source_orders")
```

This exposes the DataFrame as a temporary SQL view named `source_orders`, so it can be referenced in Spark SQL.

The view is temporary to the current Spark session and is not a permanent table.

---

## 4. Understanding `MERGE INTO`

Delta Lake's `MERGE INTO` can perform an **upsert**: update matching records and insert records that do not yet exist.

```sql
MERGE INTO retail_db.orders AS target
USING source_orders AS source
ON target.order_id = source.order_id

WHEN MATCHED THEN
  UPDATE SET
    target.customer_name = source.customer_name,
    target.amount = source.amount

WHEN NOT MATCHED THEN
  INSERT (order_id, customer_name, amount)
  VALUES (source.order_id, source.customer_name, source.amount)
```

### How it works

1. `MERGE INTO retail_db.orders AS target`: Specifies the existing target table.
2. `USING source_orders AS source`: Specifies the incoming records.
3. `ON target.order_id = source.order_id`: Matches rows by `order_id`, the business key in this example.
4. `WHEN MATCHED THEN UPDATE`: If the ID exists in both source and target, update the specified columns.
5. `WHEN NOT MATCHED THEN INSERT`: If a source ID is absent from the target, insert the source row.

### Visual flow

```text
Incoming source record
          |
          v
 Is order_id in target?
       /       \
     Yes        No
      |          |
   UPDATE      INSERT
      \          /
       v        v
     Target Delta table
```

**Note:** This example updates every matched row, even if values have not changed. A production pipeline can add a condition to update only when relevant columns differ.

---

## 5. Complete Example

### Step 1: Initial load

```python
initial_df = spark.read.csv(
    "/Volumes/ecommerce_catalog/bronze/raw_order_files/orders_day1.csv",
    header=True,
    inferSchema=True
)

initial_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_db.orders")
```

### Step 2: Read the next batch

```python
incremental_df = spark.read.csv(
    "/Volumes/ecommerce_catalog/bronze/raw_order_files/orders_day2.csv",
    header=True,
    inferSchema=True
)
```

### Step 3: Register a temporary view

```python
incremental_df.createOrReplaceTempView("source_orders")
```

### Step 4: Merge source data into the target

```python
spark.sql("""
MERGE INTO retail_db.orders AS target
USING source_orders AS source
ON target.order_id = source.order_id

WHEN MATCHED THEN
  UPDATE SET
    target.customer_name = source.customer_name,
    target.amount = source.amount

WHEN NOT MATCHED THEN
  INSERT (
    order_id,
    customer_name,
    amount
  )
  VALUES (
    source.order_id,
    source.customer_name,
    source.amount
  )
""")
```

### Step 5: Display the result

```python
display(spark.table("retail_db.orders"))
```

This displays the final contents of the target table in a Databricks notebook.

---

## 6. What Each Part Does

| Code / concept | Purpose |
|---|---|
| `spark.read.csv()` | Reads CSV data into a DataFrame |
| `header=True` | Treats the first row as column names |
| `inferSchema=True` | Infers column data types |
| `format("delta")` | Writes data in Delta Lake format |
| `mode("overwrite")` | Replaces existing target data |
| `saveAsTable()` | Saves a DataFrame as a table |
| `createOrReplaceTempView()` | Makes a DataFrame queryable through SQL in the current session |
| `MERGE INTO` | Applies updates and inserts based on a match condition |
| `WHEN MATCHED` | Defines what happens when a source row matches a target row |
| `WHEN NOT MATCHED` | Defines what happens when a source row has no target match |
| `display()` | Displays the result in a Databricks notebook |

---

## 7. Useful Commands and Concepts

### `overwrite`

Replaces existing data in the target being written.

```python
df.write.format("delta").mode("overwrite").saveAsTable("retail_db.orders")
```

Use carefully. It is not the usual choice for a recurring incremental load.

### `append`

Adds rows to the target rather than replacing existing data.

```python
df.write.format("delta").mode("append").saveAsTable("retail_db.orders")
```

Append alone does not deduplicate records or update existing orders. Repeated input can create duplicate rows unless the pipeline handles them.

### `left_anti` join

Returns rows from the left DataFrame that have no matching row in the right DataFrame. It can help find new keys.

```python
new_records_df = source_df.join(
    target_df,
    on="order_id",
    how="left_anti"
)
```

This identifies source records whose `order_id` does not exist in the target. It does **not** identify changed records by itself.

### `MERGE`

Use `MERGE` when you need to update existing rows and insert new rows based on a matching key.

> **Remember:** `left_anti` helps identify new records. `MERGE` can handle both new records and updates in one operation.

---

## 8. Delta Lake Benefits

Delta Lake tables support capabilities useful for data engineering pipelines, including:

- **ACID transactions:** Helps maintain consistent table updates.
- **UPDATE, DELETE, and MERGE:** Supports modifying existing table data.
- **Time Travel:** Can query previous table versions when history is available and retained.
- **Schema enforcement and schema evolution:** Helps validate or manage schema changes. Evolution behavior depends on configuration and the operation used.

---

## 9. Real-Time Data Flow

A simplified data-lake flow:

```text
Source files
     ↓
Bronze layer
(raw ingestion)
     ↓
Silver layer
(cleaning, validation, MERGE / upsert)
     ↓
Gold layer
(aggregations and business-ready datasets)
```

In this example:
- `orders_day1.csv` provides the initial batch.
- `orders_day2.csv` provides the incremental batch.
- `retail_db.orders` is the Delta target table.

Bronze/Silver/Gold placement varies by architecture. The flow above is a common learning pattern, not a mandatory design.

---

## 10. Best Practices

1. **Ensure the target is a Delta table.** Delta Lake `MERGE INTO` requires a supported Delta target.
2. **Check the match key.** `order_id` should uniquely identify an order for this example.
3. **Avoid duplicate source keys.** Multiple source rows matching the same target row can cause a `MERGE` to fail or behave ambiguously. Deduplicate or resolve them before merging.
4. **Handle schema deliberately.** `inferSchema=True` is convenient for learning, but explicit schemas are often more predictable in production.
5. **Be careful with `overwrite`.** It can replace target data and is used here for the initial load.
6. **Plan for repeat runs.** A well-designed upsert pipeline should be idempotent for the same input batch, assuming source keys and update logic are handled consistently.
7. **Handle deletes separately.** This example updates matching records and inserts new records. It does not delete target rows missing from the source.
8. **Add data-quality checks.** Validate required columns, null keys, duplicate IDs, and unexpected amounts before merging.

---

## 11. Quick Revision

```text
Initial load
    ↓
Read orders_day1.csv
    ↓
Write as Delta table with overwrite
    ↓
retail_db.orders

Incremental load
    ↓
Read orders_day2.csv
    ↓
Create temporary view: source_orders
    ↓
MERGE using order_id
    ├── Match found     → UPDATE
    └── No match found  → INSERT
    ↓
Display final target table
```

### Key commands

| Command | Meaning |
|---|---|
| `overwrite` | Replace existing target data |
| `append` | Add rows |
| `left_anti` | Find left-side rows with no match on the right |
| `MERGE INTO` | Update matching rows and insert non-matching rows |
| `saveAsTable()` | Save a DataFrame as a table |

---

## 12. Interview Answer

**Question: What is incremental data loading, and how do you implement it in Databricks?**

**Answer:**

Incremental data loading processes only new or changed records instead of reloading the complete dataset each time. In Databricks, I can read the incoming batch into a Spark DataFrame, register it as a temporary view, and use Delta Lake `MERGE INTO` to compare it with the target table using a business key such as `order_id`. Matching records are updated, and non-matching records are inserted. This reduces unnecessary full reloads and supports reliable upsert workflows.

---

## 13. Practice Questions

<details>
<summary><strong>Q1. What is incremental data loading?</strong></summary>

**Answer:** Processing new or changed records instead of reloading the entire dataset each time.
</details>

<details>
<summary><strong>Q2. What is an initial load?</strong></summary>

**Answer:** The first load that creates or populates the target with the starting dataset.
</details>

<details>
<summary><strong>Q3. What does `mode("overwrite")` do?</strong></summary>

**Answer:** Replaces existing data in the write target. Use it carefully.
</details>

<details>
<summary><strong>Q4. Why create a temporary view?</strong></summary>

**Answer:** It allows the incoming DataFrame to be referenced by name in Spark SQL.
</details>

<details>
<summary><strong>Q5. What is an upsert?</strong></summary>

**Answer:** A combination of updating existing records and inserting records that do not exist.
</details>

<details>
<summary><strong>Q6. What does `WHEN MATCHED` do in this example?</strong></summary>

**Answer:** Updates the target row when its `order_id` matches a source row.
</details>

<details>
<summary><strong>Q7. What does `WHEN NOT MATCHED` do?</strong></summary>

**Answer:** Inserts the source row when its `order_id` is not present in the target.
</details>

<details>
<summary><strong>Q8. What does a `left_anti` join find?</strong></summary>

**Answer:** Rows from the left DataFrame with no matching key in the right DataFrame.
</details>

<details>
<summary><strong>Q9. Does this `MERGE` delete records missing from the source?</strong></summary>

**Answer:** No. The example only updates matching records and inserts non-matching source records.
</details>

<details>
<summary><strong>Q10. Name two Delta Lake benefits.</strong></summary>

**Answer:** Examples include ACID transactions, `MERGE` support, and Time Travel.
</details>

---

## 14. Revision Checklist

- [ ] Explain initial load vs incremental load.
- [ ] Explain what `overwrite` does and why it needs care.
- [ ] Explain why the source DataFrame is registered as a temporary view.
- [ ] Describe the `MERGE INTO` match condition.
- [ ] Explain `WHEN MATCHED` and `WHEN NOT MATCHED`.
- [ ] Explain the difference between `append`, `left_anti`, and `MERGE`.
- [ ] Name important Delta Lake capabilities.
- [ ] Identify that this example does not process deletes.
- [ ] Explain the pipeline in an interview without reading the notes.

---

**End of Incremental Data Loading in Databricks notes.**
