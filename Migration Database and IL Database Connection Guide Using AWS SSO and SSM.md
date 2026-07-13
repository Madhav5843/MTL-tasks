# Migration Database and IL Database Connection Guide Using AWS SSO and SSM

## Purpose

This document provides the steps for securely connecting to the Migration PostgreSQL Database and Migration IL Database using AWS SSO authentication and AWS Systems Manager (SSM) Port Forwarding.

This approach allows database access without exposing the database publicly and follows AWS security best practices.

***

# Prerequisites

Before starting, ensure the following:

* AWS CLI is installed and configured.
* AWS SSO access is available.
* AWS Session Manager Plugin is installed.
* Required AWS permissions are assigned.
* Database credentials are available through the approved credential management process.

***

# Architecture Overview

```text
Local Machine
      │
      ▼
AWS SSO Authentication
      │
      ▼
SSM Session Manager
      │
      ▼
EC2 Jump Host
(i-01a2fc8ff1fcb9fdf)
      │
      ▼
RDS Database
```

***

# Section 1: Connect to Migration PostgreSQL Database

## Step 1: Authenticate Using AWS SSO

Run the following command:

```bash
aws sso login --profile MigrationILLeads-971422672695
```

### Expected Result

A browser window opens and prompts for AWS authentication.

After successful login:

```text
Successfully logged into AWS
```

***

## Step 2: Start Port Forwarding Session

Run the following command:

```bash
aws --profile AWSAdministratorAccess-971422672695 \
--region eu-west-2 \
ssm start-session \
--target i-01a2fc8ff1fcb9fdf \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters host=ebs-mig-postgres-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com,portNumber="5432",localPortNumber="5433"
```

### Purpose

This command creates a secure tunnel between your local machine and the Migration PostgreSQL database.

### Connection Details

**Remote Database Host**

```text
ebs-mig-postgres-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com
```

**Remote Port**

```text
5432
```

**Local Port**

```text
5433
```

***

## Step 3: Connect to PostgreSQL Database

Once the SSM session is active, open another terminal and connect using:

```bash
psql -h localhost -p 5433 -d postgres -U ebsmigpgsdbuser
```

### Enter Database Password

Enter the approved database password when prompted.

### Expected Result

```text
postgres=>
```

This indicates a successful database connection.

***

## Step 4: Validate PostgreSQL Connectivity

### Verify Current Database

```sql
SELECT current_database();
```

### List Available Databases

```sql
\l
```

### List Tables

```sql
\dt
```

***

# Section 2: Connect to Migration IL Database

## Step 1: Authenticate Using AWS SSO

Run:

```bash
aws sso login --profile AWSAdministratorAccess-971422672695
```

### Expected Result

AWS authentication completes successfully.

***

## Step 2: Create SSM Port Forwarding Session

Run:

```bash
aws --profile AWSAdministratorAccess-971422672695 \
--region eu-west-2 \
ssm start-session \
--target i-01a2fc8ff1fcb9fdf \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters host=ebs-mig-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com,portNumber="4000",localPortNumber="4030"
```

### Connection Details

**IL Database Endpoint**

```text
ebs-mig-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com
```

**Database Port**

```text
4000
```

**Local Port**

```text
4030
```

***

## Step 3: Connect Using Database Client

Open DBeaver, MySQL Workbench, or your preferred SQL client.

### Connection Parameters

**Host**

```text
localhost
```

**Port**

```text
4030
```

**Database**

```text
Target IL Database
```

**Username**

```text
IL Database User
```

**Password**

```text
Approved Database Password
```

***

# Connection Validation

After connecting successfully, execute:

```sql
SHOW DATABASES;
```

Verify available databases are displayed.

### Verify Tables

```sql
SHOW TABLES;
```

### Verify Connectivity

```sql
SELECT NOW();
```

Expected output:

```text
Current timestamp returned successfully
```

***

# Troubleshooting

## AWS SSO Login Failure

Re-authenticate:

```bash
aws sso login --profile AWSAdministratorAccess-971422672695
```

***

## SSM Session Fails

Verify:

* Correct AWS Profile
* Correct AWS Region
* Valid Target Instance ID
* Required SSM permissions

***

## Database Connection Failure

Verify:

* Port forwarding session is still active.
* Correct local port is used.
* Database credentials are correct.
* VPN access (if required) is connected.

***

# Recommended Workflow

```text
1. AWS SSO Login
        ↓
2. Start SSM Port Forwarding
        ↓
3. Verify Session Established
        ↓
4. Connect to Database
        ↓
5. Validate Connectivity
        ↓
6. Execute Queries
        ↓
7. Complete Activity
        ↓
8. Disconnect Session
```

***

# Conclusion

This procedure provides a secure method for connecting to the Migration PostgreSQL and IL databases using AWS SSO and Systems Manager Port Forwarding. By leveraging SSM tunnels, database access remains secure, auditable, and compliant with AWS security standards while avoiding direct database exposure.
