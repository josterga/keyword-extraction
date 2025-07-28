import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

class BasicKeywordExtractor:
    def __init__(self, config):
        self.use_lemmatization = config.get("use_lemmatization", True)
        self.remove_stopwords = config.get("remove_stopwords", True)
        self.min_word_length = config.get("min_word_length", 3)
        self.min_phrase_length = config.get("min_phrase_length", 2)
        self.extract_phrases = config.get("extract_phrases", True)
        self.spacy_model = config.get("spacy_model", "en_core_web_sm")
        self.stopwords = set(stopwords.words('english')) if self.remove_stopwords else set()
        self.lemmatizer = WordNetLemmatizer() if self.use_lemmatization else None
        self.nlp = spacy.load(self.spacy_model) if self.extract_phrases else None

    def normalize_word(self, word):
        word = re.sub(r"[^\w\-]", "", word).lower()
        if self.lemmatizer:
            word = self.lemmatizer.lemmatize(word)
        return word

    def extract_keywords(self, text):
        words = [self.normalize_word(w) for w in word_tokenize(text)]
        words = [
            w for w in words
            if w and (not self.remove_stopwords or w not in self.stopwords)
            and len(w) >= self.min_word_length and not w.isnumeric()
        ]
        return words

    def extract_noun_phrases(self, text):
        if not self.extract_phrases or not self.nlp:
            return []
        doc = self.nlp(text)
        def normalize_phrase(phrase):
            return ' '.join([
                self.lemmatizer.lemmatize(w.lower()) if self.lemmatizer else w.lower()
                for w in word_tokenize(phrase) if w.isalnum()
            ])
        return [
            normalize_phrase(chunk.text)
            for chunk in doc.noun_chunks
            if len(chunk.text.split()) >= self.min_phrase_length
        ]