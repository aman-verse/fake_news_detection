import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from nlp.text_processor import (
    download_nltk_data,
    split_sentences,
    preprocess_text
)

from nlp.vectorizer import NewsVectorizer

download_nltk_data()

text = """
The government announced a new education policy today.
The policy will provide additional financial support to students.
"""

print("\n" + "=" * 60)
print("ORIGINAL TEXT")
print("=" * 60)

print(text)

print("\n" + "=" * 60)
print("SENTENCES")
print("=" * 60)

sentences = split_sentences(text)

for sentence in sentences:
    print("-", sentence)

print("\n" + "=" * 60)
print("PROCESSED TEXT")
print("=" * 60)

processed = preprocess_text(text)

print(processed)

print("\n" + "=" * 60)
print("TF-IDF")
print("=" * 60)

vectorizer = NewsVectorizer()

matrix = vectorizer.fit_transform(
    [processed]
)

print("Shape:", matrix.shape)

print("\n" + "=" * 60)
print("FEATURES")
print("=" * 60)

print(
    vectorizer.get_feature_names()
)
