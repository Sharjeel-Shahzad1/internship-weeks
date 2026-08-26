# Week 4: MNIST Model Training and Month 1 Report

Week 4 completes Task 2, MNIST Digit Recognition. It reuses the pre-processed arrays from `week-3/data`, compares a Logistic Regression baseline with a small scikit-learn neural network (`MLPClassifier`), evaluates both models, tunes the stronger model, and demonstrates predictions on held-out digit images.

## Contents

- `src/train_mnist_model.py`: loads Week 3 arrays, trains the baseline and neural network, tunes the stronger model, and saves artifacts.
- `notebooks/mnist_evaluation.ipynb`: evaluates accuracy, classification reports, confusion matrices, tuning results, and sample predictions.
- `models/`: saved model artifacts created by the training script.
- `reports/Month1_Report.docx`: combined Task 1 and Task 2 report with editable placeholders.

## Dataset and expected input

Download MNIST from Kaggle as described in `week-3/README.md`, run the Week 3 preprocessing notebook, and confirm that `week-3/data/mnist_processed.npz` exists. The Week 4 script reuses its `x_train`, `x_test`, `y_train`, and `y_test` arrays and does not reprocess the images. It also accepts the separate Week 3 files `x_train.npy`, `x_test.npy`, `y_train.npy`, and `y_test.npy` if those are used instead.

## Run end to end

From the repository root:

```text
pip install -r week-4/requirements.txt
python week-4/src/train_mnist_model.py
jupyter notebook week-4/notebooks/mnist_evaluation.ipynb
```

The script writes `baseline_logistic_regression.pkl`, `neural_network.pkl`, `mnist_classifier.pkl`, and `training_summary.json` into `week-4/models/`. The final model is saved as `mnist_classifier.pkl` because this project uses scikit-learn rather than Keras. Run the notebook cells in order to create evaluation plots and sample prediction outputs for the report.

The strongest model and accuracy are printed by the script and notebook after the real MNIST files are available. The report intentionally leaves result values as fill-in placeholders until the actual dataset is trained.

## Month 1 report naming

Before submission, rename the report using the convention `Name_Domain_Month1.docx`, replacing `Name` and `Domain` with the required internship details. The front page contains placeholders for full name, internship domain, email address, and phone number.

## Scope

Weeks 1 and 2 completed Task 1 (Email Spam Classification). Week 3 began Task 2 with acquisition, exploration, visualization, and preprocessing. Week 4 completes Task 2 and combines both tasks into the Month 1 submission. Model training and evaluation are the focus here; later internship work can extend the models and deployment.
