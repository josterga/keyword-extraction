import argparse
import yaml
import json
import os

from keyword_extractor.extractor import KeywordExtractor

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["keyword_extraction"]

def load_stopwords(stopwords_path):
    if not stopwords_path or not os.path.exists(stopwords_path):
        return set()
    with open(stopwords_path, "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

def prune_stopwords_from_results(results, stopwords):
    def is_stopword(term):
        # Handles both single words and phrases
        return all(word.lower() in stopwords for word in term.split())

    pruned = {}
    for strategy, items in results.items():
        # Items can be list of strings, list of dicts, or list of tuples
        new_items = []
        for item in items:
            if isinstance(item, str):
                if not is_stopword(item):
                    new_items.append(item)
            elif isinstance(item, (list, tuple)):
                # For n-grams as tuples/lists
                if not any(word.lower() in stopwords for word in item):
                    new_items.append(item)
            elif isinstance(item, dict):
                # For dicts with 'term' or 'phrase'
                key = 'term' if 'term' in item else 'phrase' if 'phrase' in item else None
                if key and not is_stopword(item[key]):
                    new_items.append(item)
                # If no key, keep as is
            else:
                new_items.append(item)
        pruned[strategy] = new_items
    return pruned

def main():
    parser = argparse.ArgumentParser(description="Keyword extraction runner")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file")
    parser.add_argument("--input", type=str, default=None, help="Path to input text file (overrides config)")
    parser.add_argument("--output", type=str, default=None, help="Path to output file (overrides config)")
    args = parser.parse_args()

    config = load_config(args.config)
    input_path = args.input or config.get("input_file", "input/file.txt")
    output_path = args.output or config.get("output_file", "output.json")
    stopwords_path = config.get("stopwords_file", "stopwords.txt")
    postprocess = config.get("postprocess_prune_stopwords", False)

    with open(input_path, "r") as f:
        text = f.read()

    extractor = KeywordExtractor(config)
    results = extractor.extract(text)

    if postprocess:
        stopwords = load_stopwords(stopwords_path)
        results = prune_stopwords_from_results(results, stopwords)
        print(f"Postprocessed results: pruned stopwords using {stopwords_path}")

    print("Extraction results:")
    print(results)

    with open(output_path, "w") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()