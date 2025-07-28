import argparse
import yaml
from keyword_extractor.extractor import KeywordExtractor
import json

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["keyword_extraction"]

def main():
    parser = argparse.ArgumentParser(description="Keyword extraction runner")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file")
    parser.add_argument("--input", type=str, default=None, help="Path to input text file (overrides config)")
    parser.add_argument("--output", type=str, default=None, help="Path to output file (overrides config)")
    args = parser.parse_args()

    config = load_config(args.config)
    input_path = args.input or config.get("input_file", "input/file.txt")
    output_path = args.output or config.get("output_file", "output.json")

    with open(input_path, "r") as f:
        text = f.read()

    extractor = KeywordExtractor(config)
    results = extractor.extract(text)

    print("Extraction results:")
    print(results)

    # Write results to output file
    with open(output_path, "w") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()