"""Text preprocessing utilities using spaCy.

Provides helpers to initialise a spaCy language model and to clean /
normalise raw document texts (lowercasing, lemmatisation, stop-word and
punctuation removal).
"""

from typing import List, Optional

import spacy
from spacy.language import Language

from audit_insight.config import SPACY_MODEL


def init_spacy(model_name: Optional[str] = None) -> Language:
    """Load (or download then load) a spaCy language model.

    Parameters
    ----------
    model_name:
        Name of the spaCy model.  Defaults to
        :pydata:`audit_insight.config.SPACY_MODEL`.

    Returns
    -------
    Language
        The loaded spaCy ``Language`` pipeline object.
    """
    model_name = model_name or SPACY_MODEL
    try:
        nlp = spacy.load(model_name)
    except OSError:
        from spacy.cli import download  # noqa: WPS433 (nested import OK)
        download(model_name)
        nlp = spacy.load(model_name)
    return nlp


def preprocess_texts(
    texts: List[str],
    nlp: Optional[Language] = None,
) -> List[str]:
    """Clean and normalise a list of raw texts.

    Processing steps applied to each document:

    1. Tokenisation via spaCy
    2. Lowercasing
    3. Lemmatisation
    4. Removal of stop words, punctuation, and numeric tokens
    5. Removal of single-character lemmas

    Parameters
    ----------
    texts:
        Raw document strings.
    nlp:
        A pre-loaded spaCy ``Language`` object.  If *None* the default
        model from :pyfunc:`init_spacy` is loaded automatically.

    Returns
    -------
    List[str]
        Cleaned texts where each entry is a space-joined sequence of
        lemmas.
    """
    if nlp is None:
        nlp = init_spacy()

    cleaned: List[str] = []
    for doc in nlp.pipe(texts, disable=["ner"]):
        tokens: List[str] = []
        for tok in doc:
            if tok.is_stop or tok.is_punct or tok.like_num:
                continue
            lemma = tok.lemma_.strip().lower()
            if len(lemma) <= 1:
                continue
            tokens.append(lemma)
        cleaned.append(" ".join(tokens))
    return cleaned
