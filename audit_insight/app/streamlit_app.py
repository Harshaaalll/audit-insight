"""Streamlit front-end for the Audit Insight NLP pipeline.

Launch with::

    streamlit run audit_insight/app/streamlit_app.py
"""

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from audit_insight.clustering import cluster_documents, compute_tfidf_vectors, reduce_and_tsne
from audit_insight.config import N_CLUSTERS, NUM_TOPICS
from audit_insight.preprocessing import preprocess_texts
from audit_insight.sentiment import sentiment_roberta
from audit_insight.topics import get_topic_keywords, topic_modeling_lda
from audit_insight.utils import assemble_result_dataframe

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Text-to-Insight: Audit NLP",
    page_icon="🔍",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar — tuneable parameters
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Pipeline Parameters")
num_topics: int = st.sidebar.slider(
    "Number of LDA topics",
    min_value=2,
    max_value=20,
    value=NUM_TOPICS,
)
num_clusters: int = st.sidebar.slider(
    "Number of clusters (KMeans)",
    min_value=2,
    max_value=20,
    value=N_CLUSTERS,
)

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("🔍 Text-to-Insight — Audit NLP Pipeline")
st.markdown(
    "Upload a CSV containing a **text** column and run the full NLP "
    "pipeline (preprocessing → sentiment → topics → clustering)."
)

uploaded = st.file_uploader("Upload a CSV with a 'text' column", type=["csv"])

input_path: str | None = None
if uploaded is not None:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp.write(uploaded.read())
    tmp.flush()
    tmp.close()
    input_path = tmp.name
    st.info(f"📄 File uploaded: **{uploaded.name}**")

run_btn = st.button("🚀 Run Pipeline")

if run_btn and input_path:
    with st.spinner(
        "Running pipeline — this can take a few minutes "
        "(model downloads on first run)…"
    ):
        try:
            df = pd.read_csv(input_path)
            texts = df["text"].astype(str).tolist()

            # 1. Preprocess
            cleaned = preprocess_texts(texts)

            # 2. Sentiment
            sentiments = sentiment_roberta(cleaned)

            # 3. Topics
            lda, corpus, dictionary, docs_topics = topic_modeling_lda(
                cleaned, num_topics=num_topics,
            )

            # 4. TF-IDF + t-SNE
            vect, X = compute_tfidf_vectors(cleaned)
            X_emb = reduce_and_tsne(X)

            # 5. Clustering
            cluster_labels = cluster_documents(X_emb, n_clusters=num_clusters)

            # 6. Assemble
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

            st.success("✅ Pipeline finished!")

            # Results table
            st.subheader("Results Preview")
            st.dataframe(result_df.head(50), use_container_width=True)

            # Topic keywords
            st.subheader("Topic Keywords")
            keywords = get_topic_keywords(lda, num_words=10)
            for tid, words in keywords.items():
                st.write(f"**Topic {tid}:** {', '.join(words)}")

            # Download
            csv_bytes = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Results CSV",
                csv_bytes,
                file_name="audit_insight_results.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"Error running pipeline: {exc}")
elif run_btn:
    st.warning("Please upload a CSV file first.")
