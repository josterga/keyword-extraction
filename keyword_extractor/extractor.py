from keyword_extractor.strategies.ngram import NgramKeywordExtractor
from keyword_extractor.strategies.tfidf import TfIdfKeywordExtractor
from keyword_extractor.strategies.textrank import TextRankKeywordExtractor
from keyword_extractor.strategies.rake import RakeKeywordExtractor

class KeywordExtractor:
    STRATEGY_MAP = {
        "ngram": NgramKeywordExtractor,
        "tfidf": TfIdfKeywordExtractor,
        "textrank": TextRankKeywordExtractor,
        "rake": RakeKeywordExtractor,
    }

    def __init__(self, config):
        strategy_name = config.get("strategy")
        if not strategy_name or strategy_name not in self.STRATEGY_MAP:
            raise ValueError(f"Invalid or missing strategy: {strategy_name}")
        strategy_config = config.get(strategy_name, {})
        self.strategy_name = strategy_name
        self.strategy = self.STRATEGY_MAP[strategy_name](**strategy_config)

    def extract(self, text: str):
        return {self.strategy_name: self.strategy.extract(text)}