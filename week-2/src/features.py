"""Feature extraction utilities for the Week 2 spam classifier."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

VectorizerKind = Literal["bow", "tfidf"]


def load_cleaned_dataset(csv_path: str | Path) -> pd.DataFrame:
    """Load Week 1 output and validate the columns needed for modeling."""
    dataset = pd.read_csv(csv_path)
    required = {"clean_text", "label_binary"}
    missing = required.difference(dataset.columns)
    if missing:
        raise ValueError(
            f"Dataset is missing {sorted(missing)}. Expected Week 1 columns: "
            "clean_text and label_binary."
        )
    dataset = dataset.dropna(subset=["clean_text", "label_binary"]).copy()
    dataset["clean_text"] = dataset["clean_text"].astype(str)
    dataset["label_binary"] = dataset["label_binary"].astype(int)
    if dataset["label_binary"].nunique() < 2:
        raise ValueError("The dataset must contain both ham (0) and spam (1) labels.")
    return dataset.reset_index(drop=True)


def create_vectorizer(kind: VectorizerKind = "tfidf", **kwargs: object):
    """Create a scikit-learn vectorizer without fitting it."""
    if kind == "bow":
        return CountVectorizer(**kwargs)
    if kind == "tfidf":
        return TfidfVectorizer(**kwargs)
    raise ValueError("kind must be either 'bow' or 'tfidf'")


def fit_transform_texts(
    texts: pd.Series | list[str],
    kind: VectorizerKind = "tfidf",
    vectorizer_path: str | Path | None = None,
    **kwargs: object,
):
    """Fit a vectorizer, transform texts, and optionally save the fitted vectorizer."""
    vectorizer = create_vectorizer(kind, **kwargs)
    features = vectorizer.fit_transform(texts)
    if vectorizer_path is not None:
        output_path = Path(vectorizer_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(vectorizer, output_path)
    return features, vectorizer


def transform_texts(texts: pd.Series | list[str], vectorizer):
    """Transform new texts with an already-fitted vectorizer."""
    return vectorizer.transform(texts)


def save_vectorizer(vectorizer, output_path: str | Path) -> Path:
    """Persist a fitted vectorizer for later inference."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, output_path)
    return output_path


def load_vectorizer(input_path: str | Path):
    """Load a previously saved fitted vectorizer."""
    return joblib.load(input_path)
