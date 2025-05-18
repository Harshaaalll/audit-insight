"""TF-IDF vectorisation, dimensionality reduction, and document clustering.

Provides a three-step pipeline:

1. TF-IDF feature extraction
2. SVD + t-SNE dimensionality reduction to 2-D
3. KMeans clustering on the 2-D embedding
"""

from typing import List, Optional, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

from audit_insight.config import MAX_FEATURES, N_CLUSTERS, SVD_COMPONENTS, TSNE_PERPLEXITY


def compute_tfidf_vectors(
    cleaned_texts: List[str],
    max_features: Optional[int] = None,
) -> Tuple[TfidfVectorizer, "scipy.sparse.csr_matrix"]:
    """Compute TF-IDF document-term matrix.

    Parameters
    ----------
    cleaned_texts:
        Pre-processed texts (space-joined lemmas).
    max_features:
        Maximum vocabulary size.  Defaults to
        :pydata:`audit_insight.config.MAX_FEATURES`.

    Returns
    -------
    tuple
        ``(vectoriser, X)`` where *X* is a sparse document-term matrix.
    """
    max_features = max_features if max_features is not None else MAX_FEATURES
    vect = TfidfVectorizer(max_features=max_features)
    X = vect.fit_transform(cleaned_texts)
    return vect, X


def reduce_and_tsne(
    X: "scipy.sparse.csr_matrix",
    n_components_svd: Optional[int] = None,
    tsne_perplexity: Optional[int] = None,
    random_state: int = 42,
) -> np.ndarray:
    """Reduce dimensionality via SVD then t-SNE to 2-D.

    Parameters
    ----------
    X:
        Sparse or dense feature matrix (n_docs × n_features).
    n_components_svd:
        Components for TruncatedSVD.  Defaults to
        :pydata:`audit_insight.config.SVD_COMPONENTS`.
    tsne_perplexity:
        t-SNE perplexity.  Defaults to
        :pydata:`audit_insight.config.TSNE_PERPLEXITY`.
    random_state:
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        2-D array of shape ``(n_docs, 2)``.
    """
    n_components_svd = n_components_svd if n_components_svd is not None else SVD_COMPONENTS
    tsne_perplexity = tsne_perplexity if tsne_perplexity is not None else TSNE_PERPLEXITY

    svd = TruncatedSVD(
        n_components=min(n_components_svd, X.shape[1] - 1),
        random_state=random_state,
    )
    X_reduced = svd.fit_transform(X)

    effective_perplexity = min(tsne_perplexity, max(1, X_reduced.shape[0] - 1))

    tsne = TSNE(
        n_components=2,
        perplexity=effective_perplexity,
        random_state=random_state,
        n_jobs=1,
    )
    X_embedded: np.ndarray = tsne.fit_transform(X_reduced)
    return X_embedded


def cluster_documents(
    X_2d: np.ndarray,
    n_clusters: Optional[int] = None,
) -> np.ndarray:
    """Cluster 2-D document embeddings using KMeans.

    Parameters
    ----------
    X_2d:
        Array of shape ``(n_docs, 2)`` — typically the output of
        :pyfunc:`reduce_and_tsne`.
    n_clusters:
        Number of clusters.  Defaults to
        :pydata:`audit_insight.config.N_CLUSTERS`.

    Returns
    -------
    np.ndarray
        Integer cluster labels of shape ``(n_docs,)``.
    """
    n_clusters = n_clusters if n_clusters is not None else N_CLUSTERS
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels: np.ndarray = km.fit_predict(X_2d)
    return labels
