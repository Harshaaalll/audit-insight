"""Tests for :mod:`audit_insight.clustering`."""

import numpy as np
import pytest
from scipy.sparse import issparse

from audit_insight.clustering import (
    cluster_documents,
    compute_tfidf_vectors,
    reduce_and_tsne,
)


# Audit-themed sample texts shared across tests
_SAMPLE_TEXTS = [
    "internal control weakness identified during audit",
    "revenue recognition policy compliance review",
    "accounts payable reconciliation discrepancy found",
    "risk assessment of financial reporting processes",
    "segregation of duties violation in procurement",
    "inventory count variance exceeds materiality threshold",
    "management override of internal controls detected",
    "audit committee reviewed quarterly financial statements",
]


class TestComputeTfidfVectors:
    """Unit tests for ``compute_tfidf_vectors``."""

    def test_tfidf_returns_sparse_matrix(self) -> None:
        """Output should be a tuple of (TfidfVectorizer, sparse matrix)."""
        vect, X = compute_tfidf_vectors(_SAMPLE_TEXTS[:5])
        assert issparse(X), "TF-IDF output should be a sparse matrix"

    def test_tfidf_shape_matches_input(self) -> None:
        """Rows of the TF-IDF matrix should match the number of input
        texts."""
        vect, X = compute_tfidf_vectors(_SAMPLE_TEXTS)
        assert X.shape[0] == len(_SAMPLE_TEXTS)


class TestReduceAndTsne:
    """Unit tests for ``reduce_and_tsne``."""

    def test_reduce_and_tsne_returns_2d(self) -> None:
        """Output shape should be (n_docs, 2)."""
        _, X = compute_tfidf_vectors(_SAMPLE_TEXTS)
        X_2d = reduce_and_tsne(X, n_components_svd=5, tsne_perplexity=5)
        assert X_2d.shape == (len(_SAMPLE_TEXTS), 2)

    def test_perplexity_guard_small_dataset(self) -> None:
        """A dataset smaller than the default perplexity (30) should
        not crash thanks to the perplexity guard."""
        small_texts = [
            "audit risk identified",
            "compliance review completed",
            "internal control testing",
        ]
        _, X = compute_tfidf_vectors(small_texts)
        # Default perplexity is 30 but we only have 3 samples — the
        # guard should clamp perplexity and avoid a ValueError.
        X_2d = reduce_and_tsne(X, n_components_svd=2)
        assert X_2d.shape == (3, 2)


class TestClusterDocuments:
    """Unit tests for ``cluster_documents``."""

    def test_cluster_documents_returns_correct_count(self) -> None:
        """Number of labels should equal the number of input
        documents."""
        _, X = compute_tfidf_vectors(_SAMPLE_TEXTS)
        X_2d = reduce_and_tsne(X, n_components_svd=5, tsne_perplexity=5)
        labels = cluster_documents(X_2d, n_clusters=3)
        assert len(labels) == len(_SAMPLE_TEXTS)

    def test_cluster_labels_within_range(self) -> None:
        """All cluster labels should be in [0, n_clusters)."""
        n_clusters = 3
        _, X = compute_tfidf_vectors(_SAMPLE_TEXTS)
        X_2d = reduce_and_tsne(X, n_components_svd=5, tsne_perplexity=5)
        labels = cluster_documents(X_2d, n_clusters=n_clusters)
        assert all(0 <= lbl < n_clusters for lbl in labels)
