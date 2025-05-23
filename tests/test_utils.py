"""Tests for :mod:`audit_insight.utils`."""

import os
from pathlib import Path

import pandas as pd
import pytest

from audit_insight.utils import load_documents_from_csv


# Resolve the path to data/sample_docs.csv relative to the repo root
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SAMPLE_CSV = _REPO_ROOT / "data" / "sample_docs.csv"


class TestLoadDocumentsFromCsv:
    """Unit tests for ``load_documents_from_csv``."""

    def test_loads_sample_docs(self) -> None:
        """Should load sample_docs.csv and return a DataFrame with a
        ``text`` column."""
        df = load_documents_from_csv(str(_SAMPLE_CSV))
        assert isinstance(df, pd.DataFrame)
        assert "text" in df.columns
        # sample_docs.csv has 4 data rows (the last line is blank)
        assert len(df) >= 3

    def test_returns_only_text_column(self) -> None:
        """Result DataFrame should contain exactly one column."""
        df = load_documents_from_csv(str(_SAMPLE_CSV))
        assert list(df.columns) == ["text"]

    def test_raises_for_missing_column(self, tmp_path: Path) -> None:
        """Should raise ``ValueError`` when the requested text column
        does not exist in the CSV."""
        csv_path = tmp_path / "bad.csv"
        pd.DataFrame({"other_col": ["hello"]}).to_csv(csv_path, index=False)

        with pytest.raises(ValueError, match="Column 'text' not found"):
            load_documents_from_csv(str(csv_path))

    def test_custom_text_column(self, tmp_path: Path) -> None:
        """Should correctly rename a custom text column to ``text``."""
        csv_path = tmp_path / "custom.csv"
        pd.DataFrame({"content": ["a", "b"]}).to_csv(csv_path, index=False)

        df = load_documents_from_csv(str(csv_path), text_col="content")
        assert list(df.columns) == ["text"]
        assert df["text"].tolist() == ["a", "b"]

    def test_raises_for_missing_custom_column(self, tmp_path: Path) -> None:
        """Should raise ``ValueError`` for a custom column name that
        does not exist."""
        csv_path = tmp_path / "missing.csv"
        pd.DataFrame({"x": [1]}).to_csv(csv_path, index=False)

        with pytest.raises(ValueError, match="Column 'body' not found"):
            load_documents_from_csv(str(csv_path), text_col="body")
