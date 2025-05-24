# 📦 Installation Guide

Complete setup instructions for **Audit Insight** on all major platforms.

---

## Prerequisites

| Requirement | Minimum Version | Check Command |
|-------------|----------------|---------------|
| Python | 3.9+ | `python --version` |
| pip | 21.0+ | `pip --version` |
| Git | 2.0+ | `git --version` |

> **Note:** A virtual environment is strongly recommended to avoid dependency conflicts.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/Harshaaalll/audit-insight.git
cd audit-insight
```

---

## Step 2: Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Once activated, your terminal prompt will be prefixed with `(venv)`.

---

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs all required packages:

| Package | Purpose |
|---------|---------|
| spacy | Text preprocessing (tokenization, lemmatization) |
| transformers | RoBERTa sentiment classification |
| torch | PyTorch backend for transformers |
| gensim | LDA topic modeling |
| scikit-learn | TF-IDF, SVD, t-SNE, KMeans |
| pandas | Data manipulation and CSV I/O |
| streamlit | Interactive web dashboard |

---

## Step 4: Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

This downloads the small English language model (~12 MB) required for text preprocessing.

---

## Step 5: Verify the Installation

Run the test suite to confirm everything is configured correctly:

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_preprocessing.py::test_clean_text PASSED
tests/test_sentiment.py::test_sentiment_labels PASSED
tests/test_topics.py::test_topic_count PASSED
tests/test_clustering.py::test_cluster_assignment PASSED
tests/test_utils.py::test_csv_read PASSED
...
```

All tests should pass with no errors.

---

## Step 6: Quick Smoke Test

Run the pipeline on the small sample dataset:

```bash
python -m audit_insight --input data/sample_docs.csv --output quick_test.csv
```

If the command completes without errors and produces `quick_test.csv`, the installation is successful.

---

## Optional: Install as Editable Package

For development, install the project in editable mode so that changes to the source code are reflected immediately:

```bash
pip install -e .
```

This allows you to import `audit_insight` from anywhere in your environment:

```python
from audit_insight.pipeline import run_pipeline
from audit_insight.preprocessing import preprocess_texts
```

---

## Optional: Launch the Streamlit Dashboard

```bash
streamlit run audit_insight/app/streamlit_app.py
```

The dashboard will open at `http://localhost:8501` in your default browser.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'spacy'` | Ensure the virtual environment is activated and run `pip install -r requirements.txt` |
| `OSError: [E050] Can't find model 'en_core_web_sm'` | Run `python -m spacy download en_core_web_sm` |
| `torch` installation issues on Windows | Visit [pytorch.org](https://pytorch.org/get-started/locally/) for platform-specific instructions |
| `streamlit` command not found | Ensure the virtual environment is activated or run `pip install streamlit` |
| Permission errors on Linux/macOS | Use `python3` and `pip3` instead of `python` and `pip` |

For additional help, see [troubleshooting.md](troubleshooting.md) or open an issue on [GitHub](https://github.com/Harshaaalll/audit-insight/issues).

---

[← Back to README](../README.md)
