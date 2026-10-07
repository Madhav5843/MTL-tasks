# EBS Change Request (CR) Creation Guide

A simple guide to create **Staging and Production deployment CRs** in Jira.

---

## 1. Get the Release Notes

Before creating a CR, open the relevant **Release Notes**.

Use the Release Notes as the **source of truth** for:

- Release title
- SF tickets
- IL tickets
- Ticket descriptions
- Related production tickets

---

## 2. Create the CR

Create a new **Change Request** in Jira.

Fill in the following details.

### Basic Details

| Field | What to enter |
|---|---|
| **Title** | Copy the title directly from Release Notes |
| **Change Type** | Standard |
| **Impact** | Minor / Localized |
| **Urgency** | Medium |
| **Change Risk** | Medium |
| **Change Reason** | Upgrade |
| **Test Plan** | As applicable |
| **Planned Start** | Deployment start time |
| **Planned End** | Deployment end time |

### Example

```text
Change Type    : Standard
Impact         : Minor / Localized
Urgency        : Medium
Change Risk    : Medium
Change Reason  : Upgrade
```

---

## 3. Add Release Details

Copy the applicable tables from the Release Notes into the CR.

### If it is an SF release

Add:

```text
SF Ticket
```

Then copy the **SF ticket table** from the Release Notes.

### If it is an IL release

Add:

```text
IL Ticket
```

Then copy the **IL ticket table** from the Release Notes.

### If the release contains both

Add both:

```text
SF Ticket

[SF Release Notes Table]


IL Ticket

[IL Release Notes Table]
```

**Do not manually modify the ticket details. Copy them from the Release Notes.**

---

## 4. Add Implementation Plan

Use **Rovo** to generate the Implementation Plan.

The plan should cover:

1. Pre-deployment checks
2. Deployment steps
3. Validation
4. Post-deployment monitoring

Review the Rovo-generated plan before adding it to the CR.

---

## 5. Add Backout Plan

Use **Rovo** to generate the Backout Plan.

The plan should cover:

1. Conditions requiring rollback
2. Rollback steps
3. Restore previous stable version
4. Application/service validation
5. Post-rollback monitoring

Review the generated plan before adding it to the CR.

---

## 6. Add Approvers

Add the required approvers for the environment.

Example:

```text
Approvers

- Chris Wizard
- Hannah Rabbitt
- Josh Hoban
- Sudip Dasgupta
```

The approvers may differ between **Staging and Production**, so always use the appropriate approvers for the specific deployment.

---

# 7. Deployment Dates & Times

Fill in the change window.

### Planned Start

The expected time when deployment will begin.

### Planned End

The expected time when deployment should finish.

### Actual Start

Update when the deployment actually starts.

### Actual End

Update when the deployment actually finishes.

Example:

```text
Planned Start : 07-Oct-2026 09:00 AM
Planned End   : 07-Oct-2026 11:00 AM

Actual Start  : 07-Oct-2026 09:00 AM
Actual End    : 07-Oct-2026 11:00 AM
```

---

# 8. Final CR Checklist

Before submitting the CR:

- [ ] Correct Release Notes used
- [ ] Title copied from Release Notes
- [ ] Correct environment selected
- [ ] SF table added, if applicable
- [ ] IL table added, if applicable
- [ ] Change Type selected
- [ ] Impact selected
- [ ] Urgency selected
- [ ] Change Risk selected
- [ ] Change Reason selected
- [ ] Test Plan completed, if applicable
- [ ] Planned Start added
- [ ] Planned End added
- [ ] Implementation Plan added using Rovo
- [ ] Backout Plan added using Rovo
- [ ] Required approvers added
- [ ] CR reviewed
- [ ] CR submitted for approval

---

# Staging vs Production

### STAGING

```text
Release Notes
      ↓
Create Staging CR
      ↓
Copy Title + SF/IL Tables
      ↓
Set Change Details
      ↓
Set Deployment Window
      ↓
Rovo → Implementation Plan
      ↓
Rovo → Backout Plan
      ↓
Add Staging Approvers
      ↓
Review & Submit
```

### PRODUCTION

```text
Production Release Notes
      ↓
Create Production CR
      ↓
Copy Title + SF/IL Tables
      ↓
Set Change Details
      ↓
Set Production Change Window
      ↓
Rovo → Implementation Plan
      ↓
Rovo → Backout Plan
      ↓
Add Production Approvers
      ↓
Final Review
      ↓
Submit for Approval
      ↓
Deploy after Approval
```

## Quick Rule

> **Release Notes → Create CR → Copy Title & Tickets → Fill Change Details → Add Deployment Window → Rovo Implementation Plan → Rovo Backout Plan → Add Approvers → Review → Submit.**

This is the cleanest version for a GitHub SOP, because someone new can scan it and immediately understand **what to copy, what to fill, what Rovo is used for, and what needs to be checked before submitting the CR**.
