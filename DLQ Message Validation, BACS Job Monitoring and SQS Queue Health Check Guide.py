# DLQ Message Validation, BACS Job Monitoring and SQS Queue Health Check Guide

## Purpose

This document provides step-by-step instructions to validate stuck DLQ messages, monitor BACS report processing, and verify the health and message count of AWS SQS queues in the EBS Production environment. These checks help L2 Support engineers identify failed transactions, pending messages, and queue backlogs.

***

# 1. Verify Stuck Messages in DLQ

## Objective

Identify messages that have been moved to the Dead Letter Queue (DLQ) but do not have a corresponding transaction record in the audit table.

This helps determine whether transactions are stuck, failed during processing, or require further investigation.

## Query

```sql
SELECT
    d.id,
    d.queue_name,
    d.created_on,
    d.endToEndTransactionId,
    d.pretty_message
FROM (
    SELECT
        id,
        queue_name,
        created_on,
        JSON_UNQUOTE(
            JSON_EXTRACT(
                JSON_UNQUOTE(JSON_EXTRACT(message, '$.text')),
                '$.endToEndTransactionId'
            )
        ) AS endToEndTransactionId,
        JSON_PRETTY(
            JSON_UNQUOTE(JSON_EXTRACT(message, '$.text'))
        ) AS pretty_message
    FROM t_dlq_messages_sink
    WHERE queue_name IN (
        'ebs-prd-dlq-agencybank-savings-outbound-payment-request-queue.fifo',
        'ebs-prd-dlq-manual-savings-outbound-payment-response-queue.fifo',
        'ebs-prd-dlq-agencybank-savings-outbound-payment-response-queue.fifo',
        'ebs-prd-dlq-notification-event-queue'
    )

) d
WHERE d.endToEndTransactionId IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM prdildb.t_clearbank_audit a
      WHERE a.transaction_id = d.endToEndTransactionId
  )
ORDER BY d.created_on DESC
LIMIT 10;
```

***

## What This Query Does

The query:

1. Reads messages from selected DLQ queues.
2. Extracts the `endToEndTransactionId` from the message payload.
3. Checks whether the transaction exists in the `t_clearbank_audit` table.
4. Returns only transactions that do not have a matching audit record.

***

## Expected Output

```text
id
queue_name
created_on
endToEndTransactionId
pretty_message
```

***

## Investigation Outcome

### If Records Are Returned

This indicates:

* Messages are present in DLQ.
* Corresponding transaction records are not available in audit tables.
* Further application-level investigation is required.

### If No Records Are Returned

This indicates:

* No stuck transactions detected.
* Audit records exist for all processed transactions.

***

# 2. Verify BACS Job Processing

## Objective

Check whether BACS report processing is occurring correctly and verify recent job activity.

## Query

```sql
SELECT *
FROM prdildb.t_bacs_report
ORDER BY created_on DESC;
```

***

## Purpose

The query retrieves BACS report records ordered by the latest creation date.

***

## What to Check

### Recent Records

Verify that new records are being created regularly.

### Processing Status

Check whether recently created reports have completed successfully.

### Timestamp Validation

Confirm that report generation timestamps are current and aligned with expected schedules.

***

## Expected Result

```text
Recent BACS reports available
Created timestamps updating regularly
No unusual processing delays
```

***

# 3. Check Available SQS Queues

## Objective

List all available SQS queues in the AWS environment.

### Command

```bash
aws sqs list-queues --region eu-west-2
```

***

## Purpose

This command displays all configured SQS queues within the specified AWS region.

***

## Example Output

```text
ebs-prd-payment-request-queue.fifo
ebs-prd-payment-response-queue.fifo
ebs-prd-dlq-account-creation-event-queue.fifo
ebs-prd-dlq-notification-event-queue
```

***

# 4. Check Message Count for All DLQ Queues

## Objective

Validate whether any DLQ queues contain pending messages.

### Command

```bash
for q in $(aws sqs list-queues --queue-name-prefix ebs-prd-dlq --query 'QueueUrls[*]' --output text); do
  echo "===== $q ====="
  aws sqs get-queue-attributes \
  --queue-url "$q" \
  --attribute-names ApproximateNumberOfMessages \
  --query 'Attributes.ApproximateNumberOfMessages' \
  --output text
done
```

***

## Purpose

The command:

1. Retrieves all DLQ queues.
2. Checks the message count for each queue.
3. Displays the number of visible messages awaiting processing.

***

## Example Output

```text
===== ebs-prd-dlq-notification-event-queue =====
0

===== ebs-prd-dlq-account-creation-event-queue.fifo =====
15
```

***

## Interpretation

### Message Count = 0

```text
Queue is healthy
No pending messages
```

### Message Count > 0

```text
Messages remain in DLQ
Further investigation required
```

***

# 5. Check a Specific SQS Queue

## Objective

Verify the status of a particular queue and determine whether messages are waiting or currently being processed.

### Command

```bash
aws sqs get-queue-attributes \
--queue-url https://sqs.eu-west-2.amazonaws.com/585443427735/ebs-prd-dlq-account-creation-event-queue.fifo \
--attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible
```

***

## Understanding the Output

### ApproximateNumberOfMessages

Represents visible messages currently waiting in the queue.

Example:

```text
ApproximateNumberOfMessages = 25
```

Meaning:

```text
25 messages are pending processing.
```

***

### ApproximateNumberOfMessagesNotVisible

Represents messages currently being processed by consumers.

Example:

```text
ApproximateNumberOfMessagesNotVisible = 5
```

Meaning:

```text
5 messages are actively being processed.
```

***

## Queue Health Assessment

### Healthy Queue

```text
ApproximateNumberOfMessages = 0
ApproximateNumberOfMessagesNotVisible = 0
```

No backlog and no processing issues.

***

### Active Processing

```text
ApproximateNumberOfMessages = 0
ApproximateNumberOfMessagesNotVisible > 0
```

Messages are currently being consumed.

***

### Queue Backlog

```text
ApproximateNumberOfMessages > 0
```

Messages remain pending and require investigation.

***

# Recommended Investigation Flow

### Step 1

Check whether messages are stuck in DLQ using the SQL query.

### Step 2

Verify whether corresponding audit records exist.

### Step 3

Review BACS report activity.

### Step 4

Check all DLQ queues for message backlog.

### Step 5

Identify the affected queue.

### Step 6

Check queue attributes and message counts.

### Step 7

Investigate CloudWatch logs for related errors.

### Step 8

Determine whether the issue is:

* Application Related
* Data Related
* Queue Processing Related
* Infrastructure Related

***

# Key Takeaways

* DLQ tables help identify unprocessed or failed transactions.
* BACS report monitoring confirms batch processing activity.
* SQS queue message counts provide visibility into queue health.
* A high DLQ message count is an indicator of application or data processing issues.
* Always correlate DLQ messages with audit records and CloudWatch logs during investigations.

***

# Conclusion

This procedure provides a standard approach for monitoring DLQ messages, validating BACS processing, and assessing SQS queue health in the EBS Production environment. Following these checks enables faster identification of stuck transactions, failed queue processing, and application-related issues while ensuring effective operational support.
