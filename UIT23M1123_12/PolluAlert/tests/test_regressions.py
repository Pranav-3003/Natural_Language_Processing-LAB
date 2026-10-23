"""Regression tests for state, input handling, and keyword matching."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src import database, prediction
from src.preprocessing import preprocess_text
from src.severity import check_emergency_keywords, check_severity_keywords


@pytest.mark.parametrize('text', ['!!! ... ---', '123 456', 'https://example.com'])
def test_nonlinguistic_input_is_empty(text):
    assert preprocess_text(text) == ''


def test_empty_prediction_does_not_need_models(monkeypatch):
    def unexpected_load():
        pytest.fail('Empty input must not try to load models')
    monkeypatch.setattr(prediction, 'load_models', unexpected_load)
    assert prediction.predict('')['confidence'] == 0


def test_failed_model_load_can_be_retried(monkeypatch):
    monkeypatch.setattr(prediction, '_models', {})
    monkeypatch.setattr(prediction, 'load_vectorizer', lambda: object())

    def missing(path):
        raise FileNotFoundError(path)

    monkeypatch.setattr(prediction.joblib, 'load', missing)
    for _ in range(2):
        with pytest.raises(FileNotFoundError):
            prediction.load_models()
        assert not prediction._models


@pytest.mark.parametrize('text', [
    'The fireplace is decorative.',
    'There is no chemical leak.',
    'The smell is not toxic.',
    "There isn't a gas leak.",
])
def test_keywords_do_not_match_substrings_or_simple_negation(text):
    assert check_emergency_keywords(text) == (False, [])
    assert check_severity_keywords(text) == (None, [])


def test_positive_indicator_after_negation_is_preserved():
    emergency, matches = check_emergency_keywords('There is no smoke, but a chemical leak was reported.')
    assert emergency and 'chemical leak' in matches


def test_positive_indicator_is_not_suppressed_by_not_only():
    assert check_emergency_keywords('Not only toxic fumes but a gas leak was reported.')[0]


def test_unknown_vocabulary_requests_better_input():
    with pytest.raises(ValueError, match='No familiar terms'):
        prediction.predict('zxqvbnm qwertyuiop')


def test_bare_database_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    database.init_db('reports.db')
    assert (tmp_path / 'reports.db').exists()


def test_test_only_words_never_enter_training_vocabulary(monkeypatch):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from src import train_model

    df = pd.DataFrame({
        'cleaned_text': ['smoke factory'] * 10 + ['river sewage'] * 10,
        'pollution_type': ['Air Pollution'] * 10 + ['Water Pollution'] * 10,
    })
    _, test_rows = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['pollution_type']
    )
    df.loc[test_rows.index, 'cleaned_text'] += ' heldoutmarker'
    monkeypatch.setattr(train_model, 'save_vectorizer', lambda vectorizer: None)
    train_rows, heldout, X_train, X_test, vectorizer = train_model.prepare_training_split(df)
    assert set(train_rows.index).isdisjoint(heldout.index)
    assert 'heldoutmarker' not in vectorizer.vocabulary_
    assert X_train.shape[1] == X_test.shape[1]
    assert len(train_rows) == 16 and len(heldout) == 4


@pytest.fixture
def app(tmp_path, monkeypatch):
    # UI tests must never modify the user's actual report history.
    monkeypatch.setattr(database, 'DEFAULT_DB_PATH', str(tmp_path / 'reports.db'))
    path = Path(__file__).resolve().parents[1] / 'app.py'
    at = AppTest.from_file(str(path), default_timeout=30).run()
    assert not at.exception
    return at


def button(app, label):
    return next(item for item in app.button if item.label == label)


def test_navigation_feedback_and_results_survive_reruns(app):
    button(app, 'Start Analysis').click().run()
    assert app.radio[0].value == 'Pollution Analysis'
    app.text_area[0].set_value('The river water has become dark and smells very bad.').run()
    button(app, 'Analyze Incident').click().run()
    assert not app.exception
    assert database.get_report_stats()['total_reports'] == 1
    report_id = app.session_state['last_report_id']
    button(app, 'Correct').click().run()
    assert not app.exception
    assert database.get_report_by_id(report_id)['user_feedback'] == 'correct'
    assert database.get_report_stats()['total_reports'] == 1
    button(app, 'Incorrect').click().run()
    assert database.get_report_by_id(report_id)['user_feedback'] == 'incorrect'
    app.radio[0].set_value('Analytics Dashboard').run()
    assert not app.exception
    app.radio[0].set_value('Pollution Analysis').run()
    assert app.session_state['last_report_id'] == report_id
    assert any(item.label == 'Correct' for item in app.button)
    assert database.get_report_stats()['total_reports'] == 1


def test_examples_are_editable_and_bad_input_is_not_saved(app):
    app.radio[0].set_value('Pollution Analysis').run()
    example = app.selectbox[0].options[1]
    app.selectbox[0].select(example).run()
    assert app.text_area[0].value == example
    app.text_area[0].set_value('!!!').run()
    button(app, 'Analyze Incident').click().run()
    assert not app.exception
    assert app.warning
    assert database.get_report_stats()['total_reports'] == 0


def test_empty_dashboard_can_show_model_performance(app):
    app.radio[0].set_value('Analytics Dashboard').run()
    assert not app.exception
    assert len(app.dataframe) == 3
    assert any(' *' in value for value in app.dataframe[-1].value['Model'])
