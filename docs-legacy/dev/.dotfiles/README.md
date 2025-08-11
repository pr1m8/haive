# Dotfiles & Dotfolders Reference

This document explains each top-level hidden file and folder in the project, excluding temporary caches and database files. These files configure development tools, CI systems, linters, environment management, and documentation tooling.

---

## 🛠️ Development & Environment

| Path           | Type   | Purpose                                         |
| -------------- | ------ | ----------------------------------------------- |
| `.env`         | File   | Default environment variables (not committed)   |
| `.env.local`   | File   | Local overrides (developer-specific, untracked) |
| `.env.example` | File   | Template example of `.env` (safe to commit)     |
| `.env.dav`     | File   | Developer-specific env for "dav"                |
| `.venv/`       | Folder | Python virtual environment (often gitignored)   |

---

## 🧪 Linting & Formatting

| Path               | Type   | Purpose                                                                            |
| ------------------ | ------ | ---------------------------------------------------------------------------------- |
| `.flake8`          | File   | Config for [Flake8](https://flake8.pycqa.org/) Python linter                       |
| `.pydocstyle`      | File   | Rules for [pydocstyle](https://www.pydocstyle.org/) — docstring conventions        |
| `.codespellignore` | File   | Word list for [codespell](https://github.com/codespell-project/codespell)          |
| `.clocignore`      | File   | Ignore list for [cloc](https://github.com/AlDanial/cloc) — code line counter       |
| `.proselintrc`     | File   | Config for [proselint](https://github.com/amperser/proselint) — prose linter       |
| `.pyspelling.yml`  | File   | Spell checking config for [pyspelling](https://facelessuser.github.io/pyspelling/) |
| `.aspell.en.pws`   | File   | Custom dictionary of accepted domain-specific terms for spell checking             |
| `.vale.ini`        | File   | Main config for [Vale](https://vale.sh/) writing style linter                      |
| `.vale/`           | Folder | (If present) contains custom Vale styles or rules                                  |

---

## 🔍 Code Quality & Automation

| Path                      | Type   | Purpose                                                                           |
| ------------------------- | ------ | --------------------------------------------------------------------------------- |
| `.pre-commit-config.yaml` | File   | Hook config for [pre-commit](https://pre-commit.com/) automation                  |
| `.deepsource.toml`        | File   | Static analysis config for [DeepSource](https://deepsource.io/)                   |
| `.trunk/`                 | Folder | Config and cache for [Trunk](https://trunk.io/) unified code quality tooling      |
| `.nox/`                   | Folder | [Nox](https://nox.thea.codes/) automation sessions (often used for tests/linting) |

---

## 🧾 Git & Version Control

| Path             | Type   | Purpose                                                       |
| ---------------- | ------ | ------------------------------------------------------------- |
| `.git/`          | Folder | Main Git repository metadata                                  |
| `.gitignore`     | File   | Defines which files/folders Git should ignore                 |
| `.gitattributes` | File   | Controls Git behaviors (e.g., line endings, merge strategies) |
| `.gitmodules`    | File   | Lists Git submodules if any exist                             |
| `.github/`       | Folder | GitHub-specific automation (workflows, issue templates, etc.) |

---

## 📚 Documentation & Review

| Path                    | Type   | Purpose                                                           |
| ----------------------- | ------ | ----------------------------------------------------------------- |
| `.readthedocs.yaml`     | File   | [ReadTheDocs](https://readthedocs.org/) build config              |
| `.claude/`              | Folder | Likely related to Claude-based documentation review or AI tooling |
| `.benchmarks/`          | Folder | Contains benchmark data or performance results                    |
| `.approval_tests_temp/` | Folder | Temporary files used in approval testing frameworks               |

---

## 🧪 Experimental / Miscellaneous

| Path                  | Type   | Purpose                                                                                   |
| --------------------- | ------ | ----------------------------------------------------------------------------------------- |
| `.secrets/`           | Folder | Custom folder for sensitive info or placeholder secret configs (should be ignored in Git) |
| `.ipynb_checkpoints/` | Folder | Jupyter auto-generated checkpoints (can be ignored or deleted)                            |

---

## 📝 Notes

- This list excludes `.langchain.db`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, and other caches or runtime artifacts.
- Dotfiles like `.env`, `.venv`, and `.secrets` should be included in `.gitignore` unless they are templates.
- For spellcheck and documentation linting, see `.aspell.en.pws`, `.pyspelling.yml`, `.proselintrc`, and `.vale.ini`.

---

If you add or remove tooling, update this README so contributors understand the purpose of each configuration file.
