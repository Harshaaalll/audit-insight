"""Tests for :mod:`audit_insight.preprocessing`."""

import pytest

from audit_insight.preprocessing import init_spacy, preprocess_texts


# Initialise spaCy once for the whole module (expensive)
@pytest.fixture(scope="module")
def nlp():
    """Return a shared spaCy Language object."""
    return init_spacy()


class TestPreprocessTexts:
    """Unit tests for ``preprocess_texts``."""

    def test_lowercases_text(self, nlp) -> None:
        """Output should contain only lowercase lemmas."""
        result = preprocess_texts(["The QUICK Brown Fox"], nlp=nlp)
        assert len(result) == 1
        for word in result[0].split():
            assert word == word.lower(), f"'{word}' is not lowercase"

    def test_removes_stop_words(self, nlp) -> None:
        """Common stop words should be stripped from the output."""
        result = preprocess_texts(["This is a very simple test"], nlp=nlp)
        assert len(result) == 1
        tokens = result[0].split()
        # 'this', 'is', 'a', 'very' are stop words in spaCy
        for stop in ("this", "is", "a", "very"):
            assert stop not in tokens, f"Stop word '{stop}' was not removed"

    def test_lemmatises_tokens(self, nlp) -> None:
        """Inflected words should be reduced to their lemma."""
        result = preprocess_texts(["The dogs were running quickly"], nlp=nlp)
        tokens = result[0].split()
        # 'dogs' → 'dog', 'running' → 'run'
        assert "dog" in tokens, "'dogs' was not lemmatised to 'dog'"
        assert "run" in tokens, "'running' was not lemmatised to 'run'"

    def test_handles_empty_input(self, nlp) -> None:
        """An empty list should return an empty list."""
        assert preprocess_texts([], nlp=nlp) == []

    def test_handles_empty_string(self, nlp) -> None:
        """A list with an empty string should return a list with one
        empty string (all tokens filtered out)."""
        result = preprocess_texts([""], nlp=nlp)
        assert result == [""]

    def test_removes_punctuation_and_numbers(self, nlp) -> None:
        """Punctuation marks and numeric tokens should be removed."""
        result = preprocess_texts(["Price: $100, quantity 5!"], nlp=nlp)
        tokens = result[0].split()
        for bad in (":", "$", "100", ",", "5", "!"):
            assert bad not in tokens, f"'{bad}' was not removed"

    def test_single_char_lemmas_removed(self, nlp) -> None:
        """Lemmas of length ≤ 1 should be filtered out."""
        result = preprocess_texts(["I am a person"], nlp=nlp)
        tokens = result[0].split()
        for tok in tokens:
            assert len(tok) > 1, f"Single-char token '{tok}' not removed"
