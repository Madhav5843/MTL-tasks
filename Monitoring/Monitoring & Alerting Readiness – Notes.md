# Monitoring & Alerting Readiness – Notes

## Question 1: CloudWatch Alarms

* Currently **226 CloudWatch alarms** are configured across the AWS environment.
* Alarms cover:
  * Lambda errors
  * DLQs (Dead Letter Queues)
  * Service health checks
  * Infrastructure monitoring
* Most alarms are in **OK** state.
* A few alarms are in **Insufficient Data** state and are under review.
* These alarms are either newly configured or rely on metrics that are not continuously generated.
* Standardization and validation are in progress.

***

## Question 2: Alerts Received vs Attended

* CloudWatch alarm history is used to track alarm state transitions.
* Review of sampled alarms showed **no recent ALARM state transitions**, indicating no major threshold breaches during the reviewed period.
* Current tracking is done at the individual alarm level.
* No centralized dashboard currently exists for:
  * Total alerts received
  * Total alerts acknowledged
  * Total alerts resolved
* Improvement planned:
  * Centralized alert tracking
  * SNS integration
  * JIRA integration
  * Alert reporting and aggregation

**Summary:**

* Alerts are configured and monitored.
* No significant recent threshold breaches observed.
* Centralized reporting is being enhanced.

***

## Question 3: Alert & Downtime Tracking Mechanism

### Current Process

* AWS CloudWatch monitors services and infrastructure.
* CloudWatch alarms trigger notifications when thresholds are breached.
* Notifications are sent to SNS topic:
  * `Jira_Service_Management`
* SNS triggers:
  * Lambda function (`jira-alert-forwarder`)
  * HTTPS endpoint
* JIRA incidents are automatically created and tracked.

### Downtime Tracking

* Based on:
  * CloudWatch alarm state transitions
  * Automatically generated JIRA incidents
  * Incident resolution records

**Result:**

* End-to-end tracking exists from alarm generation to incident resolution.

***

## Question 4: CloudWatch to JIRA Integration

### Status

✅ Implemented

### Flow

```text
CloudWatch Alarm
       ↓
      SNS
       ↓
 Lambda (jira-alert-forwarder)
       ↓
 JIRA Service Management
```

### Features

* Automated incident creation
* Automated alert forwarding
* Dual integration:
  * Lambda
  * HTTPS endpoint

***

## Question 5: Automatic JIRA Ticket Creation

### Status

✅ Enabled

### Process

* CloudWatch alarm enters ALARM state.
* SNS receives notification.
* Lambda forwards details to JIRA.
* JIRA ticket created automatically.

### Coverage

* Enabled for all services where CloudWatch alarms are configured.
* Ongoing effort to ensure complete coverage across critical systems.

***

## Question 6: Application Service Monitoring

### Monitoring Tools

#### CloudWatch Metrics

* Lambda Errors
* Lambda Duration
* CPU Utilization
* DLQ Metrics
* Service Health Metrics

#### CloudWatch Logs

* Application logs
* Troubleshooting
* Error analysis

#### CloudWatch Alarms

* Threshold breach detection
* Automatic notification generation

#### Alert Management

* SNS notifications
* JIRA incident creation

#### EKS Monitoring

* Pod-level monitoring
* Node-level monitoring
* Resource utilization monitoring

### Summary

* Real-time application and infrastructure monitoring is established.
* Alerting and incident management are automated.

***

## Question 7: Service & Pod Health Monitoring

### Dashboard Coverage

CloudWatch dashboards provide visibility into:

* EKS
* RDS
* Service Health
* Infrastructure metrics

### Kubernetes Monitoring

#### Commands Used

**Check all pods**

```bash
kubectl get pods -A
```

**View pod details**

```bash
kubectl describe pod <pod-name>
```

**View logs**

```bash
kubectl logs <pod-name>
```

**Check pod failures/restarts**

```bash
kubectl get pods -A | grep -i crash
```

### Health Indicators

* Running → Healthy
* CrashLoopBackOff → Issue detected
* Error → Issue detected

### Additional Monitoring

* CloudWatch Container Insights
* Infrastructure alarms

### How Downtime is Detected

* Pod failures
* Pod restart patterns
* Error logs
* CloudWatch alarms

***

## Question 8: Monitoring Improvements Implemented

### Monitoring Coverage

* 226 CloudWatch alarms
* Application monitoring
* Infrastructure monitoring
* EKS monitoring
* DLQ monitoring
* Kubernetes visibility

### Major Improvements

* CloudWatch Alarms deployed
* SNS → Lambda → JIRA integration
* CloudWatch Dashboards implemented
* Application log monitoring enabled
* Kubernetes monitoring established
* DLQ monitoring implemented

***

## Question 9: Improvements Completed

### Key Deliverables

* \~226 CloudWatch alarms configured
* Automated incident creation via JIRA
* Real-time CloudWatch dashboards
* Lambda and application monitoring
* Kubernetes service visibility
* DLQ alerting and monitoring

***

## Question 10: DevOps Readiness (Staging & Production)

### Status

✅ Ready

### Capabilities

* AWS access and permissions available
* Monitoring dashboards operational
* CloudWatch logs and alarms configured
* SNS and JIRA alert automation enabled
* Kubernetes troubleshooting capability
* Production and staging support coverage available

***

## Question 12: Vanta Board Status

### Current Status

* Most compliance-related tasks are implemented.
* Remaining tasks are:
  * Under review
  * In progress
* Coordination ongoing with:
  * Shivam
  * Sonu

***

## Question 13: Vanta Tickets Resolved

### Last 30 Days

* **4 Vanta tasks completed**

***

## Question 14: Late-Night Monitoring Coverage

### Monitoring Availability

✅ Monitoring is active 24/7

### Alert Flow

```text
CloudWatch Alarm
       ↓
      SNS
       ↓
 JIRA Ticket Creation
       ↓
 Mobile Call Notification
       ↓
 On-call Engineer Response
```

### Support Model

* On-call support process established.
* Designated engineers respond after business hours.
* Response based on incident severity and impact.

### Summary

* Monitoring continues outside standard business hours.
* Automated alerts, JIRA tickets, and mobile notifications ensure continuous incident visibility and response.
