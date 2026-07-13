Manually executing and validating the **Deposit Transaction Import Batch Job** in Production (`ebs-prd`) and also performing a **database product name update** in the IL database.

***

# 📘 Deposit Transaction Import Job – L2 Support Notes

## 🎯 Purpose

The Deposit Transaction Import Job is a scheduled Kubernetes CronJob that imports deposit transaction data into the application.

Normally it runs automatically, but sometimes Support teams need to:

* Re-run the job manually
* Validate if processing completed
* Check logs for failures
* Confirm database status
* Verify CloudWatch logs

***

# Step 1: Trigger the Job Manually

### What this does

Creates and starts a new Kubernetes Job using an existing CronJob configuration.

### Command

```bash
kubectl create job \
--from=cronjob/mtl-deposit-transaction-import-job-deployment \
mtl-deposit-transaction-import-job-deployment-`date +%s` \
-n ebs-prd
```
kubectl create job --from=cronjob/mtl-deposit-transaction-import-job-deployment mtl-deposit-transaction-import-job-deployment-`date +%s` -n ebs-prd

### Explanation

| Part           | Meaning                            |
| -------------- | ---------------------------------- |
| create job     | Create a one-time execution        |
| --from=cronjob | Use existing CronJob configuration |
| date +%s       | Adds timestamp to job name         |
| -n ebs-prd     | Execute in production namespace    |

### Expected Result

A job gets created successfully.

Example:

```bash
job.batch/mtl-deposit-transaction-import-job-deployment-1723456789 created
```

***

# Step 2: Verify Job Creation

### Command

```bash
kubectl get jobs -n ebs-prd
```

### Purpose

Ensure the job was created.

### Example Output

```bash
NAME                                  COMPLETIONS   DURATION
mtl-deposit-transaction-import-job    0/1
```

### What to Check

✅ Job exists

✅ No creation failures

***

# Step 3: Get the Job Pod

Every Job creates a Pod.

### Command

```bash
kubectl get pods -n ebs-prd
```

### Filter Deposit Pods

```bash
kubectl get pods -n ebs-prd | grep -i deposit
```

### Purpose

Identify the exact pod running the job.

Example:

```bash
mtl-deposit-transaction-import-job-abcd123
```

***

# Step 4: Monitor Logs

## Live Monitoring

```bash
kubectl logs -f <pod-name> -n ebs-prd
```

Example:

```bash
kubectl logs -f mtl-deposit-transaction-import-job-abcd123 -n ebs-prd
```

### What to Check

Look for:

✅ Records imported

✅ Processing completed

❌ Exceptions

❌ Database errors

❌ Connection failures

***

## Search Import Logs

```bash
kubectl logs <pod-name> -n ebs-prd | grep -i import
```

Example:

```bash
Imported 200 transactions
Import completed successfully
```

***

# Step 5: Validate in Database (DBeaver)

## Purpose

Verify whether the batch execution updated database status.

***

## Check Latest Run

```sql
SELECT batch_name,
       last_run_time,
       batch_status
FROM t_batch
WHERE batch_name = 'DEPOSIT_TRANSACTION_IMPORT'
ORDER BY last_run_time DESC
LIMIT 1;
```

### Expected Output

```text
batch_name                  : DEPOSIT_TRANSACTION_IMPORT
last_run_time               : 2026-07-06 09:30:15
batch_status                : SUCCESS
```

***

## Check Last 5 Executions

```sql
SELECT batch_name,
       last_run_time,
       batch_status
FROM t_batch
WHERE batch_name = 'DEPOSIT_TRANSACTION_IMPORT'
ORDER BY last_run_time DESC
LIMIT 5;
```

### Purpose

Review execution history.

***

# Step 6: Verify CloudWatch Logs

## Why?

Kubernetes logs may disappear after pod termination.

CloudWatch keeps centralized logs.

***

## Quick Search

```sql
fields @timestamp, @message
| filter @message like /depositTransactionImportJob/
| sort @timestamp desc
| limit 50
```

### Purpose

Check latest import activity.

***

## Transaction-Level Search

```sql
fields @message
| filter @message like /c7f78d0d-93b5-422d-a1d3-9d2884cf0971/
| filter @message not like /EXITED/
| filter @message not like /ENTERED/
| filter @message not like /CALLED/
| sort @timestamp
```

### Purpose

Trace a specific transaction or request.

***

# Step 7: Validate CronJob Configuration

### CronJobs

```bash
kubectl get cronjobs -n ebs-prd
```

### Jobs

```bash
kubectl get jobs -n ebs-prd
```

### Verify

✅ CronJob exists

✅ Schedule is configured

✅ Jobs are being generated

***

# Step 8: Additional Pod Verification

## List Pods

```bash
kubectl get pods -n ebs-prd
```

## Search Deposit Logs

```bash
kubectl logs <pod-name> -n ebs-prd | grep -i deposit
```

### Verify

* Deposit records processed
* No failures
* Successful completion messages

***

# ✅ Final Success Criteria

The job is considered successful when:

### Kubernetes

✅ Job Created

✅ Pod Started

✅ Pod Completed

```bash
kubectl get jobs -n ebs-prd
```

Shows:

```bash
COMPLETIONS 1/1
```

***

### Logs

✅ No exceptions

✅ Import completed messages

***

### Database

```sql
batch_status = SUCCESS
```

or

```sql
batch_status = COMPLETED
```

***

### CloudWatch

✅ Successful execution logs visible

***

# 📘 Additional Task – Update Product Name in IL DB

There is a second activity mentioned at the bottom.

***

## Purpose

Update product names in table:

```sql
t_mortgage_custom_product_parameters
```

***

## Step 1: Search Product

Example Product ID:

```text
ROSRV002508060
```

### Query

```sql
SELECT *
FROM t_mortgage_custom_product_parameters
WHERE product_id = 'ROSRV002508060';
```

***

## Step 2: Find Parameter Name

Locate record where:

```text
param_name = product_name
```

Example:

| product\_id    | param\_name   | param\_value |
| -------------- | ------------- | ------------ |
| ROSRV002508060 | product\_name | Old Value    |

***

## Step 3: Update Product Name

Example:

```sql
UPDATE t_mortgage_custom_product_parameters
SET param_value = 'Offsite Build Mortgage'
WHERE product_id = 'ROSRV002508060'
AND param_name = 'product_name';
```

***

## Step 4: Verify Update

```sql
SELECT *
FROM t_mortgage_custom_product_parameters
WHERE product_id='ROSRV002508060'
AND param_name='product_name';
```

Expected:

```text
param_value = Offsite Build Mortgage
```

***

# 🚀 Quick L2 Support Execution Flow

```text
1. Trigger Job
   ↓
2. Verify Job Created
   ↓
3. Find Pod
   ↓
4. Monitor Logs
   ↓
5. Check DB Status (t_batch)
   ↓
6. Check CloudWatch Logs
   ↓
7. Verify Job Completed
   ↓
8. Update Product Name (if requested)
   ↓
9. Validate Update
   ↓
10. Close Ticket
```

### Interview/Support Summary

> This runbook is used to manually execute the Deposit Transaction Import batch in Kubernetes, validate execution using pod logs, CloudWatch logs, and database batch status, and perform mortgage product parameter updates in the IL database when required. The success of the activity is confirmed through Kubernetes job completion, CloudWatch log validation, and `t_batch` status changing to `SUCCESS` or `COMPLETED`.
