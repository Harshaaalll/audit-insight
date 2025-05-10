"""Configuration constants and default hyperparameters for Audit Insight.

Centralises every tuneable value so that the rest of the package never
hard-codes magic numbers.  Import from here rather than scattering
literals across modules.
"""

from typing import Dict

# ---------------------------------------------------------------------------
# Model identifiers
# ---------------------------------------------------------------------------

SPACY_MODEL: str = "en_core_web_sm"
"""Name of the spaCy language model used for preprocessing."""

ROBERTA_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment"
"""Hugging Face model identifier for RoBERTa-based sentiment analysis."""

# ---------------------------------------------------------------------------
# Sentiment label mapping
# ---------------------------------------------------------------------------

LABEL_MAP: Dict[str, str] = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
}
"""Maps the generic LABEL_0 / LABEL_1 / LABEL_2 tags returned by the
RoBERTa sentiment model to human-readable sentiment labels."""

# ---------------------------------------------------------------------------
# Default hyperparameters
# ---------------------------------------------------------------------------

NUM_TOPICS: int = 6
"""Default number of LDA topics."""

LDA_PASSES: int = 10
"""Default number of passes over the corpus during LDA training."""

TSNE_PERPLEXITY: int = 30
"""Default perplexity for t-SNE dimensionality reduction."""

N_CLUSTERS: int = 5
"""Default number of KMeans clusters."""

MAX_FEATURES: int = 5000
"""Maximum number of features (terms) retained by the TF-IDF vectoriser."""

SVD_COMPONENTS: int = 50
"""Number of components for TruncatedSVD before t-SNE."""
