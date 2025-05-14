"""Sentiment analysis using a HuggingFace RoBERTa model.

Wraps the ``transformers`` pipeline so callers get back human-readable
sentiment labels (negative / neutral / positive) instead of the raw
LABEL_0 / LABEL_1 / LABEL_2 tags.
"""

from typing import Any, Dict, List, Optional

from transformers import pipeline as hf_pipeline

from audit_insight.config import LABEL_MAP, ROBERTA_MODEL


def sentiment_roberta(
    texts: List[str],
    model_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Run sentiment analysis on a list of texts.

    Parameters
    ----------
    texts:
        Documents (or cleaned texts) to analyse.
    model_name:
        Hugging Face model identifier.  Defaults to
        :pydata:`audit_insight.config.ROBERTA_MODEL`.

    Returns
    -------
    List[Dict[str, Any]]
        Each dict contains:

        * ``label`` – human-readable sentiment string
          (``"negative"`` / ``"neutral"`` / ``"positive"``).
        * ``score`` – model confidence as a float.
    """
    model_name = model_name or ROBERTA_MODEL

    nlp_sent = hf_pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
    )
    raw_results: List[Dict[str, Any]] = nlp_sent(texts, truncation=True)

    # Map LABEL_0/1/2 → negative/neutral/positive
    mapped_results: List[Dict[str, Any]] = []
    for entry in raw_results:
        raw_label: str = entry.get("label", "")
        mapped_results.append(
            {
                "label": LABEL_MAP.get(raw_label, raw_label),
                "score": entry.get("score"),
            }
        )
    return mapped_results
