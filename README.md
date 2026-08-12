# GitRank

> Understand Git by building Git from scratch.

GitRank is a Python project that parses Git repositories directly from the `.git` directory without executing Git commands.

Instead of relying on commands such as `git log` or `git ls-tree`, GitRank reads and interprets Git's internal object database to reconstruct repository information.

The long-term goal is to evolve GitRank into a lightweight repository analytics engine capable of analyzing contributors, repository history, commit relationships, and code activity.

---

## Current Features

### Repository Resolution

- Validate Git repository paths
- Read and resolve `HEAD`
- Resolve local branch references
- Read branch commit hashes
- Traverse history from multiple branch heads

### Git Object Parsing

- Locate Git objects using SHA-1 hashes
- Read compressed Git objects
- Decompress objects using zlib
- Parse Git object headers
- Detect object types:
  - `commit`
  - `tree`
  - `blob`

### Commit Parsing

- Parse commit metadata
- Parse commit messages
- Parse parent commits
- Support multiple parents for merge commits
- Parse author information
- Parse committer information
- Convert Unix timestamps into readable dates

### Tree Parsing

- Parse Git tree objects
- Detect files and directories
- Recursively traverse repository trees
- Reconstruct repository file paths

### Blob Parsing

- Load blob objects
- Read file contents directly from Git objects

### Commit History

- Traverse complete commit history
- Traverse multiple parent relationships
- Traverse history from multiple local branch heads
- Use iterative DFS with a stack
- Track visited commits to avoid duplicate processing
- Build a commit-to-parent graph
- Topologically order commits from children to parents

### Contributor Analytics

- Count commits by contributor
- Rank contributors by commit count
- Identify commits belonging to a specific contributor
- Generate contributor statistics
- Identify merge commits authored by a contributor
- Determine first and latest commits
- Display first and latest commit messages

### Commit Graph

- Build a commit graph from commit-parent relationships
- Handle normal commits and merge commits
- Track multiple parent relationships
- Render commit history in the terminal
- Display commit hashes
- Display commit messages
- Display commit authors
- Display branch and merge relationships

### CLI

```bash
python3 main.py -p <repository_path>
```

Display statistics for a specific contributor:

```bash
python3 main.py -p <repository_path> -u <username>
```

---

## Example: Contributor Ranking

```text
------------- GitRank Statistics -----------
Rank    Name                        Commits
--------------------------------------------
1       bybhargav                        22
2       ManojKanakam                      2
3       Basani Sai Raju                   1
--------------------------------------------
```

---

## Example: Contributor Profile

```text
--------------------------------------------
--------- GitRank - User Statistics --------
--------------------------------------------
Name                : bybhargav
Email               : ...
Total Commits       : 22
Merge Commits       : 0
First Commit        : 30-07-2026 17:21:36
Last Commit         : 11-08-2026 13:23:01

First Commit Message:
Initial GitRank project

Last Commit Message:
Fix commit history traversal for merge commits

--------------------------------------------
```

---

## Example: Commit Graph

```text
--------------- GitRank - Commit Graph ---------------

* b678483  updated README.md
|
* 16a1c74  feat: add contributor user statistics
|
* c33523f  Fix commit history traversal for merge commits
|
* 77468ce  Fix commit history traversal for merge commits
|
* ab58d89  Merge pull request #1 from ManojKanakam/main
|\
| * 51dc9a9  Contributor: Testing
| * 14b6046  Contributor: Testing
|/
* 94dab69  Refactor Git object loading and implement commit history traversal
|
* 3ef95cd  parsing trial 1
```

The graph is built from Git's commit-parent relationships rather than from Git's command-line output.

---

## Project Structure

```text
GitRank/
│
├── main.py              # CLI entry point
├── gitinfo.py           # Git object parsing and repository traversal
├── gitanalytics.py      # Repository and contributor analytics
├── validator.py         # Git repository validation
├── tests/               # Tests
└── README.md
```

---

## How It Works

GitRank reconstructs repository information by reading Git's internal object database.

### Repository Resolution

```text
Repository
    │
    ▼
   .git
    │
    ├── HEAD
    │
    └── refs/heads/
           │
           ▼
      Branch Commit Hashes
           │
           ▼
      Commit Traversal
```

GitRank can start traversal from multiple local branch heads.

### Commit

```text
Commit
 ├── Tree
 │    │
 │    ▼
 │  Repository Files
 │
 └── Parent(s)
      │
      ▼
 Commit History
```

A normal commit has one parent:

```text
A
│
B
│
C
```

A merge commit can have multiple parents:

```text
    B
   / \
  C   D
   \ /
    E
```

GitRank traverses these relationships using an iterative depth-first traversal with a stack and a visited set.

---

## Architecture

```text
                    Git Repository
                          │
                          ▼
                    path_validator
                          │
                          ▼
                   Branch References
                          │
                          ▼
                 Commit History Walker
                          │
                          ▼
                       Commits
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
    Contributor Analytics        Commit Graph
             │                         │
       ┌─────┴─────┐             ┌─────┴─────┐
       │           │             │           │
       ▼           ▼             ▼           ▼
    Ranking     User Profile   Ordering   Visualization
```

---

## Roadmap

### Version 1

- [x] Read HEAD
- [x] Resolve branch references
- [x] Parse commit objects
- [x] Parse tree objects
- [x] Parse blob objects
- [x] Walk repository tree
- [x] Walk complete commit history
- [x] Handle multiple commit parents
- [x] Traverse multiple local branch heads
- [x] Build commit graph
- [x] Order commits topologically
- [x] Render commit graph in terminal
- [x] Contributor statistics
- [x] Contributor ranking
- [x] Contributor profile statistics
- [x] CLI repository path argument
- [x] CLI contributor argument
- [ ] Repository statistics
- [ ] Code churn metrics
- [ ] Lines added / removed

### Version 2

- [ ] Branch analysis
- [ ] File ownership analysis
- [ ] Lines added / removed
- [ ] Hotspot detection
- [ ] Repository health report
- [ ] Packed object support
- [ ] Git index parsing
- [ ] Advanced commit graph rendering

---

## Current Limitations

GitRank currently supports Git objects stored as loose objects inside:

```text
.git/objects/
```

Large repositories such as the Linux kernel commonly store objects inside packfiles:

```text
.git/objects/pack/
├── pack-*.pack
└── pack-*.idx
```

Packed objects are currently **not supported** by GitRank.

As a result, GitRank works with repositories whose required objects are available as loose objects, but it cannot yet fully process repositories that rely on packed object storage.

Packed-object support is planned for a future version.

---

## Why This Project?

GitRank is built as a systems programming project to understand how Git stores and traverses data internally.

Instead of treating Git as a command-line tool, GitRank explores:

- Git object storage
- Object compression
- Commit graphs
- Directed commit relationships
- Tree structures
- Blob storage
- Repository traversal
- Contributor analytics
- Branch relationships
- Merge commits

The project emphasizes learning Git's internal architecture by implementing its core concepts from scratch.

---

## Tech Stack

- Python 3.11+
- `pathlib`
- `zlib`
- `datetime`
- `argparse`

---

## Future Vision

GitRank aims to become a lightweight repository analytics tool capable of answering questions such as:

- Who contributes the most?
- What does an individual contributor work on?
- Which files change most frequently?
- Which developers own which files?
- How does the repository evolve over time?
- How active is the repository?
- What does the commit graph look like?
- How much code is being added or removed?
- Which parts of the repository are hotspots?

---

## Disclaimer

GitRank is an educational and experimental project created for learning,
curiosity, and fun.

It is provided for legitimate development, research, and educational use.
The author does not encourage or support using this project for malicious,
illegal, abusive, or harmful activities.

Use GitRank at your own discretion. The author is not responsible for any
damage, loss, misuse, or consequences resulting from the use of this project.