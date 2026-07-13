# Notes – Dashboard Discussion Summary

## Overview

* The dashboard shown is a key operational status dashboard used for bank operations.
* It provides a consolidated view of:
  * AWS & Infrastructure Health
  * Mobile Application & Notifications
  * Batch Job Status
  * Database Job Status
  * System Monitoring (availability, failures, alerts)
  * Business Metrics (logs, accounts, statements, transactions, etc.)

## Josh's Key Message

* This dashboard should be the target model for our team.
* There are approximately 7 dashboards in total, but this is the most important one.
* Achieving even 50% of the functionality and visibility shown here would be a strong start.
* Remaining enhancements can be added gradually over time.

***

## Expectations for Mahesh & Team

### 1. Understand the Dashboard Structure

Need to identify:

* What each widget/component represents.
* Data sources behind each widget.
* Health indicators (Healthy vs Failed/Warning states).
* Dependencies between systems and services.

Examples:

* AWS metrics → CloudWatch
* Job status → Batch scheduler/DB
* Service health → Monitoring tools/APIs
* Logs & errors → Log management platforms

***

### 2. Recreate or Align Existing Dashboard

Focus on building a similar operational dashboard.

### Priority Sections

✅ Service Health (UP/DOWN)

✅ Batch Job Status (SUCCESS/FAILED)

✅ Monitoring & Availability

✅ Logs and Error Counts

✅ Key Business Metrics

* Accounts
* Transactions
* Statements
* Other operational KPIs

***

### 3. Identify Required Data Sources

Potential integrations include:

* AWS CloudWatch Logs & Metrics
* Database queries
* Batch job outputs/schedulers
* Monitoring and health-check tools
* Application APIs
* Logging platforms

***

### 4. Prioritize Delivery

**Key guidance from Josh:**

> "If we can achieve half of this, we are well on our way."

Approach:

* Do not attempt to build everything at once.
* Focus on high-value operational widgets first.
* Deliver a working dashboard quickly.
* Expand functionality incrementally.

***

### 5. Long-Term Goal

* Build a comprehensive operational dashboard.
* Provide end-to-end visibility across systems.
* Create a **single pane of glass** for operations and support teams.
* Continuously improve coverage and monitoring capabilities.

***

# Action Items

### 1. Break Down the Dashboard

Create an inventory of all sections:

* AWS Infrastructure
* Service Health
* Batch Jobs
* Database Jobs
* Monitoring
* Alerts
* Logs
* Business Metrics

### 2. Map Components to Data Sources

For each widget, identify:

* Required data
* Source system
* Collection method
* Refresh frequency

### 3. Build Priority Features First

Start with:

1. Service Status
2. Job Status
3. Alerts & Failures
4. Monitoring Metrics

### 4. Validate with Team

* Review dashboard understanding with stakeholders.
* Confirm alignment with Josh's expectations.
* Identify any gaps or missing requirements.

### 5. Iterate and Enhance

* Deliver an initial version.
* Gather feedback.
* Add additional widgets and metrics over time.
* Move toward full operational visibility.

## Success Criteria

* Centralized operational visibility.
* Real-time service and job monitoring.
* Clear health status indicators.
* Actionable alerts and failures.
* Gradual evolution into a complete operations dashboard.