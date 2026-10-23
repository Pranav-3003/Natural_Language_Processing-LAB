"""
Prediction Module for PolluAlert
Provides the complete prediction pipeline:
    Input text → Preprocessing → TF-IDF → ML Classification → Severity/Emergency Adjustment
    → Entity Extraction → Keyword Extraction → Summary Generation → Output
"""

import os
import sys
import joblib
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.preprocessing import preprocess_text
from src.feature_extraction import load_vectorizer, get_top_tfidf_terms
from src.entity_extraction import extract_all_entities, extract_location
from src.severity import (
    adjust_severity, adjust_emergency,
    generate_suggested_action, generate_incident_summary,
    check_severity_keywords, check_emergency_keywords
)

# Model paths
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')

# Global model cache
_models = {}


def load_models():
    """Load all trained models and vectorizer into memory."""
    global _models
    
    if _models:
        return _models
    
    try:
        loaded = {'vectorizer': load_vectorizer()}
        loaded['pollution_classifier'] = joblib.load(
            os.path.join(MODELS_DIR, 'pollution_classifier.pkl')
        )
        loaded['severity_classifier'] = joblib.load(
            os.path.join(MODELS_DIR, 'severity_classifier.pkl')
        )
        loaded['emergency_classifier'] = joblib.load(
            os.path.join(MODELS_DIR, 'emergency_classifier.pkl')
        )
        _models = loaded
        print("All models loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading models: {e}")
        print("Please run 'python src/train_model.py' first to train the models.")
        raise
    
    return _models


def extract_keywords(text, vectorizer, top_n=8):
    """
    Extract important keywords from text using TF-IDF scores.
    
    Parameters:
        text (str): Preprocessed text
        vectorizer: Fitted TF-IDF vectorizer
        top_n (int): Number of top keywords to return
    
    Returns:
        list of str: Top keywords
    """
    top_terms = get_top_tfidf_terms(text, vectorizer, top_n=top_n)
    keywords = [term for term, score in top_terms if score > 0.05]
    return keywords if keywords else ['general observation']


def get_confidence(model, features):
    """
    Get prediction confidence from model.
    
    Parameters:
        model: Trained classifier
        features: TF-IDF feature vector
    
    Returns:
        float: Confidence score (0-1)
    """
    try:
        proba = model.predict_proba(features)
        return float(np.max(proba))
    except AttributeError:
        # Model doesn't support predict_proba
        return 0.0


def predict(text):
    """
    Complete prediction pipeline for a given text.
    
    Parameters:
        text (str): Raw input text describing a pollution incident or observation
    
    Returns:
        dict: Complete analysis results containing:
            - original_text: The raw input
            - cleaned_text: Preprocessed text
            - pollution_type: Classified pollution category
            - severity: Final severity level (LOW/MEDIUM/HIGH/NONE)
            - emergency_status: Final emergency classification
            - location: Extracted location
            - keywords: Important extracted terms
            - entities: Extracted named entities
            - summary: Structured incident summary
            - suggested_action: Recommended next step
            - confidence: Model confidence score
            - severity_explanation: Why this severity was assigned
            - emergency_explanation: Why this emergency status was assigned
            - indicators: Emergency indicator keywords found
    """
    # Step 1: Preprocess
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text.strip():
        return {
            'original_text': text,
            'cleaned_text': '',
            'pollution_type': 'Not Pollution',
            'severity': 'NONE',
            'emergency_status': 'NORMAL',
            'location': 'Not identified',
            'keywords': [],
            'entities': {},
            'summary': 'Unable to analyse: text was empty after preprocessing.',
            'suggested_action': 'No action required.',
            'confidence': 0.0,
            'severity_explanation': 'Text was empty after preprocessing.',
            'emergency_explanation': 'Text was empty after preprocessing.',
            'indicators': []
        }
    
    # Step 2: TF-IDF transform
    models = load_models()
    features = models['vectorizer'].transform([cleaned_text])
    if features.nnz == 0:
        raise ValueError("No familiar terms found. Please describe the incident in English with more detail.")
    
    # Step 3: ML Classification
    pollution_type = models['pollution_classifier'].predict(features)[0]
    ml_severity = models['severity_classifier'].predict(features)[0]
    ml_emergency = models['emergency_classifier'].predict(features)[0]
    
    # Get confidence from pollution classifier (primary task)
    confidence = get_confidence(models['pollution_classifier'], features)
    
    # Step 4: Severity and Emergency Adjustment (rule-based boost)
    final_severity, severity_explanation = adjust_severity(ml_severity, text)
    final_emergency, emergency_explanation, indicators = adjust_emergency(
        ml_emergency, text, final_severity
    )
    
    # Step 5: Entity Extraction
    entities = extract_all_entities(text)
    location = entities['location']
    
    # Step 6: Keyword Extraction
    keywords = extract_keywords(cleaned_text, models['vectorizer'])
    
    # Add emergency indicator keywords if found
    _, severity_kw = check_severity_keywords(text)
    _, emergency_kw = check_emergency_keywords(text)
    all_indicator_keywords = list(dict.fromkeys(keywords + severity_kw[:3] + emergency_kw[:3]))
    
    # Step 7: Generate Summary
    summary = generate_incident_summary(
        pollution_type, final_severity, final_emergency, location, all_indicator_keywords
    )
    
    # Step 8: Suggested Action
    suggested_action = generate_suggested_action(final_severity, final_emergency)
    
    return {
        'original_text': text,
        'cleaned_text': cleaned_text,
        'pollution_type': pollution_type,
        'severity': final_severity,
        'emergency_status': final_emergency,
        'location': location,
        'keywords': all_indicator_keywords,
        'entities': {
            'locations': entities.get('all_locations', []),
            'organizations': entities.get('organizations', []),
            'pollution_sources': entities.get('pollution_sources', []),
            'water_bodies': entities.get('water_bodies', []),
            'affected_groups': entities.get('affected_groups', []),
            'area_types': entities.get('area_types', [])
        },
        'summary': summary,
        'suggested_action': suggested_action,
        'confidence': round(confidence, 4),
        'severity_explanation': severity_explanation,
        'emergency_explanation': emergency_explanation,
        'indicators': indicators
    }


def predict_batch(texts):
    """
    Predict for multiple texts.
    
    Parameters:
        texts (list of str): List of input texts
    
    Returns:
        list of dict: List of prediction results
    """
    return [predict(text) for text in texts]


# === Demonstration ===
if __name__ == "__main__":
    test_inputs = [
        "There is thick black smoke coming from a factory near the highway.",
        "A strong chemical smell is spreading around the residential area.",
        "The river water has become dark and smells very bad.",
        "A large amount of garbage has been dumped near the school.",
        "A chemical leak has caused a toxic smell and people are having breathing problems.",
        "Today is a sunny day.",
        "There is a strange smell near the river.",
    ]
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          PolluAlert - Prediction Pipeline Demo          ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    for text in test_inputs:
        print(f"\n{'=' * 60}")
        print(f"INPUT: {text}")
        print('=' * 60)
        
        result = predict(text)
        
        print(f"  Pollution Type:    {result['pollution_type']}")
        print(f"  Severity:          {result['severity']}")
        print(f"  Emergency Status:  {result['emergency_status']}")
        print(f"  Location:          {result['location']}")
        print(f"  Keywords:          {', '.join(result['keywords'][:5])}")
        print(f"  Confidence:        {result['confidence']:.2%}")
        print(f"\n  Summary:")
        for line in result['summary'].split('\n'):
            print(f"    {line}")
