"""Train and save MNIST classifiers using the arrays prepared in Week 3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neural_network import MLPClassifier


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WEEK3_DATA = REPOSITORY_ROOT / "week-3" / "data"
MODEL_DIR = REPOSITORY_ROOT / "week-4" / "models"


def load_week3_arrays(data_dir: Path = WEEK3_DATA) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load train/test arrays saved by the Week 3 preprocessing work."""
    processed_path = data_dir / "mnist_processed.npz"
    if processed_path.exists():
        with np.load(processed_path) as arrays:
            required = {"x_train", "x_test", "y_train", "y_test"}
            missing = required.difference(arrays.files)
            if missing:
                raise ValueError(f"{processed_path} is missing arrays: {sorted(missing)}")
            return tuple(arrays[name] for name in ("x_train", "x_test", "y_train", "y_test"))  # type: ignore[return-value]

    separate_names = ("x_train.npy", "x_test.npy", "y_train.npy", "y_test.npy")
    separate_paths = [data_dir / name for name in separate_names]
    if all(path.exists() for path in separate_paths):
        return tuple(np.load(path) for path in separate_paths)  # type: ignore[return-value]

    expected = " or ".join((str(processed_path), ", ".join(separate_names)))
    raise FileNotFoundError(
        "Week 3 processed data was not found. Run week-3/notebooks/mnist_eda.ipynb "
        f"first so that {expected} is available."
    )


def train_models(
    x_train: np.ndarray,
    y_train: np.ndarray,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a linear baseline and a small neural network for comparison."""
    baseline = LogisticRegression(max_iter=1000, solver="lbfgs", random_state=random_state)
    neural_network = MLPClassifier(
        hidden_layer_sizes=(64,),
        learning_rate_init=0.001,
        max_iter=25,
        early_stopping=True,
        random_state=random_state,
    )
    baseline.fit(x_train, y_train)
    neural_network.fit(x_train, y_train)
    return {"baseline": baseline, "neural_network": neural_network}


def evaluate_models(
    models: dict[str, Any],
    x_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, dict[str, Any]]:
    """Return accuracy and a serializable classification report for each model."""
    evaluation: dict[str, dict[str, Any]] = {}
    for name, model in models.items():
        predictions = model.predict(x_test)
        evaluation[name] = {
            "accuracy": float(accuracy_score(y_test, predictions)),
            "classification_report": classification_report(y_test, predictions, output_dict=True),
        }
    return evaluation


def tune_neural_network(
    x_train: np.ndarray,
    y_train: np.ndarray,
    random_state: int = 42,
) -> tuple[MLPClassifier, dict[str, Any]]:
    """Try a few beginner-friendly neural-network settings and keep the best."""
    candidates = [
        {"hidden_layer_sizes": (64,), "learning_rate_init": 0.001},
        {"hidden_layer_sizes": (128,), "learning_rate_init": 0.001},
        {"hidden_layer_sizes": (64,), "learning_rate_init": 0.01},
    ]
    best_model: MLPClassifier | None = None
    best_score = -1.0
    best_params: dict[str, Any] = {}
    validation_size = max(1, int(len(x_train) * 0.1))
    x_fit, x_validation = x_train[:-validation_size], x_train[-validation_size:]
    y_fit, y_validation = y_train[:-validation_size], y_train[-validation_size:]

    for parameters in candidates:
        model = MLPClassifier(
            **parameters,
            max_iter=40,
            early_stopping=True,
            random_state=random_state,
        )
        model.fit(x_fit, y_fit)
        score = float(model.score(x_validation, y_validation))
        if score > best_score:
            best_model, best_score, best_params = model, score, parameters

    if best_model is None:
        raise RuntimeError("No neural-network tuning candidate was trained")

    # Fit the selected settings on all available training data before saving.
    final_model = MLPClassifier(
        **best_params,
        max_iter=40,
        early_stopping=True,
        random_state=random_state,
    )
    final_model.fit(x_train, y_train)
    return final_model, {"validation_accuracy": best_score, "best_params": best_params}


def main() -> None:
    """Train, evaluate, tune, and save all Week 4 model artifacts."""
    x_train, x_test, y_train, y_test = load_week3_arrays()
    x_train = np.asarray(x_train, dtype=np.float32)
    x_test = np.asarray(x_test, dtype=np.float32)
    y_train = np.asarray(y_train)
    y_test = np.asarray(y_test)
    models = train_models(x_train, y_train)
    evaluation = evaluate_models(models, x_test, y_test)
    tuned_model, tuning = tune_neural_network(x_train, y_train)
    tuned_evaluation = evaluate_models({"tuned_neural_network": tuned_model}, x_test, y_test)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(models["baseline"], MODEL_DIR / "baseline_logistic_regression.pkl")
    joblib.dump(models["neural_network"], MODEL_DIR / "neural_network.pkl")
    joblib.dump(tuned_model, MODEL_DIR / "mnist_classifier.pkl")
    summary = {"baseline_and_neural_network": evaluation, "tuning": tuning, "final_model": tuned_evaluation}
    (MODEL_DIR / "training_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Model comparison:")
    for name, result in evaluation.items():
        print(f"  {name}: accuracy={result['accuracy']:.4f}")
    print(f"Tuned neural network: accuracy={tuned_evaluation['tuned_neural_network']['accuracy']:.4f}")
    print(f"Saved final model to {MODEL_DIR / 'mnist_classifier.pkl'}")


if __name__ == "__main__":
    main()
