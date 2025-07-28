from keyword_extractor.base import KeywordExtractionStrategy
import re
from collections import Counter, defaultdict

class RakeKeywordExtractor(KeywordExtractionStrategy):
    def __init__(self, stopwords=None, min_char_length=1, max_words_length=5, top_k=10):
        self.stopwords = set(stopwords) if stopwords else set()
        self.min_char_length = min_char_length
        self.max_words_length = max_words_length
        self.top_k = top_k

    def extract(self, text: str) -> list:
        sentences = re.split(r'[.!?;\n]', text.lower())
        phrase_list = []
        for sent in sentences:
            words = [w for w in re.findall(r'\b\w+\b', sent) if w not in self.stopwords]
            phrase = []
            for word in words:
                if word in self.stopwords:
                    if phrase:
                        phrase_list.append(' '.join(phrase))
                        phrase = []
                else:
                    phrase.append(word)
            if phrase:
                phrase_list.append(' '.join(phrase))
        # Calculate word scores
        freq = Counter()
        degree = defaultdict(int)
        for phrase in phrase_list:
            words = phrase.split()
            degree.update({w: len(words) for w in words})
            freq.update(words)
        word_score = {w: degree[w] / freq[w] for w in freq}
        # Calculate phrase scores
        phrase_scores = {}
        for phrase in phrase_list:
            phrase_scores[phrase] = sum(word_score.get(w, 0) for w in phrase.split())
        sorted_phrases = sorted(phrase_scores.items(), key=lambda x: -x[1])
        return [phrase for phrase, score in sorted_phrases[:self.top_k]]