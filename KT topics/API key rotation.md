## 1. What is this email about?

The email discussion is about rotating AWS access keys used by the Airflow environment in the **ebs-prd (production)** environment. This activity was raised because of a Vanta compliance/security task[...]

# 2. What is the main concern?

The main concern raised by [Shivam Nanda](https://www.office.com/search?q=Shivam+Nanda\&EntityRepresentationId=6c25240f-7196-412d-b06d-d9b040a2ea65) is:

> Before restarting Airflow, the team must identify DAG execution schedules because restarting Airflow while DAGs are running could impact ongoing workflows.

In simple words:

```text
If Airflow is restarted
            while
A workflow/job is running
            ↓
That job may fail or get interrupted
```

For this reason, the team wants to check whether any DAGs are running before proceeding.

# 3. What is Apache Airflow?

Apache Airflow is a workflow orchestration and job scheduling platform.

Think of it as a central scheduler that automatically runs business processes, data pipelines, imports, exports, reports, and other automated tasks.

Example:

```text
06:00 AM  Download data
06:05 AM  Validate data
06:10 AM  Process data
06:20 AM  Update database
06:30 AM  Send notifications
```

Instead of a person performing these tasks manually every day, Airflow executes them automatically.

You can think of Airflow as:

```text
Windows Task Scheduler
          +
Workflow Controller
          +
Automation Engine
```

# 4. What is a DAG?

DAG stands for:

```text
Directed Acyclic Graph
```

In Airflow, a DAG is simply a workflow.

Example:

```text
Step 1 → Fetch data
            ↓
Step 2 → Validate data
            ↓
Step 3 → Process data
            ↓
Step 4 → Create report
            ↓
Step 5 → Send report
```

This entire flow is called a DAG.

Airflow reads the DAG and executes each task in the correct order.

# 5. What are DAG schedules?

Every DAG has a schedule.

Examples:

```text
Customer Import DAG
Runs daily at 6:00 AM

Transaction Sync DAG
Runs every hour

Statement Generation DAG
Runs daily at 8:00 PM
```

Airflow automatically starts the DAG at the configured time.

Because of this, before restarting Airflow the team needs to know:

```text
When does each DAG run?
Is any DAG currently running?
Is any DAG scheduled to run soon?
```

This is exactly what [Shivam Nanda](https://www.office.com/search?q=Shivam+Nanda\&EntityRepresentationId=6c25240f-7196-412d-b06d-d9b040a2ea65) is trying to verify.

# 6. What is AWS doing here?

Airflow is using AWS resources.

Airflow may connect to services such as:

```text
AWS S3
AWS RDS
AWS Lambda
AWS SNS
AWS Redshift
Other AWS Services
```

To access those AWS services, Airflow uses AWS credentials.

```text
Access Key
Secret Key
```

These credentials allow Airflow to authenticate with AWS.

# 7. What is Key Rotation?

Key rotation means replacing old AWS credentials with new ones.

Example:

```text
Old Access Key
      ↓
Remove/Deactivate

New Access Key
      ↓
Create and Update
```

Key rotation is important because:

* Improves security
* Reduces risk if credentials are exposed
* Meets compliance requirements
* Satisfies Vanta security checks

That is why [Deepak Monga](https://www.office.com/search?q=Deepak+Monga\&EntityRepresentationId=9c5f0728-2d75-4b3a-9700-7f76e0464f5c) raised this activity.

# 8. Why does Airflow need a restart?

Imagine Airflow is already running with old credentials loaded into memory.

```text
Airflow
   ↓
Using Old AWS Key
```

If the key changes:

```text
Airflow
   ↓
Still remembers old key
```

Therefore:

```text
Update Key
      ↓
Restart Airflow
      ↓
Load New Key
      ↓
Continue working
```

This is why the email mentions restarting Airflow.

# 9. Why can't they restart immediately?

Suppose this DAG is running:

```text
Transaction Import DAG

Step 1  Download File    ✅
Step 2  Validate File    ✅
Step 3  Process Data     RUNNING
Step 4  Update DB
```

If Airflow is restarted during Step 3:

```text
Download File    ✅
Validate File    ✅
Process Data     ❌ Interrupted
Update DB        ❌ Not Executed
```

This could result in:

* Failed jobs
* Partial processing
* Missing records
* Business impact

Therefore they first need to verify the DAG schedule and current execution status.

# 10. What needs to be done?

The expected process is:

### Step 1

Identify all DAGs.

### Step 2

Check their schedules.

### Step 3

Verify no DAG is currently running.

### Step 4

Confirm there are no important DAGs scheduled during the maintenance window.

### Step 5

Rotate AWS access keys.

### Step 6

Restart Airflow.

### Step 7

Verify Airflow starts successfully.

### Step 8

Verify DAGs continue running normally.

# 11. What is [Shivam Nanda](https://www.office.com/search?q=Shivam+Nanda\&EntityRepresentationId=6c25240f-7196-412d-b06d-d9b040a2ea65) specifically doing?

According to the email:

* He understands that most DAGs run during morning hours.
* He wants to confirm whether any DAGs run later during IST hours.
* Only after that confirmation will the restart activity proceed safely.

# 12. One-Line Summary

**The team needs to rotate AWS access keys used by Airflow in the production environment. Since restarting Airflow is required, they first need to check all Airflow DAG schedules and ensure no wo[...]

As an L2 Support Engineer, the simplest way to remember it is:

```text
Airflow = Job Scheduler

DAG = Workflow/Job

AWS Key = Credential

Key Rotation = Security Requirement

Restart Airflow = Load New Key

Check DAGs First = Avoid Job Failures
```