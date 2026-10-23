# PolluAlert

An academic NLP project that turns a written pollution complaint into a category, severity, possible emergency status, location, keywords, and a structured report.

The app displays alerts locally. It does **not** send SMS, email, or reports to authorities, measure pollution with sensors, or verify incident truth.

## Run on this computer

The dependencies and retrained models were checked using Python 3.13.14 and Streamlit 1.53.1. Open PowerShell:

```powershell
cd "D:\NLP Project\PolluAlert"
python -m streamlit run app.py
```

Open **http://localhost:8501**. Keep the terminal open while using the app. Press **Ctrl+C** to stop it. You can also run `./run.ps1`; it prefers the project's `.venv` when one exists.

## First-time setup on another computer

Use Python 3.11–3.13. These commands use the virtual environment directly, so activating PowerShell scripts is unnecessary.

```powershell
cd "D:\NLP Project\PolluAlert"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m nltk.downloader punkt_tab stopwords wordnet
.\.venv\Scripts\python.exe src/train_model.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Change the folder path if you copied the project elsewhere. Installation and NLP downloads need internet; the app does not download data at startup. Retrain in a new environment because saved scikit-learn models depend on library versions.

For full named-entity recognition, optionally install the English spaCy model:

```powershell
.\.venv\Scripts\python.exe -m spacy download en_core_web_sm
```

If spaCy or its model is unavailable, known-location and domain patterns still work. The sidebar shows the active method. During the screenshot run on 2 October 2026, full spaCy NER loaded successfully on this computer.

## Demo in class

1. Click **Start Analysis** on Home.
2. Choose an example or write an English incident description.
3. Click **Analyze Incident**. Show category, severity, location, confidence, and summary.
4. Expand **View Classification Explanation** to show cleaned text and rule explanations.
5. Click **Correct** or **Incorrect**. Feedback is stored for later review; it does not automatically train the model.
6. Download the analysis as JSON if needed.
7. Open **Analytics Dashboard** to show saved reports, charts, feedback, and model comparisons.

Use [the teacher guide](docs/TEACHER_GUIDE.md) for a speaking script, worked example, and viva questions.

## Project screenshots

Ten actual screenshots of the running app are in [`docs/screenshots/`](docs/screenshots/README.md). Open [`docs/screenshots/index.html`](docs/screenshots/index.html) for the complete gallery. The images show Home, the input form, air/water/noise/waste/chemical/normal results, analytics, and model performance.

The screenshots use six demonstration reports in `data/demo_reports.db`. Your regular history remains in `data/pollualert.db`. To reproduce the demo dashboard, stop any running app on port 8501 and run `./run_demo.ps1`. Normal startup with `python -m streamlit run app.py` uses the regular history.

## Folder organization

```text
PolluAlert/
  app.py                 Streamlit application
  run.ps1                Normal launcher
  run_demo.ps1           Launcher using separate demo history
  requirements.txt       Dependencies
  README.md              Setup and project guide
  .streamlit/            App theme
  src/                   NLP, models, database, dataset utilities
  data/                  Dataset, processed data, local databases
  models/                Trained models and current metrics
  tests/                 Automated checks
  scripts/               Optional report and diagram generators
  notebooks/             Exploratory walkthrough
  docs/                  Teacher guide and academic report
    figures/             Diagrams and evaluation plots
    screenshots/         Ten current app screenshots and gallery
```

Cleanup backup: `../PolluAlert-backups/before-cleanup-2026-10-02.zip`. Generated caches, old logs, an empty data directory, and replaced screenshots were removed from the active project and preserved in the adjacent backup folder. Original reports, training data, saved models, and tests were retained. Optional document tools now live in `scripts/` and use portable project-relative paths.

## How it works

```text
English incident description
    -> cleaning, tokenization, stop-word removal, lemmatization
    -> TF-IDF numbers for individual words and two-word phrases
    -> three classifiers: category, severity, emergency status
    -> keyword checks adjust severity and emergency status
    -> entity/location extraction and template-based summary
    -> Streamlit result, SQLite history, optional user feedback
```

The pipeline uses NLTK, scikit-learn, optional spaCy NER, Streamlit, SQLite, pandas, Matplotlib, and Seaborn. It is conventional machine learning, not an LLM or chatbot.

## Dataset and evaluation

`data/pollution_dataset.csv` contains **430 academic examples**, with nine categories including **Not Pollution**. It is student-curated/synthetic academic data, not a verified real-world monitoring dataset.

- One stratified split provides **344 training rows and 86 test rows** for all three tasks.
- TF-IDF learns vocabulary and IDF values from training rows only.
- Naive Bayes, Logistic Regression, and calibrated Linear SVM are compared.
- Models are selected by **3-fold cross-validation weighted F1 on training data**. TF-IDF is fitted again inside each fold.
- The held-out test set reports performance; it does not select the winner.

Latest results from the retrained artifacts:

| Task | Selected model | Test accuracy | Test weighted F1 |
|---|---|---:|---:|
| Pollution type | Logistic Regression | 76.74% | 0.7679 |
| Severity | Linear SVM | 70.93% | 0.7001 |
| Emergency status | Linear SVM | 83.72% | 0.8187 |

These scores evaluate the ML classifiers before keyword rules. The dataset is small, categories overlap, and wording can strongly affect predictions. Complex negation, sarcasm, unfamiliar vocabulary, and other languages remain limitations. Simple negated phrases are excluded from keyword boosts, but ML can still misunderstand them. Confidence is the pollution-category model's score, not the probability of an actual emergency.

`models/evaluation_results.json` is the source of current metrics. Earlier reports, notebooks, and screenshots in `docs/` may describe an older run; use this README and the teacher guide for the revised version.

## Fixes and improvements

- Results persist across widget reruns; feedback no longer disappears.
- Each analysis submission inserts one report; feedback does not duplicate it.
- Home navigation and sidebar stay synchronized; examples remain editable.
- Blank, punctuation-only, numeric-only, and entirely unknown-vocabulary inputs receive guidance.
- Added JSON download, cleaned-text display, low category-score notice, and visible extraction mode.
- Removed automatic NLTK network downloads at import.
- Model cache updates only after every model loads successfully.
- Keyword checks use phrase boundaries and simple local negation filtering.
- Fixed evaluation file paths and selected emergency model indicator.
- Fixed TF-IDF data leakage and test-set model selection; regenerated models and evaluation plots.

## Test and retrain

```powershell
python -m pytest -q
python src/train_model.py
```

Use `.\.venv\Scripts\python.exe` instead of `python` if using the virtual environment. Restart the app after retraining so cached models reload. Training overwrites generated models and evaluation plots; it does not delete saved reports. UI regression tests use temporary databases, preserving real report history.

## Troubleshooting

| Problem | Action |
|---|---|
| `python` is not recognized | Install Python and reopen the terminal, or use the Python launcher `py`. |
| Missing package | Install requirements with the same Python interpreter used to launch the app. |
| Missing NLTK resource | Run `python -m nltk.downloader punkt_tab stopwords wordnet` once with internet. |
| Models missing or incompatible | Run `python src/train_model.py`, then restart the app. |
| Port 8501 occupied | Add `--server.port 8502` and open `http://localhost:8502`. |
| spaCy cannot load | Use the visible pattern fallback; full NER needs working spaCy and the English model. |

## Main files

| File | Purpose |
|---|---|
| `app.py` | Home, analysis, results, feedback, dashboard |
| `src/preprocessing.py` | Text cleaning and NLTK preprocessing |
| `src/feature_extraction.py` | TF-IDF features |
| `src/train_model.py` | Training, selection, evaluation, plots |
| `src/prediction.py` | Prediction pipeline |
| `src/severity.py` | Keywords, severity rules, summary template |
| `src/entity_extraction.py` | spaCy NER and pattern fallback |
| `src/database.py` | SQLite storage and feedback |
| `data/pollualert.db` | Local saved report history |
| `tests/` | Prediction, database, UI, regression tests |
| `notebooks/PolluAlert_Walkthrough.ipynb` | Earlier exploratory walkthrough |
| `docs/TEACHER_GUIDE.md` | Speaking script, demo, viva answers |

Academic use only. PolluAlert is a preliminary screening tool and does not replace environmental measurements or professional incident assessment.
