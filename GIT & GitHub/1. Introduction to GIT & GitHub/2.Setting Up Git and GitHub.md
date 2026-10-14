# Git & GitHub Installation - Notes

## 1. Create a GitHub Account

Go to **GitHub** and create a free account.

[GitHub](https://github.com/?utm_source=chatgpt.com)

### Steps

```text
github.com
   ↓
Sign Up
   ↓
Create Account
   ↓
Login
```

If it's a new account, the **Repositories** section will initially be empty.

---

# 2. Install Git

Git is installed on your **local computer**.

Official Git website:

[Git Downloads](https://git-scm.com/downloads?utm_source=chatgpt.com)

Git provides installers for:

- Windows
- macOS
- Linux

---

# 3. Install Git on macOS

On Mac, the video uses **Homebrew**.

### What is Homebrew?

**Homebrew is a package manager for macOS.**

It allows you to easily install software from the Terminal.

### Step 1: Install Homebrew

Go to:

[Homebrew](https://brew.sh/?utm_source=chatgpt.com)

Copy the installation command provided there and run it in Terminal.

You may need to enter your Mac administrator password.

### Step 2: Install Git

After Homebrew is installed:

```bash
brew install git
```

### Step 3: Verify Git

Run:

```bash
git
```

If Git is installed correctly, you'll see the Git help/usage information.

---

# 4. Install Git on Linux

Git can be installed using the package manager for your Linux distribution.

For example, on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install git
```

Then verify:

```bash
git
```

or:

```bash
git --version
```

---

# 5. Install Git on Windows

Go to the official Git website:

[Git for Windows](https://git-scm.com/download/win?utm_source=chatgpt.com)

Download the **64-bit Windows installer**.

Then open the downloaded installer.

---

## Windows Installation Steps

The installer will show several configuration screens.

### 1. Installation Location

Choose where Git should be installed.

You can normally keep the **default location**.

---

### 2. Default Editor

Git asks which text editor you want to use by default.

The video chooses:

**Notepad++**

For beginners, you can select an editor you're comfortable with.

---

### 3. Default Branch Name

Git asks what the initial/default branch should be called.

The video selects:

```text
main
```

So:

```text
main = default branch
```

> Note: This doesn't mean all Git repositories must use `main`, but it is the common default today.

---

### 4. Other Options

The installer provides several additional configuration options.

For beginners:

**Keep the default options unless you have a specific reason to change them.**

Then continue:

```text
Next
↓
Next
↓
Next
↓
Install
↓
Finish
```

---

# 6. Verify Git Installation

After installation, open **Command Prompt**, **PowerShell**, or **Git Bash**.

Run:

```bash
git --version
```

You should get something similar to:

```text
git version 2.x.x
```

This confirms Git is installed successfully. ✅

---

# 7. Important Terms

| Term | Meaning |
|---|---|
| **GitHub** | Online platform for hosting Git repositories |
| **Git** | Version control software |
| **Homebrew** | Package manager for macOS |
| **Repository** | Project managed by Git |
| **Branch** | Separate line of development |
| **main** | Common default branch name |
| **Git Bash** | Terminal provided with Git for Windows |

---

# 🧠 Quick Revision

### GitHub

```text
GitHub
  ↓
Create account
  ↓
Login
  ↓
Create repositories
```

### Git Installation

```text
Windows → Download Git installer
macOS   → Homebrew → brew install git
Linux   → Package manager → Install Git
```

### Verify

```bash
git --version
```

If you see the Git version:

**Git installation = successful ✅**

---

## ⭐ DevOps Note

For your DevOps learning, remember this distinction:

```text
GitHub
   ↑
   │ git push
   │
Git
   ↑
   │
Your Project
```

**Git runs on your machine. GitHub is the remote platform where you can store and collaborate on your Git repositories.**
