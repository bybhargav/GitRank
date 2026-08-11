# GitRank

> Understand Git by building Git from scratch.

GitRank is a Python project that parses Git repositories directly from the `.git` directory without executing Git commands.

Instead of relying on commands such as `git log` or `git ls-tree`, GitRank reads and interprets Git's internal object database to reconstruct repository information.

The long-term goal is to evolve GitRank into a lightweight repository analytics engine capable of analyzing contributors, repository history, commit relationships, and code activity.

---

## Current Features

### Repository Resolution

- Read and resolve `HEAD`
- Resolve branch references
- Read the current commit hash
- Validate Git repository paths

### Git Object Parsing

- Locate Git objects using SHA-1 hashes
- Read compressed Git objects
- Decompress objects using zlib
- Parse Git object headers
- Detect object types: `commit`, `tree`, `blob`

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
- Use iterative DFS with a stack
- Track visited commits to avoid duplicate processing

### Contributor Analytics

- Count commits by contributor
- Rank contributors by commit count
- Identify commits belonging to a specific contributor
- Generate contributor statistics
- Identify merge commits authored by a contributor
- Determine first and latest commits
- Display first and latest commit messages

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
    ▼
   HEAD
    │
    ▼
Branch Reference
    │
    ▼
Commit Hash
```

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
   /   C   D
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
                     HEAD Resolver
                          │
                          ▼
                    Commit Traversal
                          │
                          ▼
                       Commits
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
    Contributor Analytics        Commit Graph
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
    Ranking     User Profile
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
- [x] Contributor statistics
- [x] Contributor ranking
- [x] Contributor profile statistics
- [x] CLI repository path argument
- [x] CLI contributor argument
- [ ] Repository statistics
- [ ] Commit graph visualization
- [ ] Code churn metrics

### Version 2

- [ ] Branch analysis
- [ ] File ownership analysis
- [ ] Lines added / removed
- [ ] Hotspot detection
- [ ] Repository health report

---

## Current Limitations

GitRank currently reads Git objects stored as loose objects inside:

```text
.git/objects/
```

Packed Git objects inside:

```text
.git/objects/pack/
```

are not currently supported.

GitRank is intentionally focused on learning and reconstructing Git's internal architecture rather than providing full compatibility with every Git repository feature.

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

## License

MIT License
