import argparse
import yaml
from keyword_extractor.extractor import KeywordExtractor

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["keyword_extraction"]

def main():
    parser = argparse.ArgumentParser(description="Keyword extraction runner")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file")
    parser.add_argument("--input", type=str, default="input/file.txt", help="Path to input text file")
    args = parser.parse_args()

    config = load_config(args.config)
    extractor = KeywordExtractor(config)

    with open(args.input, "r") as f:
        text = f.read()

    results = extractor.extract(text)
    print("Extraction results:")
    print(results)

if __name__ == "__main__":
    main()