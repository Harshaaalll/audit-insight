# 🤝 Contributing to Audit Insight

Thank you for considering contributing to **Audit Insight**! Every contribution — whether it's a bug fix, feature, or documentation improvement — is valued and appreciated.

---

## 📋 How to Contribute

1. **Check existing issues** — Browse [open issues](https://github.com/Harshaaalll/audit-insight/issues) to see if your idea or bug is already tracked.
2. **Open a new issue** — If not, create one describing the bug or feature request with as much detail as possible.
3. **Fork & code** — Follow the workflow below to submit your changes.

---

## 🛠️ Setting Up the Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/audit-insight.git
cd audit-insight

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate          # Windows

# 3. Install dependencies (including dev tools)
pip install -r requirements.txt
pip install -e ".[dev]"

# 4. Download the spaCy model
python -m spacy download en_core_web_sm
```

---

## 🎨 Code Style

This project uses **[Ruff](https://docs.astral.sh/ruff/)** for linting and formatting.

```bash
# Run the linter
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

**Key rules:**
- Maximum line length: **120 characters**
- Target Python version: **3.9+**
- Write clear docstrings for public functions and classes
- Use type hints where practical

---

## 🔀 Submitting Changes

1. **Fork** the repository on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit with clear, descriptive messages:
   ```bash
   git commit -m "feat: add PII masking to preprocessing pipeline"
   ```
4. **Run tests** to make sure nothing is broken:
   ```bash
   pytest
   ```
5. **Push** your branch and open a **Pull Request** against `main`:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Fill out the PR template describing **what** you changed and **why**

---

## 🐛 Reporting Issues

When filing an issue, please include:

- **Description** — What happened vs. what you expected
- **Steps to reproduce** — Minimal steps to trigger the bug
- **Environment** — Python version, OS, relevant package versions
- **Logs / tracebacks** — Paste any error output

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for helping make Audit Insight better! 🚀
