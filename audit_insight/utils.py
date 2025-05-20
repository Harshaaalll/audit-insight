"""Utility helpers for CSV I/O and result assembly.

Contains functions shared by the CLI pipeline runner and the Streamlit
front-end but not specific to any single NLP step.
"""

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


def load_documents_from_csv(
    path: str,
    text_col: str = "text",
) -> pd.DataFrame:
    """Load a CSV file and return a DataFrame with a ``text`` column.

    Parameters
    ----------
    path:
        Filesystem path to the input CSV.
    text_col:
        Name of the column containing raw document text.

    Returns
    -------
    pd.DataFrame
        A DataFrame with a single ``text`` column.

    Raises
    ------
    ValueError
        If *text_col* is not present in the CSV.
    """
    df = pd.read_csv(path)
    if text_col not in df.columns:
        raise ValueError(
            f"Column '{text_col}' not found in {path}. "
            f"Available columns: {df.columns.tolist()}"
        )
    df = df[[text_col]].copy().rename(columns={text_col: "text"})
    return df


def assemble_result_dataframe(
    original_texts: List[str],
    cleaned_texts: List[str],
    sentiment_results: List[Dict[str, Any]],
    docs_topics: List[Dict[str, Any]],
    tsne_coords: Optional[np.ndarray],
    cluster_labels: Optional[np.ndarray] = None,
    dictionary: Optional[Any] = None,
    lda_model: Optional[Any] = None,
) -> pd.DataFrame:
    """Combine every pipeline output into a single result DataFrame.

    Parameters
    ----------
    original_texts:
        Raw document strings.
    cleaned_texts:
        Preprocessed (lemmatised) strings.
    sentiment_results:
        Per-document sentiment dicts with ``label`` and ``score`` keys.
    docs_topics:
        Per-document topic dicts with ``topic_id`` and ``topic_prob``.
    tsne_coords:
        2-D array of shape ``(n_docs, 2)`` from t-SNE, or *None*.
    cluster_labels:
        Integer cluster labels of shape ``(n_docs,)``, or *None*.
    dictionary:
        Gensim :class:`~gensim.corpora.Dictionary` (kept for
        forward-compatibility).
    lda_model:
        Trained :class:`~gensim.models.LdaModel` (kept for
        forward-compatibility).

    Returns
    -------
    pd.DataFrame
        Columns: ``text``, ``cleaned_text``, ``sentiment_label``,
        ``sentiment_score``, ``topic_id``, ``topic_prob``,
        ``tsne_x``, ``tsne_y``, ``cluster_label``.
    """
    rows: List[Dict[str, Any]] = []
    for i, txt in enumerate(original_texts):
        sent = (
            sentiment_results[i]
            if i < len(sentiment_results)
            else {"label": None, "score": None}
        )
        topic = (
            docs_topics[i]
            if i < len(docs_topics)
            else {"topic_id": None, "topic_prob": None}
        )
        if tsne_coords is not None:
            x, y = float(tsne_coords[i, 0]), float(tsne_coords[i, 1])
        else:
            x, y = None, None

        cluster = (
            int(cluster_labels[i])
            if cluster_labels is not None and i < len(cluster_labels)
            else None
        )

        rows.append(
            {
                "text": txt,
                "cleaned_text": cleaned_texts[i] if i < len(cleaned_texts) else "",
                "sentiment_label": sent.get("label"),
                "sentiment_score": (
                    float(sent["score"]) if sent.get("score") is not None else None
                ),
                "topic_id": (
                    int(topic["topic_id"]) if topic.get("topic_id") is not None else None
                ),
                "topic_prob": (
                    float(topic["topic_prob"])
                    if topic.get("topic_prob") is not None
                    else None
                ),
                "tsne_x": x,
                "tsne_y": y,
                "cluster_label": cluster,
            }
        )
    return pd.DataFrame(rows)
