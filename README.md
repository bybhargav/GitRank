# GitRank

> Understand Git by building Git from scratch.

GitRank is a Python project that parses Git repositories directly from the `.git` directory without executing Git commands. Instead of relying on `git log`, `git ls-tree`, or other CLI utilities, GitRank reads and interprets Git's internal object database to reconstruct repository information.

The long-term goal is to evolve GitRank into a repository analytics engine capable of ranking contributors, analyzing repository history, and generating insights from Git internals.

---

## Current Features

### Repository Resolution
- Read and resolve `HEAD`
- Resolve branch references
- Read the latest commit hash

### Git Object Parsing
- Locate Git objects using SHA-1 hashes
- Read compressed Git objects
- Decompress objects using zlib
- Parse Git object headers
- Detect object types (`commit`, `tree`, `blob`)

### Commit Parsing
- Parse commit metadata
- Parse commit messages
- Parse parent commits
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
- Traverse commit history using parent references
- Reconstruct repository history without using `git log`

---

## Example Output

```
Commit Metadata
================

Author      : bybhargav
Date        : 05-08-2026 19:10:54

Commit Message
==============

Parsing trial 1

Repository Files
================

.gitignore
README.md
gitinfo.py
main.py
tests/test.txt
validator.py
```

---

## Project Structure

```
GitRank/
│
├── main.py          # Entry point
├── gitinfo.py       # Git object parsing engine
├── validator.py     # Repository validation
├── tests/
└── README.md
```

---

## How It Works

```
HEAD
 │
 ▼
Reference
 │
 ▼
Latest Commit
 │
 ▼
Tree Object
 │
 ▼
Repository Files
```

GitRank reconstructs repository information by following Git's object graph:

```
HEAD
 │
 ▼
Commit
 │
 ├── Tree
 │      │
 │      ▼
 │   Files
 │
 └── Parent Commit
        │
        ▼
     Commit History
```

No Git CLI commands are required during parsing.

---

## Roadmap

### Version 1
- [x] Read HEAD
- [x] Parse commit objects
- [x] Parse tree objects
- [x] Parse blob objects
- [x] Walk repository tree
- [x] Walk commit history
- [ ] Contributor statistics
- [ ] Repository statistics
- [ ] CLI report

### Version 2
- [ ] Merge commit traversal
- [ ] Branch analysis
- [ ] File ownership analysis
- [ ] Code churn metrics
- [ ] Hotspot detection
- [ ] Repository health report

---

## Why This Project?

GitRank is built as a systems programming project to understand how Git stores data internally.

Instead of treating Git as a command-line tool, GitRank explores:

- Git object storage
- Object compression
- Commit graphs
- Tree structures
- Blob storage
- Repository traversal

The project emphasizes learning Git's internal architecture by implementing its core concepts from scratch.

---

## Tech Stack

- Python 3.11+
- pathlib
- zlib
- datetime

---

## Future Vision

GitRank aims to become a lightweight repository analytics tool capable of answering questions such as:

- Who contributes the most?
- Which files change most frequently?
- Which developers own which files?
- Repository growth over time
- Commit activity trends
- Repository health metrics

---

## License

MIT License