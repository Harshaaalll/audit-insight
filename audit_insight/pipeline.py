"""End-to-end NLP pipeline orchestrator.

Chains every processing step (preprocessing → sentiment → topics →
TF-IDF → t-SNE → clustering → result assembly) and persists the
output to CSV.

Can be used as a library function or invoked directly from the command
line::

    python -m audit_insight.pipeline --input data/sample_docs.csv --output data/results.csv
"""

import argparse
import logging
from typing import Optional

import pandas as pd

from audit_insight.clustering import cluster_documents, compute_tfidf_vectors, reduce_and_tsne
from audit_insight.config import N_CLUSTERS, NUM_TOPICS
from audit_insight.preprocessing import preprocess_texts
from audit_insight.sentiment import sentiment_roberta
from audit_insight.topics import topic_modeling_lda
from audit_insight.utils import assemble_result_dataframe, load_documents_from_csv

logger = logging.getLogger(__name__)


def run_pipeline(
    input_csv: str,
    output_csv: str,
    text_col: str = "text",
    num_topics: Optional[int] = None,
    num_clusters: Optional[int] = None,
) -> pd.DataFrame:
    """Execute the full Audit Insight NLP pipeline.

    Parameters
    ----------
    input_csv:
        Path to the input CSV containing raw documents.
    output_csv:
        Path where the result CSV will be written.
    text_col:
        Name of the column in the input CSV that holds document text.
    num_topics:
        Number of LDA topics.  Uses the package default when *None*.
    num_clusters:
        Number of KMeans clusters.  Uses the package default when *None*.

    Returns
    -------
    pd.DataFrame
        The assembled results DataFrame (also saved to *output_csv*).
    """
    num_topics = num_topics if num_topics is not None else NUM_TOPICS
    num_clusters = num_clusters if num_clusters is not None else N_CLUSTERS

    # 1. Load documents
    logger.info("Loading documents from %s …", input_csv)
    df = load_documents_from_csv(input_csv, text_col=text_col)
    texts = df["text"].astype(str).tolist()

    # 2. Preprocess
    logger.info("Preprocessing %d documents …", len(texts))
    cleaned = preprocess_texts(texts)

    # 3. Sentiment analysis (RoBERTa)
    logger.info("Running sentiment analysis …")
    sentiments = sentiment_roberta(cleaned)

    # 4. Topic modelling (LDA)
    logger.info("Training LDA model with %d topics …", num_topics)
    lda, corpus, dictionary, docs_topics = topic_modeling_lda(
        cleaned, num_topics=num_topics,
    )

    # 5. TF-IDF + t-SNE
    logger.info("Computing TF-IDF vectors and t-SNE embedding …")
    _vect, X = compute_tfidf_vectors(cleaned)
    X_emb = reduce_and_tsne(X)

    # 6. Clustering
    logger.info("Clustering documents into %d clusters …", num_clusters)
    cluster_labels = cluster_documents(X_emb, n_clusters=num_clusters)

    # 7. Assemble results
    logger.info("Assembling result DataFrame …")
    result_df = assemble_result_dataframe(
        original_texts=texts,
        cleaned_texts=cleaned,
        sentiment_results=sentiments,
        docs_topics=docs_topics,
        tsne_coords=X_emb,
        cluster_labels=cluster_labels,
        dictionary=dictionary,
        lda_model=lda,
    )

    # 8. Persist
    result_df.to_csv(output_csv, index=False)
    logger.info("Results written to %s", output_csv)

    return result_df


def _cli() -> None:
    """Parse CLI arguments and run the pipeline."""
    parser = argparse.ArgumentParser(
        description="Audit Insight — run the full NLP pipeline on a CSV.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV path with a 'text' column",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV path for results",
    )
    parser.add_argument(
        "--text-col",
        default="text",
        help="Name of the text column (default: 'text')",
    )
    parser.add_argument(
        "--num-topics",
        type=int,
        default=None,
        help=f"Number of LDA topics (default: {NUM_TOPICS})",
    )
    parser.add_argument(
        "--num-clusters",
        type=int,
        default=None,
        help=f"Number of KMeans clusters (default: {N_CLUSTERS})",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(name)s  %(levelname)s  %(message)s",
    )

    run_pipeline(
        input_csv=args.input,
        output_csv=args.output,
        text_col=args.text_col,
        num_topics=args.num_topics,
        num_clusters=args.num_clusters,
    )


if __name__ == "__main__":
    _cli()
