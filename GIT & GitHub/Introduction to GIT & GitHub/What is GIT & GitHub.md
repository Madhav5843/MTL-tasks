## 1. What is Git?

**Git is a Version Control System (VCS).**

It is software installed on your **local computer** that tracks changes made to your project.

### Example

Suppose you have a Python project:

```text
my-project/
├── app.py
├── config.json
└── README.md
```

You make a change:

```python
print("Hello")
```

Git can record that change.

If the new code breaks your application, Git allows you to **go back to an earlier version** instead of manually using `Ctrl + Z`.

### Simple definition

> **Git = Tool that tracks changes and manages versions of your code.**

---

# 2. What is Version Control?

Version control means **keeping track of different versions of your project over time**.

For example:

```text
Version 1 → Original project
Version 2 → Added login
Version 3 → Added payment
Version 4 → Fixed login bug
Version 5 → Added dashboard
```

Git keeps track of these changes.

These saved versions are called **commits**.

---

# 3. What is a Commit?

A **commit** is basically a **snapshot of your project at a particular point in time**.

Example:

```text
Commit 1 → Created project
Commit 2 → Added login
Commit 3 → Fixed login bug
Commit 4 → Added payment
```

You can look through the history and potentially return to an earlier version.

### Remember:

**Commit = Snapshot / recorded change**

---

# 4. What is GitHub?

**GitHub is a hosting service for Git repositories.**

It allows you to store your Git-managed projects online.

Think of it like:

```text
Your Computer
     ↓
    Git
     ↓
   GitHub
```

Git works primarily on your local machine.

GitHub provides a remote place where your Git repository can be stored and shared.

---

# 5. Git vs GitHub

| Git                        | GitHub                           |
| -------------------------- | -------------------------------- |
| Version control software   | Hosting/collaboration platform   |
| Installed on your computer | Online service                   |
| Tracks code changes        | Stores Git repositories remotely |
| Creates commits            | Hosts those commits              |
| Works locally              | Works over the internet          |
| Can work without GitHub    | Uses Git repositories            |

### Easy way to remember

> **Git = tracks the changes**
> **GitHub = stores and shares those changes online**

---

# 6. GitHub is NOT Just Google Drive / Dropbox

A normal cloud storage service mainly stores files.

GitHub stores:

```text
Project files
     +
Commit history
     +
Version history
     +
Collaboration information
```

For example:

```text
Project
│
├── app.py
├── config.json
├── README.md
│
└── Git History
     ├── Commit 1
     ├── Commit 2
     ├── Commit 3
     └── Commit 4
```

So GitHub gives you much more than simple file backup.

---

# 7. Why Do We Use Git?

There are **3 major reasons** discussed in the video:

### 1. Track Changes

Git records changes made to your project.

```text
Old Code
   ↓
Make Changes
   ↓
Commit
   ↓
New Version
```

If something goes wrong, you can inspect the history and restore an earlier version.

---

### 2. Backup

GitHub can act as a remote copy of your project.

```text
Local Computer
      ↓
    Git
      ↓
   GitHub
```

If your computer is lost or the local project gets deleted, you can retrieve the repository from GitHub.

**Important:** Backup is mainly the GitHub/remote-repository part, not Git itself.

---

### 3. Collaboration

Multiple developers can work on the same project.

Example:

```text
Developer A
    ↓
   Git
    ↓
 GitHub
    ↑
   Git
    ↑
Developer B
```

Developer A might work on Python/backend code.

Developer B might work on JavaScript/frontend code.

Their changes can then be combined into the project.

---

# 8. How Collaboration Works

A simplified workflow:

```text
Developer A
     ↓
Make changes
     ↓
Commit
     ↓
Push to GitHub
     ↓
       GitHub
     ↑
Push
     ↑
Developer B
```

Then developers can **pull/download the latest changes** from GitHub to their own computers.

---

# 9. Repository

A **repository (repo)** is the project managed by Git.

It contains:

```text
Project files
+
Git information
+
Commit history
```

Example:

```text
my-devops-project/
│
├── app.py
├── Dockerfile
├── README.md
│
└── .git/
```

The `.git` directory contains Git's information about the repository and its history.

---

# 10. Public vs Private Repository

GitHub repositories can be:

### 🔒 Private

Only authorized people can access the code.

Useful for:

* Company projects
* Internal applications
* Private code
* Sensitive projects

### 🌍 Public

Other people can view the repository.

Useful for:

* Portfolio
* Open-source projects
* Showing projects to employers
* Sharing code publicly

---

# 11. Git Workflow

The basic Git workflow you'll learn is:

```text
Working Directory
       ↓
   git add
       ↓
   Staging Area
       ↓
   git commit
       ↓
 Local Repository
       ↓
   git push
       ↓
     GitHub
```

And when you want changes from GitHub:

```text
GitHub
   ↓
git pull
   ↓
Local Repository
```

This workflow is **very important for DevOps**.

---

# 12. Git vs GitHub in One Example

Imagine you're working on an AWS project.

You have:

```text
terraform/
├── main.tf
├── variables.tf
└── outputs.tf
```

You modify `main.tf`.

Git tracks:

```text
Before
   ↓
main.tf version 1

After
   ↓
main.tf version 2
```

You commit it:

```text
git commit
```

Then upload it to GitHub:

```text
git push
```

Now your repository on GitHub contains the project and its Git history.

---

# 13. Git Creator

**Git was created by Linus Torvalds in 2005.**

He is also well known as the creator of the **Linux kernel**.

The name "Git" was chosen with a bit of humor, referring to British slang.

---

# 🧠 Quick Revision

Remember these 7 points:

```text
Git
 ↓
Version Control System

Git tracks
 ↓
Changes

Commit
 ↓
Snapshot of changes

GitHub
 ↓
Online hosting for Git repositories

GitHub provides
 ↓
Remote storage + collaboration

Repository
 ↓
Project + Git history

Public / Private
 ↓
Who can access the repository
```

### ⭐ Most important line

> **Git tracks and manages changes locally. GitHub hosts Git repositories online and enables backup and collaboration.**

### DevOps connection

Git/GitHub will become the foundation for things you'll learn later:

```text
Git
 ↓
GitHub
 ↓
CI/CD
 ↓
Jenkins / GitHub Actions
 ↓
Docker
 ↓
Kubernetes
 ↓
AWS
```

So don't treat Git as just another tool to memorize. **Git is one of the core building blocks of modern DevOps.**
