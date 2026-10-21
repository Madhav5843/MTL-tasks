# Google Professional Cloud Architect (PCA)
## Day 1 Study Notes: Google Cloud Fundamentals, IAM, Compute & Networking

> **Purpose:** Quick-reference notes for revision and recall. These notes are based on the Day 1 training transcript. Topics marked as “introduced” were not covered in depth during this session.

---

## Table of Contents

1. [Training Overview](#1-training-overview)
2. [Cloud Computing Fundamentals](#2-cloud-computing-fundamentals)
3. [Cloud Service Models](#3-cloud-service-models)
4. [Regions, Zones, and Global Infrastructure](#4-regions-zones-and-global-infrastructure)
5. [Open Source and Vendor Lock-in](#5-open-source-and-vendor-lock-in)
6. [Pricing, Quotas, and Budgets](#6-pricing-quotas-and-budgets)
7. [Resource Hierarchy](#7-resource-hierarchy)
8. [Project Name, ID, and Number](#8-project-name-id-and-number)
9. [IAM and Roles](#9-iam-and-roles)
10. [Service Accounts and Cloud Identity](#10-service-accounts-and-cloud-identity)
11. [Ways to Access Google Cloud](#11-ways-to-access-google-cloud)
12. [Google Cloud Marketplace](#12-google-cloud-marketplace)
13. [VPC and Subnets](#13-vpc-and-subnets)
14. [Compute Engine and Compute Choices](#14-compute-engine-and-compute-choices)
15. [Machine Types and Scaling](#15-machine-types-and-scaling)
16. [Spot VMs and VM Costs](#16-spot-vms-and-vm-costs)
17. [Routes and Firewall Rules](#17-routes-and-firewall-rules)
18. [VPC Peering and Shared VPC](#18-vpc-peering-and-shared-vpc)
19. [Load Balancing, DNS, and CDN](#19-load-balancing-dns-and-cdn)
20. [Hybrid and Private Connectivity](#20-hybrid-and-private-connectivity)
21. [Day 1 Exam Cheat Sheet](#21-day-1-exam-cheat-sheet)
22. [Practice Questions](#22-practice-questions)
23. [Topics to Revisit Later](#23-topics-to-revisit-later)

---

## 1. Training Overview

The training was described as an **8-day program** for Google Professional Cloud Architect certification preparation.

Planned areas:
- Google Cloud fundamentals
- Architecting with Compute Engine
- Terraform
- Google Kubernetes Engine (GKE)
- Observability
- Exam preparation

The trainer mentioned **19 labs**. The advice was to focus on understanding the theory and demonstrations during class, then use the supplied step-by-step guidance to complete labs separately.

### Exam format discussed in the session
- Around 2 hours
- Roughly 50–60 questions
- Scenario- and case-study-oriented
- A dedicated exam-preparation discussion was planned toward the end of training

---

## 2. Cloud Computing Fundamentals

Cloud computing means using a cloud provider's computing infrastructure instead of owning and maintaining all physical hardware yourself.

### Key characteristics

| Characteristic | Meaning | Example |
|---|---|---|
| On-demand self-service | Provision resources when needed without waiting for the provider to create them manually. | A developer creates VMs at 2 AM through the console. |
| Broad network access | Services can be accessed over networks from different locations. | Accessing cloud resources through a browser or API. |
| Resource pooling | Provider infrastructure is pooled to serve customers. | Shared underlying provider infrastructure. |
| Rapid elasticity | Capacity can grow or shrink with demand. | Increase servers during a traffic spike, then reduce them afterward. |
| Measured service / pay-as-you-go | Usage is measured and billed according to the applicable pricing model. | Paying for cloud resources based on consumption or provisioning. |

**Exam cue:** If a scenario says resources are created whenever required without provider intervention, think **on-demand self-service**. If capacity automatically or quickly expands and contracts with demand, think **rapid elasticity**.

---

## 3. Cloud Service Models

### IaaS: Infrastructure as a Service
The provider manages the physical infrastructure, such as physical servers, networking, virtualization, and underlying storage infrastructure. The customer manages more of the layers above the infrastructure.

- Example discussed: Compute Engine VM
- Memory trick: **IaaS = Rent infrastructure**

### PaaS: Platform as a Service
The provider manages more of the underlying platform, allowing the user to focus more on building and running the application.

- Memory trick: **PaaS = Build and run applications on a managed platform**

### SaaS: Software as a Service
A complete application is delivered as a service. Users generally do not manage the application's underlying servers or patches.

- Examples discussed: Gmail and Google Docs
- Memory trick: **SaaS = Use the software**

**Example question:** A team uses Gmail and Google Docs without managing servers or patches. Which service model is this?

**Answer:** SaaS.

---

## 4. Regions, Zones, and Global Infrastructure

The hierarchy introduced in the session:

```text
Global infrastructure
└── Regions
    └── Zones
```

- **Region:** A geographical area.
- **Zone:** A deployment area within a region.
- Deploying across multiple zones can help protect workloads against a single-zone outage.
- Deploying across multiple regions can help serve users in different geographical areas, reduce latency, and improve resilience against a regional failure. Replication depends on the service and architecture.

### Multi-zone example

```text
Region
├── Zone A → Application instance
└── Zone B → Application instance
```

If one zone becomes unavailable, an application deployed across other zones may continue operating.

### Multi-region concept

```text
APAC users → APAC region
Europe users → Europe region
```

The trainer also discussed Google's private/premium network backbone as a way to provide connectivity between locations, highlighting throughput and latency benefits.

---

## 5. Open Source and Vendor Lock-in

The session presented open-source technologies as one approach that can help reduce vendor lock-in.

Examples mentioned:
- **Kubernetes:** GKE is based on Kubernetes. Kubernetes' broad ecosystem can make containerized applications more portable between environments.
- **TensorFlow:** Google's open-source machine-learning framework.
- **Gemma:** Google's open model family.
- **ADK:** Google's agent development framework was also mentioned.

**Exam cue:** When a question asks which approach may help avoid vendor lock-in, consider open and widely supported technologies such as Kubernetes.

---

## 6. Pricing, Quotas, and Budgets

### Pricing concepts

- **Pay-as-you-go:** Pay according to the applicable resource usage and pricing model.
- **Sustained use discounts:** Discount concept discussed for resources running for a significant portion of a billing period.
- **Committed Use Discounts (CUD):** Can suit workloads with predictable, longer-term resource needs.

**Example discussed:** A database is expected to run 24×7 for the next three years. The session's answer was **Committed Use Discount**.

### Cloud Pricing Calculator

The trainer demonstrated estimating cloud costs using inputs such as:
- Number of VM instances
- Operating system
- Machine configuration
- CPU and memory
- Boot disk size
- Provisioning choices

Use the calculator to estimate the cost of a proposed architecture.

### Quota vs. budget

| Concept | Purpose | Example |
|---|---|---|
| Quota | Limits resource or API consumption. | A project can make only a specified number of API calls per minute. |
| Budget | Helps monitor spending and configure notifications. | Receive a notification when spending reaches a configured threshold. |

**Memory trick:**
- **Quota = usage limit**
- **Budget = spending awareness**

---

## 7. Resource Hierarchy

A key Google Cloud concept:

```text
Organization
└── Folder (optional)
    └── Project
        └── Resources
```

- **Organization:** Top-level organizational node.
- **Folder:** Groups projects and may contain subfolders. Folders are optional.
- **Project:** Organizes and manages workloads and resources. Project-level concepts include billing, quotas, APIs/services, and resources.
- **Resources:** Examples include Compute Engine instances, storage resources, and Kubernetes resources.

A folder is not mandatory. An organization can contain projects directly.

### Policy inheritance

Policies can flow down the hierarchy:

```text
Organization
    ↓
  Folder
    ↓
  Project
    ↓
 Resources
```

This hierarchy is important when designing enterprise environments.

---

## 8. Project Name, ID, and Number

| Value | Meaning | Changeability described in the session |
|---|---|---|
| Project name | Human-friendly display name | Can be changed |
| Project ID | Identifier associated with the project | Treated as unchangeable once established |
| Project number | Unique numeric identifier generated for the project | Cannot be changed |

**Exam cue:** If asked which of these can be changed after project creation, the session's answer was **project name**.

---

## 9. IAM and Roles

### What is IAM?

IAM answers:

> **Who can do what on which resource?**

```text
WHO?       → Identity / principal
DO WHAT?   → Permissions / role
ON WHAT?   → Resource
```

Identities mentioned:
- Users
- Groups
- Service accounts
- Cloud Identity identities

### IAM role categories

| Role type | Description |
|---|---|
| Basic roles | Broad permissions, such as Viewer, Editor, and Owner. Less granular. |
| Predefined roles | Google-maintained roles for specific services or use cases. |
| Custom roles | Roles created for more precise permission requirements when existing roles grant more access than needed. |

The session's memory sequence was:

```text
Basic → Predefined → Custom
Broad              → More fine-grained
```

### Viewer, Editor, and Owner

- **Viewer:** Primarily allows viewing resources rather than changing them.
- **Editor:** Can modify many resources but does not provide the same access-management capabilities as Owner.
- **Owner:** Broad control, including access-management capabilities.
- **Billing Administrator:** Discussed as a role for billing-related administration.

**Scenario discussed:** Finance needs to manage project billing but should not change project resources.

**Answer discussed:** Billing Administrator.

### IAM Deny

The training emphasized:

> **Deny overrides Allow.**

Example:
- A user has Editor permissions.
- A deny policy explicitly blocks deleting a VM.
- The deletion is blocked.

---

## 10. Service Accounts and Cloud Identity

### Service accounts

A service account is an identity primarily intended for workloads and applications rather than a human user.

Example:

```text
Service A
   ↓
Service account identity
   ↓
Service B
```

This enables application-to-application access without relying on a person manually entering a username and password.

Service accounts were discussed in relation to:
- APIs
- Applications and services
- Tokens and credentials
- Controlled resource access

**Memory trick:**
- User account → Human
- Service account → Workload/application

### Cloud Identity and directory integration

- **Cloud Identity:** Introduced for centralized identity management.
- **GCDS (Google Cloud Directory Sync):** Discussed as a way to synchronize users from directory systems such as Active Directory or LDAP into the Google identity environment.

---

## 11. Ways to Access Google Cloud

| Access method | Description / use |
|---|---|
| Google Cloud Console | Browser-based GUI for exploring services, creating resources, and administration. |
| Cloud Shell | Browser-accessible command-line environment. |
| Cloud SDK / `gcloud` | Command-line tooling for Google Cloud. |
| APIs and client libraries | Allow scripts and applications to interact with Google Cloud programmatically. Python was mentioned as an example. |
| Mobile application | Another way to access certain Google Cloud information and actions. |

Tools mentioned as available in Cloud Shell included `gcloud`, Docker, Terraform, and BigQuery tooling.

---

## 12. Google Cloud Marketplace

Google Cloud Marketplace provides packaged solutions that can be deployed more quickly than manually installing every component.

The trainer demonstrated a LAMP stack:

- **L:** Linux
- **A:** Apache
- **M:** MySQL
- **P:** PHP

The demo provisioned supporting resources, including compute and related configuration.

**Memory trick:** Marketplace = deploy preconfigured solutions more quickly.

---

## 13. VPC and Subnets

### What is a VPC?

A **Virtual Private Cloud (VPC)** provides logical networking and isolation for cloud resources. The session also connected VPC networking with software-defined networking (SDN).

### Important scope distinction

The key point emphasized during the session:

```text
VPC     = GLOBAL
Subnet  = REGIONAL
VM      = ZONAL
```

- A VPC network is global.
- A subnet is regional.
- A VM instance is zonal.

### Regional subnets

A regional subnet can be used by VMs in different zones within that region.

```text
Global VPC
└── Regional subnet
    ├── VM in Zone A
    ├── VM in Zone B
    └── VM in Zone C
```

**Exam cue:** VMs in different zones can share one subnet because the subnet is **regional**, not zonal.

### Multiple VPCs

The trainer confirmed that one project can contain multiple VPC networks.

```text
Project
├── VPC-A
├── VPC-B
└── VPC-C
```

### Subnet IP exhaustion

The Q&A discussed two possible approaches when a subnet runs out of available IP addresses:
1. Expand/edit the subnet IP range when possible.
2. Create another subnet and place new resources there if needed.

---

## 14. Compute Engine and Compute Choices

### Compute Engine

Compute Engine provides virtual machines. A VM can include:
- vCPU
- Memory
- Operating system
- Disks/storage
- Network interfaces

VMs can be created using:
- Google Cloud Console
- `gcloud`
- API

The demonstration covered VM name, region/zone, machine type, OS image, boot disk, networking, external IP, and creation. Linux VM access was demonstrated through SSH. A Windows Server VM was also created, with RDP access attempted; the demo experienced connection/loading delays.

### Choosing a compute option

| Requirement | Option introduced in the session |
|---|---|
| VM-based workload | Compute Engine |
| Kubernetes/container orchestration | Google Kubernetes Engine (GKE) |
| Serverless application/container | Cloud Run |
| Event-driven function | Cloud Run functions |

The session mentioned both stateful and stateless applications in the GKE discussion and introduced Cloud Run as an option for stateless applications.

---

## 15. Machine Types and Scaling

### Machine-type categories

| Category | Typical workload fit described |
|---|---|
| General purpose | Balanced CPU and memory for common workloads |
| Compute optimized | CPU-intensive workloads |
| Memory optimized | Memory-intensive workloads |
| Accelerator optimized | Workloads needing accelerators such as GPUs |

Machine families mentioned included E2, N-series, C-series, and H-series. The trainer recommended checking Google's machine-type documentation rather than relying only on family names.

### Vertical vs. horizontal scaling

**Vertical scaling = scale up/down**

Change the capacity of an existing machine.

```text
4 vCPU / 16 GB RAM
        ↓
8 vCPU / 32 GB RAM
```

**Horizontal scaling = scale out/in**

Change the number of instances.

```text
Before: VM1, VM2
After:  VM1, VM2, VM3, VM4
```

**Memory trick:**
- Scale **UP** = bigger machine
- Scale **OUT** = more machines

---

## 16. Spot VMs and VM Costs

### Spot VMs

Spot VMs use excess compute capacity at a lower cost, but the provider can reclaim the capacity. They are therefore not a good fit for workloads that cannot tolerate interruption.

Suitable example discussed:
- A batch job that can be stopped and restarted.

**Exam cue:** A night-time batch job can be interrupted and restarted without losing progress. The session's answer was **Spot VM**.

### VM shutdown and storage costs

Stopping a VM stops its compute workload, but attached/provisioned disks can remain and continue to incur storage charges.

```text
VM stopped
   ↓
Compute no longer running

Disk still exists
   ↓
Storage cost may continue
```

---

## 17. Routes and Firewall Rules

### Routes

Routes determine where network traffic is forwarded. This concept was introduced during the discussion of communication across network locations and subnets.

### Firewall rules

Firewall rules control traffic. The demonstration included targeting firewall behavior using instance/network tags.

Example concept:

```text
Web VM 1 → tag: web
Web VM 2 → tag: web
DB VM    → different tag

Firewall rule targets "web"
   ↓
Web VMs are targeted
```

The trainer warned that loosely controlled tags can be risky in enterprise environments because users sharing a project may apply tags incorrectly. Service-account-based approaches were mentioned as a topic for further coverage.

---

## 18. VPC Peering and Shared VPC

### VPC Network Peering

Separate VPCs are isolated by default. VPC Network Peering can establish connectivity between VPC networks.

```text
VPC-A ←──── peering ────→ VPC-B
```

**Important: Peering is not transitive.**

If:
```text
A ↔ B
B ↔ C
```

It does **not** automatically mean:
```text
A ↔ C
```

Connections need to be established appropriately for the required communication.

### Shared VPC

Shared VPC was introduced as a way to share a network across multiple projects.

```text
Shared VPC
├── Project A
├── Project B
└── Project C
```

The detailed implementation was not covered during Day 1.

---

## 19. Load Balancing, DNS, and CDN

### Load balancing

Load balancers distribute traffic across multiple backends. Benefits discussed included availability, traffic distribution, and potentially reduced latency depending on the architecture.

| Type | Layer | Main idea introduced |
|---|---|---|
| Application Load Balancer | Layer 7 | Application/web traffic and proxy behavior; SSL/TLS termination was mentioned. |
| Network Load Balancer | Layer 4 | Network-level traffic forwarding. |

**Memory trick:**
- **L7 → Application Load Balancer**
- **L4 → Network Load Balancer**

### Cloud DNS

Cloud DNS was introduced as a service for mapping names to IP addresses. Google's public DNS address **8.8.8.8** was also mentioned during the discussion.

### Cloud CDN

CDN means **Content Delivery Network**.

The core concept is to cache content closer to consumers so the origin does not have to serve every request directly.

Benefits discussed:
- Lower latency
- Reduced load on the origin
- Potential cost efficiency

```text
User
  ↓
CDN cache
  ↓ (when needed)
Origin
```

These topics were introduced at a high level; detailed implementation was left for later.

---

## 20. Hybrid and Private Connectivity

Several connectivity options were introduced:

- **Cloud VPN:** Provides an encrypted tunnel between environments, such as on-premises infrastructure and Google Cloud.
- **Partner Interconnect:** Connectivity through supported partners/providers.
- **Dedicated Interconnect:** Dedicated connectivity into Google's network for higher-capacity or private-connectivity requirements.
- **Peering:** Network peering concepts were also mentioned.

The session kept this section high-level, with more detailed discussion expected later.

---

## 21. Day 1 Exam Cheat Sheet

Review this section before moving to the next training day.

### Resource hierarchy

```text
Organization
└── Folder (optional)
    └── Project
        └── Resources
```

### IAM

```text
WHO → CAN DO WHAT → ON WHICH RESOURCE
```

- Basic roles: broad permissions
- Predefined roles: service/use-case-specific roles maintained by Google
- Custom roles: more tailored permissions
- Deny overrides Allow

### Networking scope

```text
VPC     → GLOBAL
Subnet  → REGIONAL
VM      → ZONAL
```

### Scaling

- Vertical scaling → bigger or smaller machine
- Horizontal scaling → more or fewer machines

### Load balancing

- Layer 7 → Application Load Balancer
- Layer 4 → Network Load Balancer

### Pricing

- Interruptible, restartable batch workload → Spot VM
- Predictable, long-term workload → consider CUD

### Compute choice

- VM → Compute Engine
- Kubernetes → GKE
- Serverless application/container → Cloud Run
- Event-driven function → Cloud Run functions

### Other high-value reminders

- Folders are optional.
- Project name can change; project ID and project number were described as unchangeable.
- Subnets are regional, so VMs in different zones can share a subnet.
- VPC peering is not transitive.
- Stopping a VM does not automatically eliminate persistent disk storage costs.
- One project can contain multiple VPCs.
- Quotas limit consumption; budgets help monitor spending.

---

## 22. Practice Questions

Try answering these before checking the answers.

<details>
<summary><strong>Q1. A developer creates three VMs at 2 AM without contacting the provider. Which cloud characteristic is this?</strong></summary>

**Answer:** On-demand self-service.
</details>

<details>
<summary><strong>Q2. A team uses Gmail and Google Docs without managing servers or patches. Which service model is this?</strong></summary>

**Answer:** SaaS.
</details>

<details>
<summary><strong>Q3. Which resource-hierarchy component is optional?</strong></summary>

**Answer:** Folder.
</details>

<details>
<summary><strong>Q4. Which project value can be changed according to the training discussion: name, ID, or number?</strong></summary>

**Answer:** Project name.
</details>

<details>
<summary><strong>Q5. What three questions does IAM answer?</strong></summary>

**Answer:** Who can do what on which resource?
</details>

<details>
<summary><strong>Q6. A user has an Allow permission, but a deny policy explicitly blocks the operation. What happens?</strong></summary>

**Answer:** The denied operation is blocked; deny overrides allow.
</details>

<details>
<summary><strong>Q7. Can VMs in different zones within a region use the same subnet?</strong></summary>

**Answer:** Yes. A subnet is regional.
</details>

<details>
<summary><strong>Q8. Is a VPC global, regional, or zonal? What about a subnet and a VM?</strong></summary>

**Answer:** VPC = global; subnet = regional; VM = zonal.
</details>

<details>
<summary><strong>Q9. A batch job can be interrupted and restarted. Which lower-cost VM option was discussed?</strong></summary>

**Answer:** Spot VM.
</details>

<details>
<summary><strong>Q10. What is the difference between vertical and horizontal scaling?</strong></summary>

**Answer:** Vertical scaling changes the size/capacity of a machine. Horizontal scaling changes the number of instances.
</details>

<details>
<summary><strong>Q11. If A peers with B and B peers with C, does A automatically connect to C?</strong></summary>

**Answer:** No. VPC peering is not transitive.
</details>

<details>
<summary><strong>Q12. Which load balancer layer was associated with application traffic in the session?</strong></summary>

**Answer:** Layer 7, Application Load Balancer.
</details>

<details>
<summary><strong>Q13. A project needs to limit API calls per minute. Is this a quota or a budget?</strong></summary>

**Answer:** Quota.
</details>

<details>
<summary><strong>Q14. What cost may remain after a VM is stopped?</strong></summary>

**Answer:** Attached/provisioned disk storage costs may continue.
</details>

<details>
<summary><strong>Q15. Which option was discussed for managing project billing without changing project resources?</strong></summary>

**Answer:** Billing Administrator.
</details>

---

## 23. Topics to Revisit Later

The trainer identified these as topics introduced or planned for subsequent sessions, rather than fully covered in Day 1:

- Detailed machine types
- Detailed scaling configuration
- Firewall configuration
- Load balancer implementation
- CDN implementation
- DNS implementation
- Detailed GKE
- Terraform
- Observability
- Detailed hybrid networking
- More practical labs
- PCA exam and case-study preparation

Keep these in separate day-wise notes as the training progresses.

---

## Final Revision Checklist

Use this checklist when revising Day 1:

- [ ] Explain the five cloud characteristics.
- [ ] Differentiate IaaS, PaaS, and SaaS.
- [ ] Explain regions and zones and why multi-zone deployment helps availability.
- [ ] Differentiate pay-as-you-go, CUD, quota, and budget.
- [ ] Draw the Organization → Folder → Project → Resource hierarchy.
- [ ] Explain project name, project ID, and project number.
- [ ] Explain IAM principals, roles, and deny policies.
- [ ] Explain service accounts and Cloud Identity at a high level.
- [ ] Remember VPC = global, subnet = regional, VM = zonal.
- [ ] Choose between Compute Engine, GKE, Cloud Run, and Cloud Run functions.
- [ ] Explain vertical versus horizontal scaling.
- [ ] Explain Spot VM trade-offs and persistent disk costs.
- [ ] Explain why VPC peering is not transitive.
- [ ] Differentiate Layer 4 and Layer 7 load balancing.
- [ ] Summarize VPN, Partner Interconnect, and Dedicated Interconnect at a high level.
