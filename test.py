import json
from keyword_extractor.extractor import KeywordExtractor
from keyword_extractor.stopword_pruner import prune_stopwords_from_results

# Example arguments (not using config.yaml)
config = {
    "strategy": "tfidf",
    "tfidf": {
        "top_k": 10,
        "stopwords": ["the", "and", "is", "in", "to", "of"]  # Example stopwords for the strategy
    }
}

input_file = "input/file.txt"
output_file = "results_test.json"
postprocess = True
prune_mode = "remove_if_all_stopwords"
stopwords = {"the", "and", "is", "in", "to", "of"}  # Example global stopwords for postprocessing

# Read input text
with open(input_file, "r") as f:
    text = f.read()

# Run extraction
extractor = KeywordExtractor(config)
results = extractor.extract(text)

# Optionally postprocess
if postprocess:
    results = prune_stopwords_from_results(results, stopwords, mode=prune_mode)
    print(f"Postprocessed results with mode {prune_mode}")

# Print and save results
print("Extraction results:")
print(json.dumps(results, indent=2))

with open(output_file, "w") as out_f:
    json.dump(results, out_f, indent=2)
print(f"Results written to {output_file}")