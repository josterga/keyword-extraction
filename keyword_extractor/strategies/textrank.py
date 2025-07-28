from keyword_extractor.base import KeywordExtractionStrategy
import networkx as nx
import re

class TextRankKeywordExtractor(KeywordExtractionStrategy):
    def __init__(self, top_k=10, stopwords=None, window_size=4):
        self.top_k = top_k
        self.stopwords = set(stopwords) if stopwords else set()
        self.window_size = window_size

    def extract(self, text: str) -> list:
        tokens = [w for w in re.findall(r'\b\w+\b', text.lower()) if w not in self.stopwords]
        graph = nx.Graph()
        for i, word in enumerate(tokens):
            for j in range(i+1, min(i+self.window_size, len(tokens))):
                if tokens[j] != word:
                    graph.add_edge(word, tokens[j])
        scores = nx.pagerank(graph)
        sorted_terms = sorted(scores.items(), key=lambda x: -x[1])
        return [term for term, score in sorted_terms[:self.top_k]]