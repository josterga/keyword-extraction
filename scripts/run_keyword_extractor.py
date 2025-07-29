import argparse
import yaml
import json
import os

from keyword_extractor.extractor import KeywordExtractor
from keyword_extractor.stopword_pruner import prune_stopwords_from_results

def load_config(config_path):
    if not config_path or not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f).get("keyword_extraction", {})

def load_stopwords(stopwords_path):
    if not stopwords_path or not os.path.exists(stopwords_path):
        return set()
    with open(stopwords_path, "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

def main():
    parser = argparse.ArgumentParser(description="Keyword extraction runner")
    parser.add_argument("--config", type=str, default=None, help="Path to YAML config file")
    parser.add_argument("--input", type=str, default=None, help="Path to input text file")
    parser.add_argument("--output", type=str, default=None, help="Path to output file")
    parser.add_argument("--stopwords", type=str, default=None, help="Path to stopwords file")
    parser.add_argument("--postprocess", action="store_true", help="Enable postprocessing to prune stopwords")
    parser.add_argument("--prune-mode", type=str, default=None, choices=[
        "remove_if_all_stopwords", "remove_if_any_stopword", "remove_stopwords_within_phrase"
    ], help="Stopword pruning mode")
    args = parser.parse_args()

    # Load config if provided
    config = load_config(args.config) if args.config else {}

    # CLI args override config, which override defaults
    input_path = args.input or config.get("input_file", "input/file.txt")
    output_path = args.output or config.get("output_file", "output.json")
    stopwords_path = args.stopwords or config.get("stopwords_file", "stopwords.txt")
    postprocess = args.postprocess or config.get("postprocess_prune_stopwords", False)
    prune_mode = args.prune_mode or config.get("stopword_prune_mode", "remove_if_all_stopwords")

    with open(input_path, "r") as f:
        text = f.read()

    extractor = KeywordExtractor(config)
    results = extractor.extract(text)

    if postprocess:
        stopwords = load_stopwords(stopwords_path)
        results = prune_stopwords_from_results(results, stopwords, mode=prune_mode)
        print(f"Postprocessed results: pruned stopwords using {stopwords_path} with mode {prune_mode}")

    print("Extraction results:")
    print(results)

    with open(output_path, "w") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()