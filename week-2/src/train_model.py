"""Train, compare, tune, and save the Week 2 spam classifier."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB

from features import create_vectorizer, load_cleaned_dataset

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = ROOT / "data" / "spam_cleaned.csv"
DEFAULT_MODEL_PATH = ROOT / "models" / "spam_classifier.pkl"


def metric_summary(y_true, predictions) -> dict[str, float]:
    return {
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "f1": f1_score(y_true, predictions, zero_division=0),
    }


def compare_models(dataset: pd.DataFrame, random_state: int = 42):
    """Compare Naive Bayes and Logistic Regression with BoW and TF-IDF."""
    texts = dataset["clean_text"]
    labels = dataset["label_binary"]
    train_texts, test_texts, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=random_state, stratify=labels
    )
    results = []
    fitted = {}
    for feature_name in ("bow", "tfidf"):
        vectorizer = create_vectorizer(feature_name)
        x_train = vectorizer.fit_transform(train_texts)
        x_test = vectorizer.transform(test_texts)
        for model_name, model in (
            ("Naive Bayes", MultinomialNB()),
            ("Logistic Regression", LogisticRegression(max_iter=1000, random_state=random_state)),
        ):
            model.fit(x_train, y_train)
            predictions = model.predict(x_test)
            results.append(
                {"features": feature_name, "model": model_name, **metric_summary(y_test, predictions)}
            )
            fitted[(feature_name, model_name)] = (vectorizer, model)
    return pd.DataFrame(results).sort_values("f1", ascending=False).reset_index(drop=True), fitted, (y_test, test_texts)


def tune_and_save(
    dataset: pd.DataFrame,
    output_path: str | Path = DEFAULT_MODEL_PATH,
    random_state: int = 42,
) -> tuple[dict, pd.DataFrame]:
    """Tune the strongest representation/model family and save an inference bundle."""
    results, fitted, (y_test, _) = compare_models(dataset, random_state=random_state)
    best = results.iloc[0]
    vectorizer, _ = fitted[(best["features"], best["model"])]

    train_texts, test_texts, y_train, y_test = train_test_split(
        dataset["clean_text"], dataset["label_binary"], test_size=0.2,
        random_state=random_state, stratify=dataset["label_binary"]
    )
    x_train = vectorizer.transform(train_texts)
    if best["model"] == "Naive Bayes":
        search = GridSearchCV(MultinomialNB(), {"alpha": [0.1, 0.5, 1.0, 2.0]}, cv=5, scoring="f1")
    else:
        search = GridSearchCV(
            LogisticRegression(max_iter=2000, random_state=random_state),
            {"C": [0.1, 1.0, 10.0]}, cv=5, scoring="f1",
        )
    search.fit(x_train, y_train)
    final_model = search.best_estimator_
    tuned_predictions = final_model.predict(vectorizer.transform(test_texts))
    tuned_metrics = {
        "features": best["features"],
        "model": best["model"],
        **metric_summary(y_test, tuned_predictions),
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "vectorizer": vectorizer,
        "model": final_model,
        "features": best["features"],
        "model_name": best["model"],
        "best_params": search.best_params_,
        "holdout_metrics": tuned_metrics,
    }
    joblib.dump(artifact, output_path)
    return artifact, results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_MODEL_PATH)
    args = parser.parse_args()
    dataset = load_cleaned_dataset(args.data)
    artifact, results = tune_and_save(dataset, args.output)
    print(results.to_string(index=False))
    print(f"Saved {artifact['model_name']} with {artifact['features']} features to {args.output}")


if __name__ == "__main__":
    main()
