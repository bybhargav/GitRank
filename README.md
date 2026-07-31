# GitRank

GitRank is a command-line tool for understanding and analyzing Git repositories by reading Git internals directly, without relying on Git commands.

The goal of this project is not only to build repository analytics, but also to understand how Git works under the hood by implementing its core object-reading pipeline from scratch.

---

## Current Features

- ✅ Validate repository paths
- ✅ Detect Git repositories
- ✅ Read `.git/HEAD`
- ✅ Resolve `HEAD` to the current branch reference
- ✅ Read the latest commit hash
- ✅ Locate Git objects using SHA-1 hashes
- ✅ Read Git objects in binary format
- ✅ Decompress Git objects using `zlib`

---

## Current Pipeline

```text
Repository
    │
    ▼
Validate Repository
    │
    ▼
Locate .git
    │
    ▼
Read HEAD
    │
    ▼
Resolve Branch Reference
    │
    ▼
Read Commit Hash
    │
    ▼
Locate Git Object
    │
    ▼
Read Binary Object
    │
    ▼
Decompress Git Object
```

---

## Project Structure

```
GitRank/
├── main.py          # Application entry point
├── validator.py     # Repository validation
├── gitinfo.py       # Git object and reference handling
└── README.md
```

---

## Usage

Clone the repository:

```bash
git clone https://github.com/bysairaju/GitRank.git
cd GitRank
```

Run GitRank on any local Git repository:

```bash
python main.py /path/to/repository
```

Example:

```bash
python main.py ~/Projects/my-repository
```

---

## Roadmap

### Repository

- [x] Repository validation
- [x] Git repository detection

### HEAD & References

- [x] Read `.git/HEAD`
- [x] Resolve current branch reference
- [x] Read current commit hash

### Git Objects

- [x] Locate Git object
- [x] Read Git object
- [x] Decompress Git object
- [ ] Parse commit objects
- [ ] Parse tree objects
- [ ] Parse blob objects

### Repository Traversal

- [ ] Traverse commit history
- [ ] Parse branches
- [ ] Parse tags

### Analytics

- [ ] Contributor statistics
- [ ] Commit leaderboard
- [ ] Repository insights

### Visualization

- [ ] Branch graph
- [ ] Commit graph
- [ ] Repository visualization

---

## Why GitRank?

Most Git analytics tools rely on Git commands internally.

GitRank takes a different approach by reading Git's object database directly, making it both a learning project and a foundation for advanced repository analytics and visualizations.

---

## License

This project is licensed under the MIT License.