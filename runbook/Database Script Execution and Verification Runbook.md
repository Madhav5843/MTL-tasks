# Database Script Execution and Verification Runbook

## Purpose

This runbook provides the standard procedure for executing database deployment scripts and validating the changes in the EBS environment. It covers database connectivity, script execution, schema validation, and post-deployment verification steps.

***

# Overview

Database deployment scripts are executed to introduce schema changes, create new database objects, update application versions, and support new functionality. After script execution, validation activities ensure all changes have been applied correctly.

***

# Environment Details

| Component   | Value                   |
| ----------- | ----------------------- |
| Environment | Staging / Production    |
| Database    | ebsstgildb / ebsprdildb |
| Host        | RDS Database Endpoint   |
| Port        | 4000                    |
| Namespace   | ebs-stg / ebs-prd       |

***

# Step 1: Connect to Bastion Server

## Objective

Access the Bastion server used for database deployment activities.

### Navigate to Temporary Directory

```bash
cd /tmp
```

### Verify Directory Contents

```bash
ls
```

### Purpose

The `/tmp` directory is commonly used to temporarily store deployment scripts before execution.

***

# Step 2: Create or Upload SQL Script

## Objective

Place the deployment script on the server before execution.

### Create SQL File

```bash
vi Sprint2025-50-3.3.3-V1.sql
```

### Verify Script Contents

```bash
cat Sprint2025-50-3.3.3-V1.sql
```

### Validation

Ensure the script contains the expected:

* CREATE TABLE statements
* ALTER TABLE statements
* INSERT statements
* Version update statements

***

# Step 3: Connect to the Database

## Objective

Establish a connection to the target database before executing the deployment script.

### Connect to Staging Database

```bash
mysql -h ebs-stg-cluster.cluster-choa4mcgcwjd.eu-west-2.rds.amazonaws.com -P 4000 -u ebsstgdbuser -p
```

### Connect to Production Database

```bash
mysql -h ebs-prd-cluster.cluster-cx4mgs2e2dub.eu-west-2.rds.amazonaws.com -P 4000 -u prddbuser -p
```

### Authentication

Enter the database password when prompted.

### Expected Result

Successful connection to the MySQL database.

Example:

```text
Welcome to the MySQL monitor.
```

***

# Step 4: Execute the Deployment Script

## Objective

Execute the SQL deployment script against the target database.

### Command

```sql
source /tmp/Sprint2025-52-3.3.1-V1.sql;
```

### Purpose

The script may perform:

* Table creation
* Table modifications
* Index creation
* Data updates
* Version updates

***

# Expected Output

Example:

```text
Query OK
Database changed
```

### What This Means

The script executed successfully and the database changes have been applied.

***

# Step 5: Validate Database Changes

## Objective

Verify that all required database objects and changes were created successfully.

### Display Available Databases

```sql
SHOW DATABASES;
```

### Select Target Database

For Staging:

```sql
USE ebsstgildb;
```

For Production:

```sql
USE ebsprdildb;
```

### Display Available Tables

```sql
SHOW TABLES;
```

***

# Validation Activities

Verify that all expected database objects are present.

### Example Validation Checklist

| Validation Item     | Expected Result      |
| ------------------- | -------------------- |
| t\_hpi\_data table  | Created Successfully |
| t\_collateral table | Created Successfully |
| t\_batch table      | Altered Successfully |
| t\_account table    | Altered Successfully |
| t\_version table    | Updated Successfully |

***

# Version Verification

## Objective

Confirm that the application/database version has been updated as part of the deployment.

### Example Query

```sql
SELECT *
FROM t_version;
```

### Validation

Verify that the version displayed matches the release version being deployed.

Example:

```text
Sprint2025-52-3.3.1
```

***

# Step 6: Exit the Database

After validation is complete, exit the database session.

```sql
exit
```

### Expected Result

The MySQL session closes successfully.

***

# Step 7: Verify Kubernetes CronJobs

## Objective

Validate that application CronJobs are available after deployment.

### Check CronJobs in Staging

```bash
kubectl get cronjobs -n ebs-stg
```

### Check CronJobs in Production

```bash
kubectl get cronjobs -n ebs-prd
```

***

# Expected Output

Example:

```text
NAME                                  SCHEDULE
mtl-hpi-valuation-job-deployment      0 0 1 1,4,7,10 *
mtl-bacs-report-job-deployment        0 9 * * *
mtl-interest-payment-job-deployment   0 2 * * *
```

### Validation

Verify:

* CronJobs are present.
* Schedules appear correctly.
* Required jobs are available.

***

# Post-Deployment Validation

After deployment, the following checks should be completed:

### Database Validation

✅ Tables created successfully

✅ Table alterations applied

✅ Indexes created successfully

✅ Version updated

***

### Kubernetes Validation

✅ CronJobs available

✅ No missing scheduled jobs

✅ Cluster resources healthy

***

### Application Validation

✅ Application services operational

✅ No deployment-related alerts

✅ No database connectivity errors

***

### Log Validation

Verify CloudWatch or application logs for:

* SQL exceptions
* Database connection errors
* Deployment failures
* Application startup issues

***

# Recommended Deployment Workflow

```text
1. Connect to Bastion Server
        ↓
2. Upload/Create SQL Script
        ↓
3. Connect to Database
        ↓
4. Execute Deployment Script
        ↓
5. Validate Database Changes
        ↓
6. Verify Version Update
        ↓
7. Verify Tables and Schema
        ↓
8. Exit Database
        ↓
9. Verify Kubernetes CronJobs
        ↓
10. Validate Application Health
        ↓
11. Monitor Logs and Alerts
```

***

# Key Notes

* Always execute and validate scripts in Staging before deploying to Production.
* Review the deployment script before execution to understand the changes being applied.
* Verify all schema updates after deployment.
* Validate version updates against the release package.
* Retain deployment scripts in source control for audit and rollback purposes.
* Capture evidence of successful validation for future reference and compliance requirements.

***

# Conclusion

This runbook provides a standardized process for executing database deployment scripts and validating successful deployment in the EBS environment. Following these steps ensures that schema changes, table modifications, and version updates are applied correctly and safely to both Staging and Production environments.
