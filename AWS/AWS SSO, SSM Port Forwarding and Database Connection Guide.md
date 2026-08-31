# AWS SSO, SSM Port Forwarding and Database Connection Guide

## Purpose

This document describes the steps required to establish secure connectivity to the Migration PostgreSQL Database and IL Database using AWS SSO authentication, AWS Systems Manager (SSM) port forwarding, and database client connections.

***

# Overview

Direct access to Migration and IL databases is restricted. Access is established through:

1. AWS SSO Authentication
2. AWS Systems Manager Session Manager
3. Secure Port Forwarding through a Bastion/EC2 Instance
4. Database Client Connection

This approach avoids opening database ports publicly and ensures secure access.

***

# Prerequisites

Before connecting:

* AWS CLI must be installed.
* AWS SSO must be configured.
* Access to the AWS account must be available.
* Session Manager Plugin must be installed.
* Database credentials must be available.

***

# 1. Login Using AWS SSO

## Objective

Authenticate with AWS using Single Sign-On (SSO).

### Command

```bash
aws sso login --profile MigrationILLeads-971422672695
```

or

```bash
aws sso login --profile AWSAdministratorAccess-971422672695
```

### Expected Result

A browser window opens and prompts for AWS authentication.

After successful login:

```text
Successfully logged into Start URL
```

***

# 2. Establish Port Forwarding for Migration PostgreSQL Database

## Objective

Create a secure tunnel from the local machine to the PostgreSQL database through Systems Manager Session Manager.

### Command

```bash
aws --profile AWSAdministratorAccess-971422672695 \
--region eu-west-2 \
ssm start-session \
--target i-01a2fc8ff1fcb9fdf \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters host=ebs-mig-postgres-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com,portNumber="5432",localPortNumber="5433"
```

***

## Parameter Explanation

### Target Instance

```text
i-01a2fc8ff1fcb9fdf
```

EC2 instance used as the jump host.

### Remote Host

```text
ebs-mig-postgres-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com
```

Migration PostgreSQL database endpoint.

### Remote Port

```text
5432
```

Default PostgreSQL port.

### Local Port

```text
5433
```

Port exposed locally on the workstation.

***

## Expected Result

Connection is established successfully.

Example:

```text
Starting session with SessionId:
Port 5433 opened for session
```

Keep this terminal open while using the database connection.

***

# 3. Connect to Migration PostgreSQL Database

## Objective

Connect to the PostgreSQL database after port forwarding has been established.

### Command

```bash
psql -h localhost -p 5433 -d postgres -U ebsmigpgsdbuser
```

### Password

Enter the database password when prompted.

### Expected Result

```text
postgres=>
```

Successful PostgreSQL session established.

***

# 4. Validate PostgreSQL Connection

## Display Databases

```sql
\l
```

### Display Current Database

```sql
SELECT current_database();
```

### Display Available Tables

```sql
\dt
```

***

# 5. Establish Port Forwarding for IL Database

## Objective

Create a secure session to access the Migration IL Database.

### Login to AWS

```bash
aws sso login --profile AWSAdministratorAccess-971422672695
```

### Start Port Forwarding Session

```bash
aws --profile AWSAdministratorAccess-971422672695 \
--region eu-west-2 \
ssm start-session \
--target i-01a2fc8ff1fcb9fdf \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters host=ebs-mig-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com,portNumber="4000",localPortNumber="4030"
```

***

## Parameter Details

### Database Host

```text
ebs-mig-cluster.cluster-c76u0qu0mgx9.eu-west-2.rds.amazonaws.com
```

Migration IL Database endpoint.

### Database Port

```text
4000
```

IL database listener port.

### Local Port

```text
4030
```

Local port used for connectivity.

***

# 6. Connect to IL Database

After the port forwarding session is established, connect using a database client such as:

* DBeaver
* MySQL Client
* SQL IDE

## Connection Parameters

### Host

```text
localhost
```

### Port

```text
4030
```

### Database

```text
Target IL Database
```

### Username

```text
Configured IL Database User
```

### Password

```text
Configured Database Password
```

***

# Validation Checks

After successful connection, perform the following checks:

### Verify Databases

```sql
SHOW DATABASES;
```

### Verify Tables

```sql
SHOW TABLES;
```

### Verify Connectivity

```sql
SELECT NOW();
```

Expected result:

```text
Current timestamp returned successfully
```

***

# Troubleshooting

## AWS SSO Authentication Failure

### Resolution

Re-authenticate:

```bash
aws sso login --profile AWSAdministratorAccess-971422672695
```

***

## Port Forwarding Session Fails

### Verify

* Correct AWS profile
* Correct EC2 instance ID
* Correct database endpoint
* Session Manager permissions

***

## Database Connection Refused

### Verify

* SSM session is still active
* Local port matches the configured port forwarding
* Database credentials are correct

***

# Recommended Connection Flow

```text
1. AWS SSO Login
        ↓
2. Start SSM Port Forwarding Session
        ↓
3. Verify Session Established
        ↓
4. Connect to Database
        ↓
5. Validate Connectivity
        ↓
6. Execute Queries
        ↓
7. Complete Investigation/Activity
        ↓
8. Disconnect Session
```

***

# Conclusion

This procedure provides a secure method for accessing Migration PostgreSQL and IL databases using AWS SSO and Systems Manager port forwarding. Following these steps ensures secure database connectivity while maintaining compliance with AWS security best practices and eliminating the need for direct database exposure.
