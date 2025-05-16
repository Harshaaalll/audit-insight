"""LDA topic modelling via Gensim.

Provides functions to train an LDA model on preprocessed texts and to
extract the top keywords for each discovered topic.
"""

from typing import Any, Dict, List, Optional, Tuple

from gensim import corpora, models

from audit_insight.config import LDA_PASSES, NUM_TOPICS


def topic_modeling_lda(
    cleaned_texts: List[str],
    num_topics: Optional[int] = None,
    passes: Optional[int] = None,
) -> Tuple[models.LdaModel, List[Any], corpora.Dictionary, List[Dict[str, Any]]]:
    """Build an LDA topic model from pre-processed texts.

    Parameters
    ----------
    cleaned_texts:
        Space-joined lemma strings (output of
        :pyfunc:`audit_insight.preprocessing.preprocess_texts`).
    num_topics:
        Number of latent topics.  Defaults to
        :pydata:`audit_insight.config.NUM_TOPICS`.
    passes:
        Number of training passes over the corpus.  Defaults to
        :pydata:`audit_insight.config.LDA_PASSES`.

    Returns
    -------
    tuple
        ``(lda_model, corpus, dictionary, docs_topics)`` where
        *docs_topics* is a list of dicts with keys ``topic_id`` (int)
        and ``topic_prob`` (float) indicating each document's dominant
        topic.
    """
    num_topics = num_topics if num_topics is not None else NUM_TOPICS
    passes = passes if passes is not None else LDA_PASSES

    tokenized: List[List[str]] = [txt.split() for txt in cleaned_texts]
    dictionary = corpora.Dictionary(tokenized)

    # Filter extremes to reduce noise (must happen before building corpus)
    dictionary.filter_extremes(no_below=2, no_above=0.8, keep_n=5000)

    corpus = [dictionary.doc2bow(text) for text in tokenized]

    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=passes,
        random_state=42,
    )

    # Dominant topic per document
    docs_topics: List[Dict[str, Any]] = []
    for bow in corpus:
        doc_topics = lda.get_document_topics(bow, minimum_probability=0.0)
        doc_topics = sorted(doc_topics, key=lambda x: -x[1])
        dominant = doc_topics[0]
        docs_topics.append(
            {"topic_id": dominant[0], "topic_prob": float(dominant[1])}
        )

    return lda, corpus, dictionary, docs_topics


def get_topic_keywords(
    lda_model: models.LdaModel,
    num_words: int = 10,
) -> Dict[int, List[str]]:
    """Return the top keywords for every topic in *lda_model*.

    Parameters
    ----------
    lda_model:
        A trained :class:`gensim.models.LdaModel`.
    num_words:
        How many keywords to return per topic.

    Returns
    -------
    Dict[int, List[str]]
        Mapping from ``topic_id`` to a list of keyword strings ordered
        by descending relevance.
    """
    topic_keywords: Dict[int, List[str]] = {}
    for topic_id in range(lda_model.num_topics):
        # show_topic returns list of (word, weight)
        pairs = lda_model.show_topic(topic_id, topn=num_words)
        topic_keywords[topic_id] = [word for word, _weight in pairs]
    return topic_keywords
