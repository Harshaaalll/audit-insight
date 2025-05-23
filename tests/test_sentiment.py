"""Tests for :mod:`audit_insight.sentiment`."""

from unittest.mock import MagicMock, patch

import pytest

from audit_insight.sentiment import sentiment_roberta


class TestSentimentRoberta:
    """Unit tests for ``sentiment_roberta``.

    The HuggingFace pipeline is mocked to avoid downloading the
    ~500 MB RoBERTa model in CI.
    """

    @patch("audit_insight.sentiment.hf_pipeline")
    def test_maps_label_0_to_negative(self, mock_pipeline: MagicMock) -> None:
        """LABEL_0 from the model should be mapped to 'negative'."""
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "LABEL_0", "score": 0.95}]
        mock_pipeline.return_value = mock_pipe

        results = sentiment_roberta(["terrible audit findings"])
        assert results[0]["label"] == "negative"
        assert results[0]["score"] == 0.95

    @patch("audit_insight.sentiment.hf_pipeline")
    def test_maps_label_1_to_neutral(self, mock_pipeline: MagicMock) -> None:
        """LABEL_1 from the model should be mapped to 'neutral'."""
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "LABEL_1", "score": 0.80}]
        mock_pipeline.return_value = mock_pipe

        results = sentiment_roberta(["the audit was performed"])
        assert results[0]["label"] == "neutral"
        assert results[0]["score"] == 0.80

    @patch("audit_insight.sentiment.hf_pipeline")
    def test_maps_label_2_to_positive(self, mock_pipeline: MagicMock) -> None:
        """LABEL_2 from the model should be mapped to 'positive'."""
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "LABEL_2", "score": 0.91}]
        mock_pipeline.return_value = mock_pipe

        results = sentiment_roberta(["excellent compliance record"])
        assert results[0]["label"] == "positive"
        assert results[0]["score"] == 0.91

    @patch("audit_insight.sentiment.hf_pipeline")
    def test_returns_list_of_dicts(self, mock_pipeline: MagicMock) -> None:
        """Output should be a list of dicts each containing 'label'
        and 'score' keys."""
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "LABEL_0", "score": 0.88}]
        mock_pipeline.return_value = mock_pipe

        results = sentiment_roberta(["audit risk is high"])
        assert isinstance(results, list)
        assert len(results) == 1
        assert isinstance(results[0], dict)
        assert "label" in results[0]
        assert "score" in results[0]

    @patch("audit_insight.sentiment.hf_pipeline")
    def test_handles_multiple_texts(self, mock_pipeline: MagicMock) -> None:
        """Multiple input texts should each be mapped correctly."""
        mock_pipe = MagicMock()
        mock_pipe.return_value = [
            {"label": "LABEL_0", "score": 0.90},
            {"label": "LABEL_1", "score": 0.75},
            {"label": "LABEL_2", "score": 0.85},
        ]
        mock_pipeline.return_value = mock_pipe

        texts = [
            "poor internal controls",
            "routine audit procedure",
            "outstanding compliance",
        ]
        results = sentiment_roberta(texts)

        assert len(results) == 3
        assert results[0]["label"] == "negative"
        assert results[1]["label"] == "neutral"
        assert results[2]["label"] == "positive"
