"""
Feature Extraction Module for PolluAlert
Implements TF-IDF (Term Frequency - Inverse Document Frequency) vectorization.

TF-IDF captures the importance of a word in a document relative to a corpus:
    TF(t,d)  = (Number of times term t appears in document d) / (Total terms in d)
    IDF(t,D) = log(Total documents in D / Number of documents containing t)
    TF-IDF(t,d,D) = TF(t,d) × IDF(t,D)

We use unigrams + bigrams to capture both individual words and two-word phrases:
- Unigrams: "smoke", "chemical", "leak"
- Bigrams: "chemical leak", "breathing problems", "toxic smoke"
"""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Default TF-IDF parameters
TFIDF_PARAMS = {
    'ngram_range': (1, 2),       # Unigrams + Bigrams
    'max_features': 5000,         # Limit vocabulary size
    'min_df': 2,                  # Minimum document frequency
    'max_df': 0.95,               # Maximum document frequency (ignore very common terms)
    'sublinear_tf': True,         # Apply sublinear TF scaling (1 + log(tf))
    'strip_accents': 'unicode',   # Handle accented characters
}

# Default path for saving/loading the vectorizer
DEFAULT_VECTORIZER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'tfidf_vectorizer.pkl'
)


def build_tfidf(corpus, params=None):
    """
    Build a TF-IDF vectorizer from a corpus of documents.
    
    Parameters:
        corpus (list of str): List of preprocessed text documents
        params (dict, optional): Custom TF-IDF parameters
    
    Returns:
        tuple: (tfidf_matrix, vectorizer)
            - tfidf_matrix: sparse matrix of TF-IDF features
            - vectorizer: fitted TfidfVectorizer object
    """
    if params is None:
        params = TFIDF_PARAMS.copy()
    
    vectorizer = TfidfVectorizer(**params)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    return tfidf_matrix, vectorizer


def transform_text(text, vectorizer):
    """
    Transform a single text or list of texts using a fitted vectorizer.
    
    Parameters:
        text (str or list of str): Text(s) to transform
        vectorizer (TfidfVectorizer): Fitted vectorizer
    
    Returns:
        sparse matrix: TF-IDF feature matrix
    """
    if isinstance(text, str):
        text = [text]
    return vectorizer.transform(text)


def save_vectorizer(vectorizer, path=None):
    """Save the fitted TF-IDF vectorizer to disk."""
    if path is None:
        path = DEFAULT_VECTORIZER_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(vectorizer, path)
    print(f"Vectorizer saved to: {path}")


def load_vectorizer(path=None):
    """Load a fitted TF-IDF vectorizer from disk."""
    if path is None:
        path = DEFAULT_VECTORIZER_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vectorizer not found at: {path}")
    vectorizer = joblib.load(path)
    return vectorizer


def get_top_tfidf_terms(text, vectorizer, top_n=10):
    """
    Get the top TF-IDF weighted terms from a text.
    Useful for keyword extraction.
    
    Parameters:
        text (str): Input text (preprocessed)
        vectorizer (TfidfVectorizer): Fitted vectorizer
        top_n (int): Number of top terms to return
    
    Returns:
        list of tuple: [(term, score), ...] sorted by score descending
    """
    tfidf_vector = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    
    # Get non-zero entries
    coo = tfidf_vector.tocoo()
    term_scores = [(feature_names[col], score) for col, score in zip(coo.col, coo.data)]
    
    # Sort by score descending
    term_scores.sort(key=lambda x: x[1], reverse=True)
    
    return term_scores[:top_n]


def get_feature_names(vectorizer):
    """Get the feature names (vocabulary) from a fitted vectorizer."""
    return vectorizer.get_feature_names_out()


# === Demonstration ===
if __name__ == "__main__":
    sample_corpus = [
        "thick black smoke factory highway",
        "chemical smell spreading residential area",
        "river water dark smell bad",
        "garbage dumped near school",
        "chemical leak toxic smell breathing problems",
        "sunny day weather pleasant",
    ]
    
    print("=" * 60)
    print("TF-IDF Feature Extraction Demo")
    print("=" * 60)
    
    tfidf_matrix, vectorizer = build_tfidf(sample_corpus, 
                                            params={'ngram_range': (1, 2), 
                                                    'min_df': 1, 
                                                    'max_features': 100})
    
    print(f"\nCorpus size: {len(sample_corpus)} documents")
    print(f"Vocabulary size: {len(get_feature_names(vectorizer))}")
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
    
    # Show top terms for a test input
    test_text = "chemical leak toxic smell breathing"
    print(f"\nTop TF-IDF terms for: '{test_text}'")
    top_terms = get_top_tfidf_terms(test_text, vectorizer, top_n=5)
    for term, score in top_terms:
        print(f"  {term}: {score:.4f}")
