PUSH Notification Failure

 1. What is this alert?

Alert: `Prod - PUSH Notification failure`
Severity: ERROR
Priority: P2
Application: `ecology-production-aws-cloudwatch`
SNS Platform Application: `mtl-ebs-prd-push-notification-app`

This alert is related to mobile push notification delivery failures.

The push notification flow is:

```text
Mobile Application
       ↓
Firebase FCM
       ↓
FCM Registration Token
       ↓
AWS SNS Platform Application
       ↓
SNS Platform Endpoint
       ↓
Firebase FCM
       ↓
User's Mobile Device
```

AWS SNS is being used as the service that sends push notifications to mobile devices through FCM.

---

# 2. What is an SNS Platform Application?

The SNS Platform Application is:

```text
mtl-ebs-prd-push-notification-app
```

It represents the mobile push-notification application configuration in AWS SNS.

Inside the Platform Application, SNS maintains multiple Platform Endpoints.

Each endpoint represents a particular mobile app/device registration.

Example:

```text
SNS Platform Application
        │
        ├── Endpoint A → Device A
        ├── Endpoint B → Device B
        ├── Endpoint C → Device C
        └── Endpoint D → Device D
```

So, the Platform Application is the overall push-notification setup, while the Platform Endpoint represents an individual device/app registration.

---

# 3. What is the SNS Platform Endpoint?

Example endpoint:

```text
42496bd7-a395-343d-98a8-7584de56d250
```

The endpoint contains information that SNS uses to send a notification to a particular mobile application/device.

The endpoint has a Device Token, for example:

```text
e7fc57f08517df7381ef3412822c52f4a6522a6eac0c828be89e5c15da301c76
```

Important:

```text
Endpoint ID ≠ Device/FCM Token
```

The Endpoint ID is the identifier of the SNS endpoint.

The Device Token is the token used to identify the mobile app/device registration with FCM.

---

# 4. What is the FCM Registration Token?

FCM = Firebase Cloud Messaging.

The mobile application registers with Firebase and receives a registration token.

Example:

```text
FCM Registration Token:
e7fc57f08517df7381ef3412822c52f4a6522a6eac0c828be89e5c15da301c76
```

SNS uses this token when it sends a push notification.

Think of the token as the destination information for the mobile app installation.

If the token is no longer valid, FCM cannot deliver the notification.

---

# 5. What is the actual error?

In Coralogix, we can see:

```text
statusCode: 400
status: FAILURE
```

and:

```text
providerResponse:
"The registration token is not a valid FCM registration token"
```

with:

```text
errorCode:
INVALID_ARGUMENT
```

# Meaning

SNS attempted to send a push notification using the FCM registration token.

FCM rejected the request because the registration token was invalid.

So the problem is not necessarily that the entire push-notification service is down.

It can be an individual/stale/invalid device registration causing notification delivery failures.

---

# 6. Why does the first Jira ticket come?

The alert has:

```text
Threshold: 20
Time Window: 15 mins
```

This means the monitoring system is watching the push-notification failure metric.

When the number of failures crosses the configured threshold within the configured time window, the alert changes to TRIGGERED.

Example:

```text
15-minute window
──────────────────────────────

Failure 1
Failure 2
Failure 3
...
Failure 20
Failure 21
       ↓
Threshold crossed
       ↓
🚨 ALERT TRIGGERED
       ↓
Jira ticket created
```

Therefore, the first ticket means:

> Push notification failures crossed the configured alert threshold.

It does not automatically mean that the entire production application is down.

---

# 7. Why do we get another RESOLVED ticket a few minutes later?

The alert has two states:

```text
TRIGGER
   ↓
Problem condition exists

RESOLVED
   ↓
Problem condition is no longer met
```

Example:

```text
07:14
Failures cross threshold
        ↓
🚨 TRIGGERED ticket

        ↓
Failure count decreases

07:28
Failures fall below threshold
        ↓
✅ RESOLVED ticket
```

Therefore, the two Jira tickets are generally two states of the same alert condition.

# Important

```text
RESOLVED ≠ Root cause fixed
```

A resolved alert only means the monitoring condition is no longer currently true.

The invalid SNS endpoint/token could still exist.

---

# 8. Why can the alert resolve by itself?

Suppose the alert threshold is:

```text
20 failures / 15 minutes
```

If there are 25 failures:

```text
25 failures
   ↓
Threshold exceeded
   ↓
ALERT TRIGGERED
```

Later, if there are only 5 failures in the monitoring window:

```text
5 failures
   ↓
Below threshold
   ↓
ALERT RESOLVED
```

So the alert can resolve because:

* failure traffic decreased
* the affected endpoint was no longer being used
* the number of failures dropped below the threshold
* the monitoring window moved forward

It does not necessarily mean somebody fixed the underlying device/token.

---

# 9. Why do we disable the SNS Endpoint?

If the endpoint contains an invalid/stale FCM token, continuing to send notifications to it will keep generating delivery failures.

So we identify the affected SNS endpoint and disable it.

Example:

```text
Invalid FCM Token
       ↓
SNS Endpoint
       ↓
Disable Endpoint
       ↓
SNS stops attempting delivery
       ↓
Avoid repeated failures
```

In the AWS SNS console, the endpoint can show:

```text
Status: Disabled
```

# Purpose of disabling

We are effectively telling SNS:

> "This endpoint is currently not a valid destination for push notifications. Don't keep trying to deliver notifications to it."

---

# 10. Does disabling the endpoint fix the FCM token?

No.

This is very important.

Disabling the endpoint prevents further delivery attempts, but it does not make the old FCM token valid again.

The proper long-term flow is:

```text
Invalid/Old FCM Token
        ↓
Mobile application gets a new token
        ↓
Backend receives the new token
        ↓
SNS endpoint is updated with new token
        ↓
Endpoint is enabled
        ↓
Push notifications work again
```

So:

```text
Disable endpoint
       ↓
Mitigation / cleanup

Update with valid token
       ↓
Actual recovery for that device
```

---

# 11. Why can an FCM token become invalid?

Common reasons include:

# App was uninstalled

```text
App installed
    ↓
Token generated
    ↓
SNS stores token
    ↓
User uninstalls app
    ↓
Old token becomes unusable
```

# App was reinstalled

```text
Old installation
    ↓
Old token

App uninstalled/reinstalled
    ↓
New installation
    ↓
New token
```

SNS may still have the old token if the application does not update it correctly.

# FCM token was refreshed

FCM registration tokens can change.

The backend/SNS configuration needs to stay synchronized with the latest token.

# Device/app registration became stale

An old registration may no longer be recognized by FCM.

# Incorrect token/environment

A token belonging to a different Firebase application/project or incorrect configuration can also result in push-delivery failures.

---

# 12. What happens from application to Jira?

The complete flow is:

```text
             MOBILE APP
                 │
                 │ FCM registration
                 ▼
          FCM Registration Token
                 │
                 ▼
       AWS SNS Platform Application
                 │
                 ▼
          SNS Platform Endpoint
                 │
                 │ Send notification
                 ▼
                FCM
                 │
                 X
        Invalid registration token
                 │
                 ▼
            HTTP 400
         INVALID_ARGUMENT
                 │
                 ▼
       SNS Delivery Failure
                 │
                 ▼
       CloudWatch / Application Logs
                 │
                 ▼
             Coralogix
                 │
                 │ Failure count crosses threshold
                 ▼
          🚨 ALERT TRIGGER
                 │
                 ▼
             Jira Ticket
```

Then:

```text
Failure count decreases
        ↓
Alert condition no longer met
        ↓
✅ ALERT RESOLVED
        ↓
Resolved Jira ticket
```

---

# 13. What should I check when this ticket comes?

Use this as the troubleshooting checklist.

# Step 1: Open the Jira ticket

Check:

```text
Alert name
Severity
Priority
Triggered time
Application
Subsystem
Threshold
Time Window
```

---

# Step 2: Check Coralogix

Look for the actual push-notification failure.

Search around the alert timestamp.

Look for:

```text
status: FAILURE
statusCode: 400
providerResponse
INVALID_ARGUMENT
registration token
FCM
```

---

# Step 3: Identify the affected SNS endpoint

From the logs, identify the SNS endpoint ARN.

Example:

```text
arn:aws:sns:eu-west-2:...:endpoint/GCM/
mtl-ebs-prd-push-notification-app/
42496bd7-a395-343d-98a8-7584de56d250
```

---

# Step 4: Open the endpoint in AWS SNS

Check:

```text
Endpoint ID
Device Token
Status
Platform Application
```

Example:

```text
Endpoint:
42496bd7-a395-343d-98a8-7584de56d250

Device Token:
e7fc57f...

Status:
Disabled
```

---

# Step 5: Determine the failure

If the logs clearly show:

```text
The registration token is not a valid FCM registration token
```

then this is an FCM token / device registration issue.

Do not immediately conclude:

```text
Production service is down
```

---

# Step 6: Follow the team's remediation process

If the endpoint is confirmed to be invalid/stale, disable the endpoint according to the team's established procedure.

---

# Step 7: Update Jira

Mention:

* push notification delivery failures were observed
* FCM returned an invalid registration token error
* affected SNS endpoint was identified
* endpoint was disabled if that was the action taken
* no broader service outage was identified, if confirmed

---

# 14. Example Jira comment

For this type of incident:

> Investigated the Prod PUSH Notification failure alert. The failures were caused by an invalid FCM registration token associated with an SNS platform endpoint. The affected SNS endpoint was identified and disabled to prevent further delivery attempts to the invalid destination. No broader service outage was identified. The alert subsequently returned to a resolved state.

---

# 15. Quick memory version 🧠

If I forget everything else, remember this:

```text
PUSH FAILURE
     ↓
SNS tries to send notification
     ↓
FCM rejects the device token
     ↓
SNS records delivery FAILURE
     ↓
Failures cross 20 within 15 mins
     ↓
🚨 Jira TRIGGER ticket
     ↓
Failures drop below threshold
     ↓
✅ Jira RESOLVED ticket
     ↓
Check affected SNS endpoint
     ↓
Disable invalid/stale endpoint
     ↓
Proper long-term fix = update with new valid FCM token
```

# One-line memory trick:

> Invalid FCM token → SNS delivery failure → threshold crossed → Trigger ticket → failures drop → Resolved ticket → identify/disable stale SNS endpoint → update token for permanent recovery.

---

 ⚠️ One thing to remember about your specific screenshots

Your Coralogix log says `INVALID_ARGUMENT` + "The registration token is not a valid FCM registration token." That's strong evidence of a token problem.

But don't assume that SNS automatically disabled the endpoint because of that exact error. The endpoint in your screenshot being `Disabled` could be the result of your team's manual action or another endpoint-management event. Always check the actual endpoint history/logs if you need to establish exactly who or what disabled it.

That distinction will save you from writing a technically incorrect RCA later.
