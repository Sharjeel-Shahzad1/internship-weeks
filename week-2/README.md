# Week 2: Email Spam Classification

This folder contains the modeling stage of the internship project. It uses the cleaned output from Week 1 and keeps all Week 2 code, data, notebooks, and model artifacts self-contained.

## Pipeline

1. Week 1 loads the Kaggle labeled dataset, removes nulls and duplicates, converts labels to `label_binary` (`0` ham, `1` spam), and creates `clean_text`.
2. Copy Week 1's `spam_cleaned.csv` into `week-2/data/spam_cleaned.csv`.
3. `src/features.py` fits either Bag-of-Words (`CountVectorizer`) or TF-IDF (`TfidfVectorizer`) and can save the fitted vectorizer.
4. `src/train_model.py` makes a stratified 80/20 split, compares Naive Bayes and Logistic Regression with both feature representations, tunes the strongest combination with `GridSearchCV`, and saves a joblib artifact.
5. The notebook reports accuracy, precision, recall, F1-score, confusion matrices, and sample predictions.

## Setup

From the repository root:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r week-2/requirements.txt
```

Copy the cleaned data without changing Week 1:

```powershell
Copy-Item week-1/email-spam-classification/week-1/data/spam_cleaned.csv week-2/data/spam_cleaned.csv
```

The CSV must contain `clean_text` and `label_binary` columns. The current workspace does not include the Kaggle CSV, so the model artifact and measured accuracy will be produced once that input is supplied.

## Train the model

```bash
cd week-2
python src/train_model.py
```

This creates `models/spam_classifier.pkl`. The artifact contains the fitted vectorizer, final classifier, selected feature type, tuned parameters, and holdout metrics. It is deliberately saved as one bundle so inference uses exactly the features seen during training.

## Run the notebook

Open `notebooks/model_evaluation.ipynb` in VS Code or Jupyter and run all cells. The notebook also saves `models/spam_classifier.pkl` and demonstrates predictions for both spam and ham messages.

## Final model and accuracy

The final model is selected by holdout F1-score across Naive Bayes and Logistic Regression with both BoW and TF-IDF. Its exact model name and accuracy are data-dependent and are printed by the notebook and training script after the Week 1 cleaned dataset is supplied; no accuracy is claimed here because that dataset is not present in the current workspace.
