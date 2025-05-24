# 🔧 Troubleshooting

Common issues and solutions when working with **Audit Insight**.

---

## Installation Issues

### `ModuleNotFoundError: No module named 'spacy'`

**Cause:** Virtual environment is not activated, or dependencies are not installed.

**Fix:**
```bash
# Activate the virtual environment first
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### `OSError: [E050] Can't find model 'en_core_web_sm'`

**Cause:** The spaCy language model has not been downloaded.

**Fix:**
```bash
python -m spacy download en_core_web_sm
```

---

### `torch` installation issues on Windows

**Cause:** PyTorch may require platform-specific installation steps.

**Fix:**
Visit [pytorch.org/get-started](https://pytorch.org/get-started/locally/) and select your OS, package manager, and CUDA version to get the correct install command.

---

## Pipeline Issues

### `ValueError: Column 'text' not found`

**Cause:** The input CSV does not contain a column named `text`.

**Fix:**
Either rename the column in your CSV, or use the `--text-col` flag:
```bash
python -m audit_insight --input data/your_file.csv --output results.csv --text-col "your_column_name"
```

---

### RoBERTa model not loading

**Cause:** First-time download requires internet access (~500 MB model).

**Fix:**
- Ensure you have a stable internet connection
- If behind a corporate proxy, configure the `HTTP_PROXY` / `HTTPS_PROXY` environment variables
- Alternatively, download the model manually from [HuggingFace](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) and place it in your local cache

---

### t-SNE takes too long

**Cause:** t-SNE has O(n²) complexity and is slow on large datasets.

**Fix:**
- Reduce your dataset size for initial testing
- Lower `SVD_COMPONENTS` in `config.py` (e.g., from 50 to 20)
- Consider replacing t-SNE with UMAP (planned for a future release)

---

### `ValueError: perplexity must be less than n_samples`

**Cause:** Your dataset has fewer rows than the default t-SNE perplexity (30).

**Fix:**
This is handled automatically by the perplexity guard in `clustering.py`. If you still encounter this error, reduce `TSNE_PERPLEXITY` in `config.py`:
```python
TSNE_PERPLEXITY: int = 5  # Lower for small datasets
```

---

## Streamlit Issues

### Streamlit app shows empty results

**Cause:** The uploaded CSV is missing the required `text` column.

**Fix:**
Ensure your CSV file has a column named `text` containing the audit observations.

---

### `streamlit` command not found

**Cause:** Streamlit is not installed or the virtual environment is not activated.

**Fix:**
```bash
pip install streamlit
```

---

### PyInstaller exe fails to run

**Cause:** Packaging Streamlit with PyInstaller is complex due to dynamic imports.

**Fix:**
Use the launcher approach instead:
```bash
python -m audit_insight.app.launcher
```

---

## Still Stuck?

If your issue is not listed here:

1. Check the [GitHub Issues](https://github.com/Harshaaalll/audit-insight/issues) page
2. Open a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Python version and OS
   - Full error traceback

---

[← Back to README](../README.md)
