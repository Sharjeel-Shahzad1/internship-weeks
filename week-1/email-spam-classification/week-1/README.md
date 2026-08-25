# Email Spam Classification

Week 1 of an internship project focused on email spam classification using a Kaggle dataset such as the SMS Spam Collection or an email spam dataset with `label` and `text/message` columns.

## What is implemented in Week 1

- Dataset loading from a local CSV in `data/`
- Basic exploratory data analysis in `notebooks/spam_eda.ipynb`
- Cleaning helpers in `src/preprocess.py`
- Text preprocessing with NLTK stopwords and tokenization
- Saving a cleaned dataset to `data/spam_cleaned.csv`

## Dataset source

Use a Kaggle dataset such as:

- SMS Spam Collection
- Email Spam Classification

If you cannot download directly in this workspace, download the CSV from Kaggle and place it in `data/spam_raw.csv`.
The code is written to work with a CSV that has columns similar to `label` and `text` or `message`.

## Project structure

- `data/` - raw and cleaned dataset files
- `notebooks/spam_eda.ipynb` - exploratory data analysis
- `src/preprocess.py` - reusable cleaning and preprocessing functions
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download the NLTK resources if needed:

```bash
python -m nltk.downloader stopwords punkt
```

4. Place the raw Kaggle CSV at `data/spam_raw.csv`.

## Run the preprocessing script

```bash
python src/preprocess.py
```

This reads the raw CSV, removes null and duplicate rows, converts labels to binary, cleans the text, and saves the result to `data/spam_cleaned.csv`.

## Week 2

Feature extraction and model training will be added in Week 2.
