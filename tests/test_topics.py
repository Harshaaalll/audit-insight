"""Tests for :mod:`audit_insight.topics`."""

import pytest

from audit_insight.topics import get_topic_keywords, topic_modeling_lda


# 12 audit-themed texts (with duplicates to ensure LDA has enough data)
_SAMPLE_TEXTS = [
    "internal control weakness risk assessment audit",
    "revenue recognition policy compliance review audit",
    "accounts payable reconciliation discrepancy found audit",
    "risk assessment financial reporting processes audit",
    "segregation duties violation procurement fraud audit",
    "inventory count variance materiality threshold audit",
    "management override internal controls detected audit",
    "audit committee reviewed quarterly financial statements",
    "internal control weakness risk assessment audit",
    "revenue recognition policy compliance review audit",
    "accounts payable reconciliation discrepancy found audit",
    "risk assessment financial reporting processes audit",
]


class TestTopicModelingLda:
    """Unit tests for ``topic_modeling_lda``."""

    def test_returns_four_element_tuple(self) -> None:
        """Return value should be a 4-tuple of
        (lda_model, corpus, dictionary, docs_topics)."""
        result = topic_modeling_lda(_SAMPLE_TEXTS, num_topics=2, passes=1)
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_docs_topics_length_matches_input(self) -> None:
        """Length of docs_topics should equal the number of input
        texts."""
        _, _, _, docs_topics = topic_modeling_lda(
            _SAMPLE_TEXTS, num_topics=2, passes=1,
        )
        assert len(docs_topics) == len(_SAMPLE_TEXTS)

    def test_docs_topics_has_required_keys(self) -> None:
        """Each docs_topics entry should have 'topic_id' and
        'topic_prob' keys."""
        _, _, _, docs_topics = topic_modeling_lda(
            _SAMPLE_TEXTS, num_topics=2, passes=1,
        )
        for entry in docs_topics:
            assert "topic_id" in entry, "Missing 'topic_id' key"
            assert "topic_prob" in entry, "Missing 'topic_prob' key"

    def test_topic_prob_is_valid(self) -> None:
        """topic_prob should be a float between 0 and 1 (inclusive)."""
        _, _, _, docs_topics = topic_modeling_lda(
            _SAMPLE_TEXTS, num_topics=2, passes=1,
        )
        for entry in docs_topics:
            assert 0.0 <= entry["topic_prob"] <= 1.0, (
                f"topic_prob {entry['topic_prob']} out of range [0, 1]"
            )

    def test_custom_num_topics(self) -> None:
        """Passing num_topics=3 should produce a model with 3 topics."""
        lda, _, _, _ = topic_modeling_lda(
            _SAMPLE_TEXTS, num_topics=3, passes=1,
        )
        assert lda.num_topics == 3


class TestGetTopicKeywords:
    """Unit tests for ``get_topic_keywords``."""

    def test_get_topic_keywords_returns_dict(self) -> None:
        """Output should be a dict mapping int topic IDs to lists of
        keyword strings."""
        lda, _, _, _ = topic_modeling_lda(
            _SAMPLE_TEXTS, num_topics=2, passes=1,
        )
        keywords = get_topic_keywords(lda, num_words=5)
        assert isinstance(keywords, dict)
        for topic_id, words in keywords.items():
            assert isinstance(topic_id, int)
            assert isinstance(words, list)
            assert all(isinstance(w, str) for w in words)
