# Service Deployment and Version Upgrade Guide (EBS Production)

## Purpose

This document provides the step-by-step process for upgrading application versions in the EBS Production environment. The process includes updating the service version in GitHub, triggering the Jenkins deployment pipeline, validating Kubernetes pods, and confirming that the new image version has been successfully deployed.

***

# 1. Update Version in GitHub

## Objective

Update the application version that needs to be deployed to the Production environment.

### Navigate to Repository

For application deployments:

```text
mtl-config → ebs → prd
```

Repository:

```text
mtl-config/ebs/prd
```

### Open the Configuration File

```text
versions.yaml
```

### Update the Required Service Version

Example:

```yaml
mtl-savings-payment-service:
  version: 1.2.10
```

Update to:

```yaml
mtl-savings-payment-service:
  version: 1.2.11
```

### Save and Commit Changes

After updating the version:

1. Commit the changes.
2. Push the changes to the repository.

***

## Verify GitHub Changes

After committing:

1. Navigate to the **History** or **Commits** section.
2. Verify the latest commit is visible.
3. Confirm the correct version has been updated.
4. Ensure the commit has been pushed successfully.

### Validation

✅ Version updated in `versions.yaml`

✅ Commit successfully pushed

✅ Changes visible in GitHub history

***

# 2. Database Release Deployment (If Applicable)

## Objective

Verify the database release script that will be included in the deployment.

### Navigate to Repository

```text
mtl-il-db → ebs → prd
```

Repository:

```text
mtl-il-database
```

Example Release Script:

```text
EBS-PRD/Sprint2025-49-R26_01.sql
```

### Validation

Verify:

* Correct SQL file is present.
* Release script matches deployment requirements.
* Script is available in the target release branch.

***

# 3. Trigger Jenkins Deployment Pipeline

## Objective

Deploy the updated application version to the Production environment.

### Open Jenkins

Navigate to:

```text
cd-pipeline [ebs-prd-pipelines]
```

### Trigger Deployment

1. Select:

```text
Build with Parameters
```

2. Enter any required deployment parameters.
3. Click:

```text
Build
```

***

## Monitor Pipeline Execution

Verify each stage completes successfully.

Typical stages include:

* Checkout
* Build Validation
* Deployment
* Kubernetes Rollout
* Verification

### Validation

✅ Pipeline completed successfully

✅ No failed stages

✅ Deployment executed successfully

***

# 4. Connect to Production Bastion Server

## Objective

Access the Production Kubernetes environment for deployment verification.

### Navigate to AWS Console

```text
AWS Console → EC2
```

### Connect to Server

```text
ebs-prd-bastion
```

***

## Configure Kubernetes Access

If required:

```bash
sudo su ec2-user
aws eks update-kubeconfig --region eu-west-2 --name ebs-prd-cluster
```

***

# 5. Verify Existing Pods Before Deployment

## Objective

Capture the running pod details before deployment.

### Savings Payment Service Example

```bash
kubectl get pods -n ebs-prd | grep -i savings
```

### Sample Output

```text
mtl-savings-payment-service-deployment-b7f4f797-jmngq
```

### Purpose

Record:

* Pod Names
* Running Status
* Replica Count

This information helps confirm whether new pods are created after deployment.

***

# 6. Verify Pods After Deployment

## Objective

Confirm that Kubernetes has created new pods with the updated version.

### Command

```bash
kubectl get pods -n ebs-prd | grep -i savings
```

### What to Verify

* Old pods are terminated.
* New pods are created.
* Pods are in Running state.
* No CrashLoopBackOff errors.

### Expected Result

```text
STATUS = Running
READY = 1/1
```

***

# 7. Verify the Deployed Image Version

## Objective

Confirm that the application is running the updated container image.

### Command

```bash
kubectl describe pod mtl-savings-payment-service-deployment-b7f4f797-jmngq -n ebs-prd | grep Image
```

### Example Output

```text
Image:
585443427735.dkr.ecr.eu-west-2.amazonaws.com/mtl-savings-payment-service:1.2.11
```

***

## Validation

Verify that the deployed image tag matches the version updated in:

```text
versions.yaml
```

### Example

Updated Version:

```yaml
version: 1.2.11
```

Pod Image:

```text
mtl-savings-payment-service:1.2.11
```

✅ Version matches

✅ Deployment successful

***

# 8. Mortgage Payment Service Verification

## Objective

Validate deployment for Mortgage Payment Service.

### Check Running Pods

```bash
kubectl get pods -n ebs-prd | grep mortgage-payment-service
```

### Example Output

```text
mtl-mortgage-payment-service-deployment-7f69d87867-v9n2q
```

***

### Verify Image Version

```bash
kubectl describe pod mtl-mortgage-payment-service-deployment-7f69d87867-v9n2q -n ebs-prd | grep Image
```

### Expected Output

```text
Image:
585443427735.dkr.ecr.eu-west-2.amazonaws.com/mtl-mortgage-payment-service:2.3.8
```

***

## Validation Checklist

### GitHub

✅ Version updated in `versions.yaml`

✅ Changes committed and pushed

✅ Commit visible in repository history

***

### Jenkins

✅ Pipeline triggered successfully

✅ Pipeline completed successfully

✅ No deployment failures

***

### Kubernetes

✅ New pods created

✅ Pods in Running state

✅ No pod restart issues

***

### Image Verification

✅ Correct image version deployed

✅ Image tag matches `versions.yaml`

✅ Old version no longer running

***

# Deployment Verification Flow

```text
1. Update version in GitHub
        ↓
2. Commit and Push Changes
        ↓
3. Verify Commit History
        ↓
4. Trigger Jenkins Pipeline
        ↓
5. Monitor Pipeline Completion
        ↓
6. Connect to Bastion Host
        ↓
7. Verify Pods Before Deployment
        ↓
8. Verify Pods After Deployment
        ↓
9. Validate Container Image Version
        ↓
10. Confirm Successful Deployment
```

***

# Conclusion

This procedure provides a standardized deployment process for upgrading application versions in the EBS Production environment. By validating GitHub changes, monitoring Jenkins pipelines, verifying Kubernetes pods, and confirming container image versions, support engineers can ensure that deployments are completed successfully and that the correct application version is running in production.
