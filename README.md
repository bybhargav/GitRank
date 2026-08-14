# GitRank

> **Understand Git by building Git from scratch.**

GitRank is an educational Python project that reads Git repositories directly from the `.git` directory instead of relying on commands such as `git log` or `git ls-tree`.

It reconstructs Git objects, commit history, branch relationships, contributor statistics, and commit graphs from Git's internal storage.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-Internals-F05032?style=for-the-badge&logo=git&logoColor=white)
![Status](https://img.shields.io/badge/Status-Learning%20Project-22C55E?style=for-the-badge)

</p>

---

## What GitRank Does

GitRank reads Git's internal object database and turns it into information that can be explored from the terminal.

```text
.git
 ├── HEAD
 ├── refs
 ├── objects
 │    ├── loose objects
 │    └── pack files
 │         ├── .idx
 │         └── .pack
 │
 └── Git history
        ↓
      GitRank
        ↓
  Analytics + Commit Graph
```

---

## Features

### Repository

- Read and resolve `HEAD`
- Resolve local branch references
- Traverse history from multiple branch heads
- Validate Git repository paths

### Git Objects

- Read loose Git objects
- Read packed Git objects
- Parse pack index (`.idx`) files
- Locate objects inside packfiles
- Parse packed object headers
- Decompress packed objects using `zlib`
- Resolve `OFS_DELTA`
- Resolve `REF_DELTA`
- Parse:
  - `commit`
  - `tree`
  - `blob`
  - `tag`

### Commit History

- Traverse complete commit history
- Support multiple parents
- Detect merge commits
- Track visited commits
- Build commit-to-parent relationships
- Topologically order commits

### Contributor Analytics

- Count commits by contributor
- Rank contributors
- Find commits made by a contributor
- Show contributor profile information
- Count merge commits
- Show first and latest commits
- Show first and latest commit messages

### Commit Graph

- Render commit history directly in the terminal
- Show commit relationships
- Show merge branches and joins
- Display commit hash, author, and message
- Use terminal colors to improve readability

### CLI

```bash
python3 main.py -p <repository_path>
```

Show contributor statistics:

```bash
python3 main.py -p <repository_path> -u <username>
```

Show the full commit graph:

```bash
python3 main.py -p <repository_path> -g
```

---

## Example

### GitRank Startup

```text
 ██████╗ ██╗████████╗██████╗  █████╗ ███╗   ██╗██╗  ██╗
██╔════╝ ██║╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
██║  ███╗██║   ██║   ██████╔╝███████║██╔██╗ ██║█████╔╝
██║   ██║██║   ██║   ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
╚██████╔╝██║   ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗
 ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

                GitRank — Git Analytics Engine
                        by bybhargav

[██░░░░░░░░░░░░░░░░░░] 10% Validating repository
[████████░░░░░░░░░░░░] 40% Reading commit history
[██████████████░░░░░░] 70% Analyzing contributors
[██████████████████░░] 90% Preparing contributor ranking
[████████████████████] 100% Yeah. We cooked. 🔥
```

### Contributor Ranking

```text
------------- GitRank Statistics -----------

Rank    Name                        Commits
--------------------------------------------
1       bybhargav                        26
2       ManojKanakam                      2
3       Basani Sai Raju                   1
--------------------------------------------
```

### Contributor Profile

```text
--------------------------------------------
--------- GitRank - User Statistics --------
--------------------------------------------
Name                : bybhargav
Email               : ...
Total Commits       : 26
Merge Commits       : 0
First Commit        : 30-07-2026 17:21:36
Last Commit         : 13-08-2026 23:40:36

First Commit Message:
  Initial GitRank project

Last Commit Message:
  intialised pack functions

--------------------------------------------
```

### Commit Graph

```text
--------------- GitRank - Commit Graph ---------------

* b678483  bybhargav  updated README.md
|
* 16a1c74  bybhargav  feat: add contributor user statistics
|
* c33523f  bybhargav  Fix commit history traversal
|
* 77468ce  bybhargav  Fix commit history traversal
|
* ab58d89  bybhargav  Merge pull request
|\
| * 51dc9a9  ManojKanakam  Contributor: Testing
| | 
| * 14b6046  ManojKanakam  Contributor: Testing
|/
* 94dab69  bybhargav  Refactor Git object loading
```

The terminal version uses colors for the commit node, hash, author, and message.

---

## Project Structure

```text
GitRank/
│
├── main.py
├── gitinfo.py
├── gitpack.py
├── gitanalytics.py
├── progress.py
├── validator.py
├── tests/
└── README.md
```

### Main Modules

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point |
| `gitinfo.py` | Repository, loose objects, commit/tree/blob parsing |
| `gitpack.py` | Pack index and packfile parsing, delta resolution |
| `gitanalytics.py` | Contributor analytics and commit graph |
| `progress.py` | Terminal banner, colors, and progress display |
| `validator.py` | Repository validation |

---

## How It Works

### Loose Objects

```text
Object SHA-1
    ↓
.git/objects/xx/yyyy...
    ↓
zlib decompression
    ↓
Git object header
    ↓
object type + body
```

### Packed Objects

```text
Object SHA-1
    ↓
.idx file
    ↓
fan-out table
    ↓
binary search
    ↓
pack offset
    ↓
.pack file
    ↓
packed object
```

### Delta Objects

```text
OFS_DELTA
    ↓
base object offset
    ↓
base object
    ↓
delta instructions
    ↓
reconstructed object
```

```text
REF_DELTA
    ↓
base object SHA-1
    ↓
base object
    ↓
delta instructions
    ↓
reconstructed object
```

All object loading paths ultimately expose the same interface:

```python
(object_type, body)
```

That means the higher-level commit, tree, and blob logic does not need to care whether an object came from loose storage or a packfile.

---

## Architecture

```text
                     Git Repository
                           │
                           ▼
                    Repository Resolver
                           │
                           ▼
                     Object Loader
                    /              \\
                   /                \\
          Loose Objects          Packed Objects
               │                    │
               │              ┌─────┴─────┐
               │              │           │
               │             .idx        .pack
               │                          │
               │                    Delta Resolution
               └──────────────┬───────────┘
                              ▼
                         Git Objects
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
             Commits        Trees         Blobs
                │
                ▼
         Commit History / DAG
                │
        ┌───────┴────────┐
        ▼                ▼
 Contributor Analytics  Graph Rendering
```

---

## Current Status

### GitRank v1

- [x] Repository validation
- [x] `HEAD` resolution
- [x] Local branch reference resolution
- [x] Loose object parsing
- [x] Packed object parsing
- [x] Pack index (`.idx`) parsing
- [x] Packfile (`.pack`) reading
- [x] `OFS_DELTA`
- [x] `REF_DELTA`
- [x] Commit parsing
- [x] Tree parsing
- [x] Blob parsing
- [x] Multi-parent commits
- [x] Commit history traversal
- [x] Contributor statistics
- [x] Contributor ranking
- [x] Contributor profile statistics
- [x] Commit graph generation
- [x] Topological commit ordering
- [x] Colored terminal output
- [x] Terminal progress display
- [x] CLI repository argument
- [x] CLI contributor argument
- [x] CLI graph argument

---

## Future Ideas

These are intentionally left for later versions:

- Incremental repository cache
- Repository-wide statistics
- Branch analysis
- Commit inspection
- File ownership analysis
- Lines added / removed
- Code churn metrics
- Hotspot detection
- Repository health reports
- More advanced graph rendering
- Performance improvements for very large repositories

---

## Why This Project?

GitRank started as a simple idea:

> **Understand Git by building Git from scratch.**

Instead of treating Git as a black-box command-line tool, the project explores how Git actually stores and connects data.

The project covers:

- Git object storage
- SHA-1 object lookup
- zlib compression
- pack indexes
- packfiles
- delta compression
- commit DAGs
- tree structures
- blobs
- branch relationships
- merge commits
- contributor analytics

The point is not to replace Git.

The point is to understand it.

---

## Tech Stack

- Python 3.11+
- `pathlib`
- `zlib`
- `datetime`
- `argparse`
- ANSI terminal escape codes

GitRank reconstructs repository history from Git's internal files rather than calling Git history commands.

---

## Disclaimer

GitRank is an educational and experimental project created for learning, curiosity, and fun.

It is intended for legitimate development, research, and educational use. The project is not intended to support malicious, illegal, abusive, or harmful activity.

Use GitRank at your own discretion. The author is not responsible for damage, loss, misuse, or other consequences resulting from use of the project.

---

## License

MIT License

Copyright (c) 2026 bybhargav

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
