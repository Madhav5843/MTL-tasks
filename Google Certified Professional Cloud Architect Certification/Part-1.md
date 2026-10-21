Absolutely. Since this is certification training, a study-notes format is much more useful than a normal meeting recap. Below are detailed Day 1 notes from the transcribed content available for Training Batch 1 || Google Certified Professional Cloud Architect Certification. The meeting search itself returned no additional result, so these notes are based on the meeting transcript already available in this conversation.

Google Professional Cloud Architect Training
Day 1 Study Notes
1. Training structure

Ashutosh S. Bhakare described this as an 8-day training program aimed at Google Professional Cloud Architect preparation.

Main areas planned:

Google Cloud fundamentals
Architecting with Compute Engine
Terraform
Google Kubernetes Engine (GKE)
Observability
Exam preparation

The overall program has 19 labs. The trainer advised participants to concentrate on understanding the theory and demonstrations during class. Step-by-step guidance for labs would also be shared so they can be completed separately.

The PCA exam was described in the session as:

Around 2 hours
Roughly 50–60 questions
Scenario/case-study oriented
Dedicated exam-preparation discussion planned toward the end of the training
Module 1: Google Cloud Fundamentals
2. What is cloud computing?

A simple way the trainer introduced cloud was as using somebody else's computing infrastructure rather than owning all the physical hardware yourself.

The important cloud characteristics discussed were:

On-demand self-service

Resources can be provisioned whenever required without waiting for someone at the cloud provider to manually create them.

Example from the quiz:
 A developer launches three VMs through the console at 2 AM without contacting the provider.

Answer: On-demand self-service.

Broad network access

Cloud resources can be accessed through networks from different locations.

Resource pooling

The provider's underlying infrastructure is pooled and used to serve customers.

Rapid elasticity

Capacity can increase or decrease depending upon demand.

Example:

Normal traffic → 2 servers
 Festival traffic → increase capacity
 Traffic drops → reduce capacity

This was identified as rapid elasticity.

Measured / pay-as-you-go usage

You pay according to resource consumption rather than purchasing all infrastructure permanently.

3. Cloud service models

The session covered three fundamental models.

IaaS: Infrastructure as a Service

The cloud provider manages the physical infrastructure, including areas such as:

networking
virtualization
physical servers
underlying storage infrastructure

The customer has greater responsibility for things above the infrastructure layer.

Example

Compute Engine VM

If you provision CPU, memory and disk resources, you pay for those provisioned resources based on the applicable pricing model.

Easy memory trick

IaaS = Rent infrastructure

PaaS: Platform as a Service

More of the underlying platform is managed by the cloud provider.

The user focuses more heavily on the application instead of managing infrastructure.

Easy memory trick

PaaS = Build/run applications on a managed platform

SaaS: Software as a Service

The complete application is provided as a service.

Examples discussed:

Gmail
Google Docs

You do not normally need to think about the application's underlying servers or patches.

Exam question

Your team uses Gmail and Google Docs and never thinks about servers or patches. Which service model?

Answer: SaaS

4. GCP regions and zones

This is an important PCA concept.

The trainer explained the hierarchy broadly as:

Global infrastructure → Regions → Zones

A region represents a geographical area.

A region contains multiple zones.

Zones allow workloads to be distributed for higher availability.

Multi-zone architecture

Example:

Region
  |
  +-- Zone A → App instance
  |
  +-- Zone B → App instance


If one zone becomes unavailable, workloads placed across other zones can help maintain availability.

Exam concept

Application deployed in:

asia-south1-a
asia-south1-b


The key protection being demonstrated is against a single-zone outage.

5. Multi-region architecture

For applications serving users across large geographical areas, resources can be deployed across regions.

Conceptually:

Users in APAC
      |
 APAC Region

Users in Europe
      |
 Europe Region


The trainer highlighted benefits such as:

lower latency
resilience against regional failure
placing services/data closer to users

Depending on the service, replication can be configured between locations.

6. Google network infrastructure

The session discussed Google's private/premium network backbone.

The key idea is that Google's global network infrastructure provides connectivity between regions and locations.

The trainer associated Google's premium network with:

higher throughput
lower latency

This was presented as one of the important characteristics of Google's infrastructure.

7. Open source and avoiding vendor lock-in

An important architectural theme discussed was Google's use of open-source technologies.

Examples mentioned:

Kubernetes

GKE is based around Kubernetes.

Because Kubernetes is open source and widely supported, containerized applications can potentially be easier to move between environments compared with completely proprietary solutions.

TensorFlow

Mentioned as Google's open-source machine learning framework.

Gemma

Mentioned as Google's open model family.

ADK

The trainer also mentioned Google's open-source agent development framework.

Exam takeaway

Question:

Which approach can help avoid vendor lock-in?

The answer discussed was using technologies such as:

Kubernetes and TensorFlow

8. Google Cloud pricing concepts

Several cost models were discussed.

Pay-as-you-go

Pay based on the resources being consumed.

Sustained use discounts

Discount concepts for workloads running for significant portions of a billing period were introduced.

Committed Use Discounts (CUD)

Useful when you expect to consume resources over a longer committed period.

Example from the session

A database runs 24×7 and is expected to continue for the next three years. Which pricing model fits?

Answer discussed: Committed Use Discount

9. Cloud Pricing Calculator

The trainer demonstrated the Google Cloud pricing calculator.

Examples of inputs included:

number of VM instances
operating system
machine configuration
CPU
memory
boot disk size
provisioning choices

The calculator can be used to estimate the cost of a proposed architecture.

10. Quotas and budgets

These are different ideas.

Quota

A quota limits resource/API consumption.

Examples discussed included restricting:

number of resources
API calls
Exam example

A project supports only a specified number of API calls per minute and the count resets afterward.

Answer: Quota

Budget

Budgets were discussed in the context of cost monitoring and notifications.

Simple distinction
Quota
   ↓
Controls resource/service consumption limits

Budget
   ↓
Helps monitor spending

Module 2: Resource Management and IAM
11. GCP resource hierarchy

One of the most important concepts from Day 1:

Organization
     ↓
   Folder
     ↓
  Project
     ↓
 Resources

Organization

Represents the top-level organizational node.

Folder

Used to organize projects.

Important: Folders are optional.

You can therefore have:

Organization
     ↓
   Project


without requiring a folder.

Folders can also contain subfolders.

Project

The project is where workloads/resources are organized and managed.

Important project-level concepts discussed:

billing
quotas
APIs/services
resources
Resources

Examples include:

Compute Engine instances
storage resources
Kubernetes resources
12. Project identifiers

The trainer identified three important project values:

Project Name

Human-friendly name.

Can be changed.

Project ID

Identifier associated with the project.

According to the session discussion, once established it is not changed.

Project Number

Unique numeric identifier generated for the project.

It cannot be changed.

Exam question

Which project identifier can be changed after project creation?

Answer: Project Name

13. Policy inheritance

Policies were described as flowing down the hierarchy.

Conceptually:

Organization policy
       ↓
Folder
       ↓
Project
       ↓
Resources


This hierarchical model is important when designing enterprise GCP environments.

14. Identity and Access Management: IAM

The trainer gave one very useful definition:

Who can do what on which resource?

Think of IAM as three questions:

WHO?
↓
Identity / principal

CAN DO WHAT?
↓
Permissions / role

ON WHAT?
↓
Resource

"Who" examples

The session discussed identities including:

users
groups
service accounts
Cloud Identity identities
15. IAM roles

Three categories were discussed.

Basic roles

Broad permissions.

Examples:

Viewer
Editor
Owner

Because they are broad, they offer less granular permission control.

Predefined roles

Created and maintained by Google for particular services/use cases.

Examples discussed included concepts such as:

Compute-related administrator roles
Storage administrator
GKE-related roles

These provide more targeted permissions than the basic roles.

Custom roles

Created when existing predefined roles provide more permissions than required.

They allow finer control over what somebody can perform.

Exam memory

From broad → fine-grained:

Basic
  ↓
Predefined
  ↓
Custom

16. Owner, Editor and Viewer

At a high level as presented in the training:

Viewer

Used for viewing resources rather than changing them.

Editor

Can modify many resources but does not provide the same access-management capabilities as Owner.

Owner

Very broad control, including access-management capabilities.

The trainer also discussed a separate Billing Administrator role for billing-related administration.

Exam scenario

Finance needs to manage project billing but should not change project resources.

Answer discussed: Billing Administrator

17. IAM Deny

Very important principle from today's session:

Deny overrides Allow.

Example:

A user has Editor permissions that would otherwise permit an operation.

A deny policy explicitly blocks deleting a VM.

Result:

The deletion is blocked.

Remember:

ALLOW + explicit DENY
          ↓
        DENY wins

18. Service accounts

A service account is an identity primarily intended for workloads/applications rather than a normal human user.

The trainer used the idea of:

Service A
   |
service identity
   |
Service B


instead of somebody manually entering a username and password for an application-to-application operation.

Service accounts were discussed in connection with:

APIs
applications/services
tokens/credentials
controlled resource access
Simple exam understanding

User account → Human

Service account → Workload/application

19. Cloud Identity and directory integration

Cloud Identity was introduced for centralized identity management.

The trainer also mentioned:

GCDS: Google Cloud Directory Sync

It was discussed as a way of synchronizing users from directory systems such as Active Directory/LDAP into the Google identity environment.

20. Ways to access and manage GCP

The session demonstrated/discussed several interfaces.

Google Cloud Console

Browser-based GUI.

Useful for:

exploring services
creating resources
administrative operations
Cloud Shell

Browser-accessible command environment.

Tools mentioned as available included:

gcloud
Docker
Terraform
BigQuery tooling
Cloud SDK

Enables Google Cloud command-line tooling to be used from a local environment.

API / client libraries

Applications/scripts can interact programmatically with Google Cloud.

Python was among the examples discussed.

Mobile application

Also mentioned as another mechanism for accessing certain Google Cloud information/actions.

Module 3: Marketplace, Compute and Networking
21. Google Cloud Marketplace

The trainer demonstrated Google Cloud Marketplace using a LAMP stack.

LAMP:

L → Linux
A → Apache
M → MySQL
P → PHP


Instead of manually installing each component individually, Marketplace provides packaged solutions that can provision a stack.

The demo created supporting resources such as the Compute resource and related configuration.

Takeaway

Marketplace = deploy preconfigured solutions more quickly.

22. VPC: Virtual Private Cloud

One of today's most important networking topics.

VPC provides logical networking/isolation for cloud resources.

The trainer also connected this with software-defined networking (SDN).

23. GCP VPC scope

VERY IMPORTANT EXAM POINT

VPC network

Global

Subnet

Regional

So remember:

VPC    = GLOBAL
Subnet = REGIONAL
VM     = ZONAL


This is worth memorizing.

24. Regional subnets

Unlike designs where you think in terms of a subnet belonging to one availability zone, the trainer emphasized that a GCP subnet is regional.

For example:

VPC - Global
 |
 +-- Subnet A - Region
       |
       +-- VM - Zone A
       |
       +-- VM - Zone B
       |
       +-- VM - Zone C


VMs can therefore exist in different zones while using the same regional subnet.

Exam question

Why can VMs in multiple zones share one subnet?

Because a subnet is regional, not zonal.

25. Multiple VPCs

The trainer confirmed that one project can contain multiple VPC networks.

Conceptually:

Project
 |
 +-- VPC-A
 |
 +-- VPC-B
 |
 +-- VPC-C


Each provides separate network environments.

26. Handling subnet IP exhaustion

A question was raised about exhausting a subnet's available IP addresses.

The trainer discussed two approaches:

Expand/edit the subnet's IP range when possible.
Create another subnet and place new resources there if necessary.

This came directly from the Q&A rather than the formal slides.

27. Compute Engine

Compute Engine provides virtual machines.

A VM can include:

vCPU
memory
operating system
disks/storage
network interfaces

VM instances can be created through methods including:

Console
gcloud
API

The console also showed equivalent CLI/Terraform configuration during the demonstration.

28. Application deployment choices discussed

The trainer introduced several GCP compute/application options.

Compute Engine

VM-based workloads.

You manage the virtual machine environment.

GKE

Google Kubernetes Engine.

Used for containerized workloads with Kubernetes orchestration.

The session mentioned both:

Stateful applications
Stateless applications
Cloud Run

Introduced as a serverless option for deploying stateless applications.

Cloud Run functions

Discussed for event-driven workloads/functions.

Mental model
Need VM?
→ Compute Engine

Need Kubernetes?
→ GKE

Need serverless container/application?
→ Cloud Run

Need event-driven function?
→ Cloud Run functions

29. Creating a VM

In the demonstration, the trainer went through configuration including:

VM name
Region/zone
Machine type
Operating-system image
Boot disk
Networking
External IP
Create instance

Linux VM access was demonstrated using SSH.

A Windows Server VM was also created, with access attempted using RDP.

The Windows demonstration experienced connection/loading delays.

30. VM machine types

Four broad workload-oriented categories were discussed.

General purpose

Balanced CPU/memory characteristics for common workloads.

Compute optimized

For CPU/compute-intensive workloads.

Memory optimized

For memory-intensive workloads.

Accelerator optimized

Associated with workloads requiring accelerators such as GPUs.

The trainer also noted that machine families/types have names such as E2, N-series, C-series, H-series, etc., and recommended referring to Google's machine-type documentation rather than relying entirely on naming conventions.

31. Vertical vs horizontal scaling

Another important exam concept.

Vertical scaling: Scale up/down

Increase/decrease the capacity of an existing machine.

Example:

4 vCPU / 16 GB
       ↓
8 vCPU / 32 GB

Horizontal scaling: Scale out/in

Change the number of instances.

Example:

VM1
VM2

Traffic increases
      ↓

VM1
VM2
VM3
VM4

Memorize

Scale UP = Bigger machine

Scale OUT = More machines

32. Spot VMs

Spot VMs use excess Google Cloud compute capacity at lower cost, with the major trade-off that Google can reclaim/terminate the capacity.

Therefore, the trainer specifically warned against depending completely on Spot VMs for workloads that cannot tolerate interruption.

Suitable classroom example

A batch job that can be stopped/restarted.

Exam question

A night batch job can be stopped and restarted without losing progress. Which option reduces cost?

Spot VM

33. VM shutdown and storage cost

An interesting participant question was about shutting down Compute Engine VMs.

The trainer explained that when compute is stopped, CPU and memory are no longer being consumed in the same way, but attached/provisioned disk remains and can still incur storage cost.

Easy memory:

VM stopped
   ↓
Compute not running

Disk still exists
   ↓
Storage cost can remain

34. Routes

Routes allow network traffic to be forwarded toward appropriate destinations.

This concept was introduced when discussing communication across network locations/subnets.

35. Firewall rules

Firewall rules control traffic.

The trainer demonstrated targeting firewall behavior using instance/network tags.

Example concept:

Web VM 1 → tag: web
Web VM 2 → tag: web
DB VM    → different tag

Firewall rule targeting "web"
        ↓
Web VMs targeted


However, the trainer warned about relying on loosely controlled tags in enterprise environments because users sharing the project may potentially apply tags incorrectly.

Service-account-based approaches were mentioned as something that would be covered further.

36. VPC Peering

Separate VPCs are isolated by default.

To establish connectivity between separate VPC networks, VPC Network Peering was introduced.

Conceptually:

VPC-A  ←──── Peering ────→  VPC-B


The trainer highlighted that peering is not transitive.

For example:

A ↔ B
B ↔ C


does not automatically mean:

A ↔ C


This is important when designing many interconnected VPCs.

37. Shared VPC

Shared VPC was introduced for sharing a network across multiple projects.

High-level concept:

Shared VPC
   |
   +-- Project A
   +-- Project B
   +-- Project C


The detailed implementation was not covered at this stage.

38. Load balancing

Load balancers distribute traffic across multiple backends.

Benefits discussed:

availability
traffic distribution
reduced latency depending on architecture

Two main categories were introduced.

Application Load Balancer

Works at Layer 7.

Associated with application/web traffic and proxy behavior.

SSL/TLS termination was also mentioned.

Network Load Balancer

Works at Layer 4.

Associated with network-level traffic forwarding.

Exam memory
L7 → Application Load Balancer
L4 → Network Load Balancer

39. Cloud DNS

Cloud DNS was introduced for mapping names to IP addresses.

Google's public DNS address 8.8.8.8 was also mentioned during the DNS discussion.

40. Cloud CDN

CDN means:

Content Delivery Network

The core concept introduced was caching content closer to consumers so the origin doesn't have to serve every request directly.

Benefits discussed:

lower latency
reduced load on origin
potential cost efficiency

Conceptually:

User
  ↓
CDN cache
  ↓  only when needed
Origin

41. Hybrid/private connectivity

Several connectivity options were introduced.

Cloud VPN

Provides an encrypted tunnel across network connectivity between environments such as on-premises and GCP.

On-premises
    |
 encrypted VPN
    |
   GCP

Partner Interconnect

Connectivity through supported partners/providers was introduced.

Dedicated Interconnect

Dedicated connectivity into Google's network was introduced for higher-capacity/private-connectivity requirements.

Peering

Direct/network peering concepts were also mentioned.

The session intentionally kept this section relatively high-level. More detailed discussion was expected later.

Day 1 Exam Cheat Sheet

If you're revising quickly before Day 2, Madhav, memorize these first:

GCP Resource Hierarchy
Organization
   ↓
Folder
   ↓
Project
   ↓
Resource

IAM
WHO
 ↓
can do WHAT
 ↓
on which RESOURCE

IAM Roles
Basic → Predefined → Custom
Broad                 Fine-grained

Networking scope

VPC     → GLOBAL
Subnet  → REGIONAL
VM      → ZONAL

Scaling

Vertical   → Bigger/smaller machine
Horizontal → More/fewer machines

Load Balancing

Layer 7 → Application Load Balancer
Layer 4 → Network Load Balancer

Pricing

Interruptible batch workload → Spot
Long predictable workload    → CUD

Compute choice

VM                  → Compute Engine
Kubernetes          → GKE
Serverless app      → Cloud Run
Event-driven logic  → Cloud Run functions


And especially remember:

Deny overrides Allow

Folders are optional

Project Name can change; Project ID/Number do not

Subnet is regional even when VMs are in different zones

VPC Peering is not transitive

Stopping a VM doesn't automatically eliminate persistent storage costs

Questions covered during the training

Some useful Q&A raised by participants:

Can one project contain multiple VPCs?
 Yes, according to the trainer.

Can VMs in separate zones use the same subnet?
 Yes. The reason emphasized was that subnets are regional.

What happens if a subnet runs out of IP addresses?
 The trainer discussed expanding the subnet range where possible or creating another subnet.

Is VPC peering transitive?
 No. The trainer said connections need to be established individually where required.

Can roles/permissions themselves incur a cost?
 The trainer answered no in the IAM discussion.

Do the labs require the participant's own GCP credits?
 The trainer said temporary lab access/credits would be provided through the training vendor.

Items planned for later

These topics were introduced but not covered deeply enough in Day 1 to treat today's discussion as complete study material:

Detailed machine types
Detailed scaling configuration
Firewall configuration
Detailed load balancer implementation
CDN implementation
DNS implementation
Detailed GKE
Terraform
Observability
Detailed hybrid networking
More practical labs
PCA exam/case-study preparation

Also, the trainer indicated that the remaining labs/details would continue in subsequent sessions, so I would keep those as separate Day 2+ notes rather than mixing them into today's material.
