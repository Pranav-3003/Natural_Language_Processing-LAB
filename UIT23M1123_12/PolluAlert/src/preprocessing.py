"""
Text Preprocessing Module for PolluAlert
Implements the NLP preprocessing pipeline:
- Lowercase conversion
- URL removal
- Special character handling
- Whitespace normalization
- Tokenization
- Stop-word removal (with negation preservation)
- Lemmatization
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (run once)
def download_nltk_data():
    """Download required NLTK resources."""
    resources = ['punkt_tab', 'stopwords', 'wordnet']
    for resource in resources:
        if not nltk.download(resource, quiet=True):
            raise RuntimeError(f"Could not download NLTK resource: {resource}")

# Negation words to preserve during stop-word removal.
# Removing these can change the meaning of a sentence.
# Example: "not dangerous" should NOT become "dangerous" after stop-word removal.
NEGATION_WORDS = {
    'not', 'no', 'nor', 'neither', 'never', 'nobody',
    'nothing', 'nowhere', 'hardly', 'barely', 'scarcely',
    "don't", "doesn't", "didn't", "won't", "wouldn't",
    "shouldn't", "couldn't", "isn't", "aren't", "wasn't",
    "weren't", "hasn't", "haven't", "hadn't", "cannot",
    "can't", "mustn't", "needn't"
}

# Custom stop words: standard English stop words minus negation words
try:
    _standard_stopwords = set(stopwords.words('english'))
except LookupError as exc:
    raise RuntimeError(
        "Missing NLTK data. Run: python -m nltk.downloader punkt_tab stopwords wordnet"
    ) from exc
CUSTOM_STOPWORDS = _standard_stopwords - NEGATION_WORDS


def to_lowercase(text):
    """Convert text to lowercase."""
    if not isinstance(text, str):
        return ""
    return text.lower()


def remove_urls(text):
    """Remove URLs from text."""
    # Match http/https URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    return text


def remove_special_characters(text):
    """
    Remove special characters while preserving:
    - Alphanumeric characters
    - Spaces
    - Basic punctuation useful for NLP (periods, commas, hyphens)
    - Apostrophes (for contractions like don't, can't)
    """
    # Keep letters, digits, spaces, periods, commas, hyphens, apostrophes
    text = re.sub(r"[^a-zA-Z0-9\s.,'\-]", ' ', text)
    return text


def normalize_whitespace(text):
    """Normalize multiple whitespace characters to single space and strip."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text):
    """Tokenize text into words using NLTK word_tokenize."""
    try:
        tokens = word_tokenize(text)
    except LookupError:
        # Fallback to simple split if tokenizer fails
        tokens = text.split()
    return tokens


def remove_stopwords(tokens):
    """
    Remove stop words while preserving negation words.
    
    This is important because removing negation words can change meaning:
    - "not dangerous" -> "dangerous" (WRONG - meaning is reversed)
    - "no pollution" -> "pollution" (WRONG - meaning is reversed)
    
    By preserving negation words, we maintain the original intent of the text.
    """
    return [token for token in tokens if token not in CUSTOM_STOPWORDS]


def lemmatize(tokens):
    """
    Lemmatize tokens using WordNet lemmatizer.
    Reduces words to their base form:
    - "polluting" -> "pollute"
    - "factories" -> "factory"
    - "breathing" -> "breathing" (kept as is when contextually important)
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for token in tokens:
        # Try verb lemmatization first, then noun
        lemma = lemmatizer.lemmatize(token, pos='v')
        if lemma == token:
            lemma = lemmatizer.lemmatize(token, pos='n')
        lemmatized.append(lemma)
    return lemmatized


def preprocess_text(text):
    """
    Complete preprocessing pipeline.
    
    Pipeline steps:
    1. Lowercase conversion
    2. URL removal
    3. Special character handling
    4. Whitespace normalization
    5. Tokenization
    6. Stop-word removal (with negation preservation)
    7. Lemmatization
    8. Rejoin tokens into cleaned text
    
    Parameters:
        text (str): Raw input text
    
    Returns:
        str: Cleaned and preprocessed text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Step 1: Lowercase
    text = to_lowercase(text)
    
    # Step 2: Remove URLs
    text = remove_urls(text)
    
    # Step 3: Remove special characters
    text = remove_special_characters(text)
    
    # Step 4: Normalize whitespace
    text = normalize_whitespace(text)
    
    # Step 5: Tokenize
    tokens = tokenize(text)
    
    # Step 6: Remove stop words (preserving negation)
    tokens = [token for token in tokens if any(char.isalpha() for char in token)]
    tokens = remove_stopwords(tokens)
    
    # Step 7: Lemmatize
    tokens = lemmatize(tokens)
    
    # Step 8: Rejoin
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text


def preprocess_for_display(text):
    """
    Light preprocessing for display purposes (no lemmatization/stopword removal).
    Used when showing cleaned text to the user.
    """
    if not text or not isinstance(text, str):
        return ""
    text = to_lowercase(text)
    text = remove_urls(text)
    text = remove_special_characters(text)
    text = normalize_whitespace(text)
    return text


# === Demonstration / Testing ===
if __name__ == "__main__":
    test_texts = [
        "There is thick black smoke coming from a factory near the highway!",
        "A strong chemical smell is spreading around the residential area.",
        "The water is NOT contaminated, it is perfectly safe.",
        "Today is a sunny day and the weather is pleasant.",
        "Check https://pollution.gov.in for more details about the chemical leak!!!",
        "Not dangerous at all, the smell is from the bakery.",
    ]
    
    print("=" * 60)
    print("PolluAlert Preprocessing Pipeline Demo")
    print("=" * 60)
    
    for text in test_texts:
        cleaned = preprocess_text(text)
        print(f"\nOriginal:    {text}")
        print(f"Preprocessed: {cleaned}")
        print("-" * 60)
    
    # Demonstrate negation preservation
    print("\n=== Negation Preservation Demo ===")
    neg_text = "The area is not polluted and there is no danger."
    cleaned_neg = preprocess_text(neg_text)
    print(f"Original: {neg_text}")
    print(f"Cleaned:  {cleaned_neg}")
    print("Note: 'not' and 'no' are preserved to maintain meaning.")
