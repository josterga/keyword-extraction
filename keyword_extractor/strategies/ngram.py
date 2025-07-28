from keyword_extractor.base import KeywordExtractionStrategy
import re

class NgramKeywordExtractor(KeywordExtractionStrategy):
    def __init__(self, ngram_sizes=(1, 2, 3), stopwords=None):
        self.ngram_sizes = ngram_sizes
        self.stopwords = set(stopwords) if stopwords else set()

    def extract(self, text: str) -> list:
        tokens = re.findall(r'\b\w+\b', text.lower())
        ngrams = set()
        for n in self.ngram_sizes:
            for i in range(len(tokens) - n + 1):
                ng = tokens[i:i+n]
                if not any(w in self.stopwords for w in ng):
                    ngrams.add(' '.join(ng))
        return list(ngrams)