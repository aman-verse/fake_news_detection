import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def download_nltk_data():

    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")

def split_sentences(text):

    return nltk.sent_tokenize(text)

def tokenize_text(text):

    return re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

def preprocess_tokens(text):

    stop_words = set(stopwords.words("english"))

    lemmatizer = WordNetLemmatizer()

    tokens = tokenize_text(text)

    processed = []

    for token in tokens:

        if token not in stop_words:

            token = lemmatizer.lemmatize(token)

            processed.append(token)

    return processed

def preprocess_text(text):

    tokens = preprocess_tokens(text)

    return " ".join(tokens)
