Git & GitHub - Quick Notes 📝
What is Git?
Git is a Version Control System (VCS).
It is software installed on your local computer.
Git tracks changes made to your project files.
If you make a mistake, Git lets you go back to an earlier version of your code.
Better than using only Ctrl + Z because Git keeps a complete history of changes.
Example
Python
1
print("Hello")
2
print("New Change")
Show more lines

If the new change causes an issue, Git can restore the previous working version.

What is GitHub?
GitHub is a cloud hosting service for Git repositories.
Stores:
Project files
Git commit history
Acts as an online backup of your code.
Benefits

✅ Backup your code

✅ Access code from anywhere

✅ Share projects with others

✅ Collaborate with team members

Git vs GitHub
Git	GitHubInstalled on local PC	Website/Cloud service
Tracks changes	Stores repositories online
Creates commits	Hosts commits and code
Version control	Backup + Collaboration

Simple way to remember:

Git = Tracks changes
 GitHub = Stores & Shares changes

What is a Commit?

A commit is a snapshot of your project at a specific time.

Example:

Plain Text
1
Commit 1 → Initial Project
2
Commit 2 → Added Login Page
3
Commit 3 → Fixed Bug
4
Commit 4 → Updated Image
Show more lines

You can return to any commit whenever needed.

Why Use Git?
1. Track Changes
Know what changed.
Know when it changed.
Know who changed it.
2. Undo Mistakes
Restore a previous working version quickly.
3. Backup Projects
Upload code to GitHub.
Recover files if your computer is lost or damaged.
4. Team Collaboration

Multiple developers can work on the same project.

Example:

Developer A works on Python code.
Developer B works on JavaScript.
Both upload changes to GitHub.
Changes are combined into one project.
GitHub Repository

A repository (repo) is a project stored on GitHub.

It can be:

Public Repository
Anyone can view the code.
Useful for portfolios.
Employers can see your projects.
Private Repository
Only approved people can access the code.
Good for company projects.
Why Not Just Use Google Drive or Dropbox?

Google Drive / Dropbox:

Store only files.

GitHub:

Stores files ✅
Stores version history ✅
Supports collaboration ✅
Allows rollback to older versions ✅

So GitHub is much more powerful for software development.

Real Workflow
Plain Text
1
1. Write code on local computer
2
↓
3
2. Git tracks changes
4
↓
5
3. Create Commit (Snapshot)
6
↓
7
4. Push Commit to GitHub
8
↓
9
5. Team members Pull changes
10
↓
11
6. Continue development
Show more lines
Interview Question Answer
What is Git?

Git is a distributed version control system that tracks changes in project files, allowing developers to manage versions, collaborate, and restore previous states of a project.

What is GitHub?

GitHub is a cloud-based platform that hosts Git repositories and provides features such as code backup, collaboration, version history, and project management.

Difference Between Git and GitHub?

Git is the tool used for version control, while GitHub is the online platform used to store and share Git repositories.

Fun Fact 🎉
Git was created in 2005 by Linus Torvalds, the creator of Linux.
The name "Git" comes from British slang meaning "an unpleasant person", chosen humorously by Linus.
One-Line Revision 🚀

Git = Track Changes
 Commit = Snapshot
 GitHub = Store + Share + Backup Code
 Repository = Project Folder on GitHub
 Push = Upload to GitHub
 Pull = Download from GitHub
