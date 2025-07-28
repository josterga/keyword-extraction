from keyword_extractor.base import KeywordExtractionStrategy
from sklearn.feature_extraction.text import TfidfVectorizer

class TfIdfKeywordExtractor(KeywordExtractionStrategy):
    def __init__(self, top_k=10, stopwords=None):
        self.top_k = top_k
        self.stopwords = stopwords

    def extract(self, text: str) -> list:
        vectorizer = TfidfVectorizer(stop_words=self.stopwords)
        tfidf = vectorizer.fit_transform([text])
        scores = zip(vectorizer.get_feature_names_out(), tfidf.toarray()[0])
        sorted_terms = sorted(scores, key=lambda x: -x[1])
        return [term for term, score in sorted_terms[:self.top_k] if score > 0]