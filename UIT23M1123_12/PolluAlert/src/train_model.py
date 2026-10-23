"""
Model Training Module for PolluAlert
Trains and evaluates three classifiers for each classification task:
    Task A: Pollution Type Classification (9 classes including 'Not Pollution')
    Task B: Severity Classification (LOW / MEDIUM / HIGH / NONE)
    Task C: Emergency Status Classification (NORMAL / POLLUTION REPORT / POTENTIAL EMERGENCY)

Models:
    1. Multinomial Naive Bayes
    2. Logistic Regression
    3. Linear SVM (LinearSVC)

Evaluation: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
"""

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.preprocessing import preprocess_text
from src.feature_extraction import build_tfidf, save_vectorizer, TFIDF_PARAMS

warnings.filterwarnings('ignore')

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
DATA_PATH = os.path.join(PROJECT_DIR, 'data', 'pollution_dataset.csv')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')
FIGURES_DIR = os.path.join(PROJECT_DIR, 'docs', 'figures')

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_dataset():
    """Load and validate the pollution dataset."""
    print("=" * 60)
    print("STEP 1: Loading Dataset")
    print("=" * 60)
    
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
    
    print(f"Total records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Check for missing values
    missing = df.isnull().sum()
    print(f"\nMissing values:\n{missing}")
    
    # Check for duplicates
    duplicates = df['text'].duplicated().sum()
    print(f"\nDuplicate texts: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates(subset='text', keep='first')
        print(f"After removing duplicates: {len(df)} records")
    
    # Class distribution
    print("\n--- Pollution Type Distribution ---")
    print(df['pollution_type'].value_counts())
    
    print("\n--- Severity Distribution ---")
    print(df['severity'].value_counts())
    
    print("\n--- Emergency Status Distribution ---")
    print(df['emergency_status'].value_counts())
    
    return df


def preprocess_dataset(df):
    """Apply text preprocessing to all records."""
    print("\n" + "=" * 60)
    print("STEP 2: Preprocessing Dataset")
    print("=" * 60)
    
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    
    # Show examples
    print("\nPreprocessing examples:")
    for i in range(min(3, len(df))):
        print(f"  Original:  {df.iloc[i]['text'][:80]}...")
        print(f"  Cleaned:   {df.iloc[i]['cleaned_text'][:80]}...")
        print()
    
    # Check for empty cleaned texts
    empty_count = (df['cleaned_text'].str.len() == 0).sum()
    if empty_count > 0:
        print(f"Warning: {empty_count} texts became empty after preprocessing")
        df = df[df['cleaned_text'].str.len() > 0]
    
    # Save processed data
    processed_path = os.path.join(PROJECT_DIR, 'data', 'processed', 'cleaned_dataset.csv')
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"Saved processed dataset to: {processed_path}")
    
    return df


def extract_features(df):
    """Extract TF-IDF features from cleaned text."""
    print("\n" + "=" * 60)
    print("STEP 3: TF-IDF Feature Extraction")
    print("=" * 60)
    
    corpus = df['cleaned_text'].tolist()
    tfidf_matrix, vectorizer = build_tfidf(corpus)
    
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    
    # Save vectorizer
    save_vectorizer(vectorizer)
    
    return tfidf_matrix, vectorizer


def train_and_evaluate_models(X_train, X_test, y_train, y_test, task_name, training_texts):
    """
    Train three models and evaluate them.
    
    Returns:
        dict: Results with metrics for each model
        best_model: The best performing model
        best_model_name: Name of the best model
    """
    print(f"\n{'=' * 60}")
    print(f"Training Models for: {task_name}")
    print(f"{'=' * 60}")
    print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")
    print(f"Classes: {sorted(set(y_train))}")
    
    models = {
        'Naive Bayes': MultinomialNB(alpha=1.0),
        'Logistic Regression': LogisticRegression(
            max_iter=1000, 
            C=1.0, 
            random_state=42,
            class_weight='balanced'
        ),
        'Linear SVM': CalibratedClassifierCV(
            LinearSVC(max_iter=2000, random_state=42, class_weight='balanced'),
            cv=3
        )
    }
    
    results = {}
    best_f1 = -1
    best_model = None
    best_model_name = None
    
    for name, model in models.items():
        print(f"\n--- {name} ---")
        # Select models using training folds only. Each fold learns its own vocabulary.
        cv_pipeline = make_pipeline(TfidfVectorizer(**TFIDF_PARAMS), clone(model))
        cv_scores = cross_val_score(
            cv_pipeline, training_texts, y_train, scoring='f1_weighted',
            cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        )
        cv_f1 = float(cv_scores.mean())
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, zero_division=0)
        
        results[name] = {
            'cv_f1_score': round(cv_f1, 4),
            'accuracy': round(acc, 4),
            'precision': round(prec, 4),
            'recall': round(rec, 4),
            'f1_score': round(f1, 4),
            'confusion_matrix': cm.tolist(),
            'classification_report': report
        }
        
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"\n{report}")
        
        # The held-out test scores never determine model selection.
        if cv_f1 > best_f1:
            best_f1 = cv_f1
            best_model = model
            best_model_name = name
    
    print(f"\nBest model for {task_name}: {best_model_name} (training CV F1: {best_f1:.4f})")
    
    return results, best_model, best_model_name


def generate_visualizations(all_results, df):
    """Generate and save all visualization figures."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    print(f"\n{'=' * 60}")
    print("Generating Visualizations")
    print(f"{'=' * 60}")
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("husl")
    
    # --- Figure 1: Dataset - Pollution Type Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    type_counts = df['pollution_type'].value_counts()
    bars = ax.barh(type_counts.index, type_counts.values, color=sns.color_palette("husl", len(type_counts)))
    ax.set_xlabel('Number of Records')
    ax.set_title('Dataset: Pollution Type Distribution')
    for bar, val in zip(bars, type_counts.values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                str(val), va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'pollution_type_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: pollution_type_distribution.png")
    
    # --- Figure 2: Severity Distribution ---
    fig, ax = plt.subplots(figsize=(8, 6))
    sev_counts = df['severity'].value_counts()
    colors = {'LOW': '#4CAF50', 'MEDIUM': '#FF9800', 'HIGH': '#F44336', 'NONE': '#9E9E9E'}
    sev_colors = [colors.get(s, '#666') for s in sev_counts.index]
    wedges, texts, autotexts = ax.pie(sev_counts.values, labels=sev_counts.index, 
                                       autopct='%1.1f%%', colors=sev_colors, startangle=90)
    ax.set_title('Dataset: Severity Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'severity_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: severity_distribution.png")
    
    # --- Figure 3: Emergency Status Distribution ---
    fig, ax = plt.subplots(figsize=(8, 6))
    em_counts = df['emergency_status'].value_counts()
    em_colors = {'NORMAL': '#4CAF50', 'POLLUTION REPORT': '#FF9800', 'POTENTIAL EMERGENCY': '#F44336'}
    em_c = [em_colors.get(e, '#666') for e in em_counts.index]
    ax.bar(em_counts.index, em_counts.values, color=em_c)
    ax.set_ylabel('Number of Records')
    ax.set_title('Dataset: Emergency Status Distribution')
    for i, v in enumerate(em_counts.values):
        ax.text(i, v + 1, str(v), ha='center', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'emergency_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: emergency_distribution.png")
    
    # --- Figure 4: Model Comparison Charts ---
    for task_name, task_results in all_results.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        model_names = list(task_results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        x = np.arange(len(model_names))
        width = 0.2
        
        for i, metric in enumerate(metrics):
            values = [task_results[m][metric] for m in model_names]
            bars = ax.bar(x + i * width, values, width, label=metric.replace('_', ' ').title())
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
                        f'{val:.3f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Model')
        ax.set_ylabel('Score')
        ax.set_title(f'Model Comparison: {task_name}')
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(model_names)
        ax.legend(loc='lower right')
        ax.set_ylim(0, 1.15)
        plt.tight_layout()
        
        safe_name = task_name.lower().replace(' ', '_').replace('/', '_')
        plt.savefig(os.path.join(FIGURES_DIR, f'model_comparison_{safe_name}.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Saved: model_comparison_{safe_name}.png")
    
    # --- Figure 5: Confusion Matrices ---
    for task_name, task_results in all_results.items():
        for model_name, metrics in task_results.items():
            cm = np.array(metrics['confusion_matrix'])
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_title(f'Confusion Matrix: {model_name}\n({task_name})')
            ax.set_ylabel('Actual')
            ax.set_xlabel('Predicted')
            plt.tight_layout()
            
            safe_name = f"{task_name}_{model_name}".lower().replace(' ', '_').replace('/', '_')
            plt.savefig(os.path.join(FIGURES_DIR, f'confusion_matrix_{safe_name}.png'), dpi=150, bbox_inches='tight')
            plt.close()
    print("  Saved: confusion matrix figures")
    
    # --- Figure 6: Source Type Distribution ---
    fig, ax = plt.subplots(figsize=(8, 6))
    src_counts = df['source_type'].value_counts()
    ax.bar(src_counts.index, src_counts.values, color=sns.color_palette("Set2", len(src_counts)))
    ax.set_ylabel('Number of Records')
    ax.set_title('Dataset: Source Type Distribution')
    ax.tick_params(axis='x', labelrotation=15)
    for i, v in enumerate(src_counts.values):
        ax.text(i, v + 1, str(v), ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'source_type_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: source_type_distribution.png")


def prepare_training_split(df):
    """Keep test rows out of TF-IDF fitting and share one split across all tasks."""
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['pollution_type']
    )
    X_train, vectorizer = extract_features(train_df)
    X_test = vectorizer.transform(test_df['cleaned_text'])
    return train_df, test_df, X_train, X_test, vectorizer


def main():
    """Main training pipeline."""
    print("============================================================")
    print("          PolluAlert - Model Training Pipeline             ")
    print("============================================================\n")
    
    # Step 1: Load dataset
    df = load_dataset()
    
    # Step 2: Preprocess
    df = preprocess_dataset(df)
    
    # Split rows before learning vocabulary or IDF. All tasks share this split.
    train_df, test_df, X_train, X_test, vectorizer = prepare_training_split(df)
    training_texts = train_df['cleaned_text'].tolist()
    
    # Step 4: Train/Test Split
    print(f"\n{'=' * 60}")
    print("STEP 4: Train/Test Split (80/20)")
    print(f"{'=' * 60}")
    
    all_results = {}
    best_models = {}
    
    # === Task A: Pollution Type Classification ===
    y_train, y_test = train_df['pollution_type'].values, test_df['pollution_type'].values
    print(f"\nPollution Type - Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    
    results_type, best_type_model, best_type_name = train_and_evaluate_models(
        X_train, X_test, y_train, y_test, "Pollution Type", training_texts
    )
    all_results['Pollution Type'] = results_type
    best_models['pollution_type'] = (best_type_model, best_type_name)
    
    # === Task B: Severity Classification ===
    X_train_s, X_test_s = X_train, X_test
    y_train_s, y_test_s = train_df['severity'].values, test_df['severity'].values
    print(f"\nSeverity - Train: {X_train_s.shape[0]}, Test: {X_test_s.shape[0]}")
    
    results_sev, best_sev_model, best_sev_name = train_and_evaluate_models(
        X_train_s, X_test_s, y_train_s, y_test_s, "Severity", training_texts
    )
    all_results['Severity'] = results_sev
    best_models['severity'] = (best_sev_model, best_sev_name)
    
    # === Task C: Emergency Status Classification ===
    X_train_e, X_test_e = X_train, X_test
    y_train_e, y_test_e = train_df['emergency_status'].values, test_df['emergency_status'].values
    print(f"\nEmergency Status - Train: {X_train_e.shape[0]}, Test: {X_test_e.shape[0]}")
    
    results_em, best_em_model, best_em_name = train_and_evaluate_models(
        X_train_e, X_test_e, y_train_e, y_test_e, "Emergency Status", training_texts
    )
    all_results['Emergency Status'] = results_em
    best_models['emergency'] = (best_em_model, best_em_name)
    
    # Step 5: Save best models
    print(f"\n{'=' * 60}")
    print("STEP 5: Saving Best Models")
    print(f"{'=' * 60}")
    
    model_paths = {
        'pollution_classifier': os.path.join(MODELS_DIR, 'pollution_classifier.pkl'),
        'severity_classifier': os.path.join(MODELS_DIR, 'severity_classifier.pkl'),
        'emergency_classifier': os.path.join(MODELS_DIR, 'emergency_classifier.pkl'),
    }
    
    joblib.dump(best_models['pollution_type'][0], model_paths['pollution_classifier'])
    print(f"Saved pollution classifier ({best_models['pollution_type'][1]}): {model_paths['pollution_classifier']}")
    
    joblib.dump(best_models['severity'][0], model_paths['severity_classifier'])
    print(f"Saved severity classifier ({best_models['severity'][1]}): {model_paths['severity_classifier']}")
    
    joblib.dump(best_models['emergency'][0], model_paths['emergency_classifier'])
    print(f"Saved emergency classifier ({best_models['emergency'][1]}): {model_paths['emergency_classifier']}")
    
    # Step 6: Save evaluation results
    print(f"\n{'=' * 60}")
    print("STEP 6: Saving Evaluation Results")
    print(f"{'=' * 60}")
    
    eval_results = {
        'dataset_info': {
            'total_records': len(df),
            'train_test_split': '80/20',
            'random_state': 42,
            'training_records': len(train_df),
            'test_records': len(test_df),
            'vectorizer_fit': 'Training data only',
            'model_selection': '3-fold training cross-validation, weighted F1; TF-IDF fitted within each fold'
        },
        'best_models': {
            'pollution_type': best_models['pollution_type'][1],
            'severity': best_models['severity'][1],
            'emergency': best_models['emergency'][1]
        },
        'results': {}
    }
    
    for task_name, task_results in all_results.items():
        eval_results['results'][task_name] = {}
        for model_name, metrics in task_results.items():
            eval_results['results'][task_name][model_name] = {
                'cv_f1_score': metrics['cv_f1_score'],
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1_score': metrics['f1_score']
            }
    
    eval_path = os.path.join(MODELS_DIR, 'evaluation_results.json')
    with open(eval_path, 'w') as f:
        json.dump(eval_results, f, indent=2)
    print(f"Saved evaluation results to: {eval_path}")
    
    # Step 7: Generate visualizations
    generate_visualizations(all_results, df)
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("TRAINING COMPLETE - SUMMARY")
    print(f"{'=' * 60}")
    print(f"\nDataset: {len(df)} records")
    print(f"\nBest Models Selected:")
    for task, (model, name) in best_models.items():
        task_key = {'pollution_type': 'Pollution Type', 'severity': 'Severity', 'emergency': 'Emergency Status'}[task]
        f1 = all_results[task_key][name]['f1_score']
        print(f"  {task_key}: {name} (F1: {f1:.4f})")
    
    print(f"\nModel Comparison Tables:")
    for task_name, task_results in all_results.items():
        print(f"\n  {task_name}:")
        print(f"  {'Model':<25} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
        print(f"  {'-'*65}")
        for model_name, metrics in task_results.items():
            print(f"  {model_name:<25} {metrics['accuracy']:>10.4f} {metrics['precision']:>10.4f} {metrics['recall']:>10.4f} {metrics['f1_score']:>10.4f}")
    
    print(f"\nAll models and artifacts saved to: {MODELS_DIR}")
    print(f"Figures saved to: {FIGURES_DIR}")
    print("\n[DONE] Training pipeline complete!")
    
    return all_results, best_models


if __name__ == "__main__":
    main()
