from typing import Iterable, List
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

class NewsVectorizer:

    def __init__(
        self,
        max_features: int = 15000,
        ngram_range: tuple = (1, 2),
        min_df: int = 3,
        max_df: float = 0.85,
        sublinear_tf: bool = True
    ):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        self.sublinear_tf = sublinear_tf

        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            sublinear_tf=sublinear_tf
        )

    def fit(self, texts: Iterable[str]):
        self.vectorizer.fit(texts)
        return self

    def transform(self, texts: Iterable[str]):
        return self.vectorizer.transform(texts)

    def fit_transform(self, texts: Iterable[str]):
        return self.vectorizer.fit_transform(texts)

    def get_feature_names(self) -> List[str]:
        return list(self.vectorizer.get_feature_names_out())

    def save(self, filepath: str):
        joblib.dump(self.vectorizer, filepath)

    @classmethod
    def load(cls, filepath: str):
        instance = cls()
        instance.vectorizer = joblib.load(filepath)
        return instance
