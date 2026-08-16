from __future__ import annotations

import re
from pathlib import Path
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "spam_raw.csv"
DEFAULT_CLEAN_PATH = PROJECT_ROOT / "data" / "spam_cleaned.csv"

_LABEL_COLUMNS = ("label", "category", "class", "target", "v1")
_TEXT_COLUMNS = ("message", "text", "email", "content", "v2")


def ensure_nltk_resources() -> None:
    """Download the NLTK resources required for preprocessing if they are missing."""
    for resource, package in (("corpora/stopwords", "stopwords"), ("tokenizers/punkt", "punkt")):
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package, quiet=True)


def load_dataset(csv_path: str | Path = DEFAULT_RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def resolve_columns(df: pd.DataFrame, label_col: str | None = None, text_col: str | None = None) -> tuple[str, str]:
    if label_col is None:
        label_col = next((column for column in _LABEL_COLUMNS if column in df.columns), None)
    if text_col is None:
        text_col = next((column for column in _TEXT_COLUMNS if column in df.columns), None)

    if label_col is None or text_col is None:
        raise ValueError(
            "Could not infer label/text columns. Expected columns similar to "
            f"{_LABEL_COLUMNS} and {_TEXT_COLUMNS}."
        )

    return label_col, text_col


def remove_nulls_and_duplicates(
    df: pd.DataFrame,
    label_col: str | None = None,
    text_col: str | None = None,
) -> pd.DataFrame:
    label_col, text_col = resolve_columns(df, label_col=label_col, text_col=text_col)
    cleaned = df.dropna(subset=[label_col, text_col]).copy()
    cleaned = cleaned.drop_duplicates(subset=[label_col, text_col])
    return cleaned.reset_index(drop=True)


def convert_labels_to_binary(df: pd.DataFrame, label_col: str | None = None) -> pd.DataFrame:
    label_col, _ = resolve_columns(df, label_col=label_col)
    normalized = df.copy()
    values = normalized[label_col].astype(str).str.strip().str.lower()
    spam_values = {"spam", "1", "yes", "true", "positive"}
    normalized["label_binary"] = values.apply(lambda value: 1 if value in spam_values else 0)
    return normalized


def clean_text(text: object) -> str:
    ensure_nltk_resources()
    if pd.isna(text):
        return ""

    normalized = str(text).lower()
    normalized = re.sub(r"[^a-z\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    tokens = word_tokenize(normalized)
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)


def preprocess_text_column(
    df: pd.DataFrame,
    text_col: str | None = None,
    output_col: str = "clean_text",
) -> pd.DataFrame:
    _, text_col = resolve_columns(df, text_col=text_col)
    processed = df.copy()
    processed[output_col] = processed[text_col].apply(clean_text)
    return processed


def preprocess_dataset(
    df: pd.DataFrame,
    label_col: str | None = None,
    text_col: str | None = None,
    output_col: str = "clean_text",
) -> pd.DataFrame:
    label_col, text_col = resolve_columns(df, label_col=label_col, text_col=text_col)
    cleaned = remove_nulls_and_duplicates(df, label_col=label_col, text_col=text_col)
    cleaned = convert_labels_to_binary(cleaned, label_col=label_col)
    cleaned = preprocess_text_column(cleaned, text_col=text_col, output_col=output_col)
    return cleaned


def save_cleaned_dataset(df: pd.DataFrame, output_path: str | Path = DEFAULT_CLEAN_PATH) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def run_pipeline(
    raw_path: str | Path = DEFAULT_RAW_PATH,
    clean_path: str | Path = DEFAULT_CLEAN_PATH,
    label_col: str | None = None,
    text_col: str | None = None,
) -> Path:
    dataset = load_dataset(raw_path)
    processed = preprocess_dataset(dataset, label_col=label_col, text_col=text_col)
    return save_cleaned_dataset(processed, clean_path)


def main() -> None:
    output_path = run_pipeline()
    print(f"Saved cleaned dataset to {output_path}")


if __name__ == "__main__":
    main()
