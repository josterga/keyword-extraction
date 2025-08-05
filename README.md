#  `keyword_extraction` — Configurable Keyword Extraction

- **Description:**  
  Extracts keywords and phrases from text using multiple strategies, with stopword pruning and lemmatization.
- **Entrypoint:**  
  CLI: `python -m scripts.run_keyword_extractor --config config.yaml`  
  Library: `from keyword_extractor.extractor import KeywordExtractor`
- **Configurable Arguments (CLI):**
  - `--config`: Path to YAML config.
  - `--input`: Input text file.
  - `--output`: Output file.
  - `--stopwords`: Stopwords file.
  - `--postprocess`: Enable stopword pruning.
  - `--prune-mode`: Stopword pruning mode.

- **Configurable Options (YAML):**
  - `use_lemmatization`, `remove_stopwords`, `min_word_length`, `min_phrase_length`, `top_n_keywords`, `top_n_phrases`, `extract_phrases`, `spacy_model`, `input_dir`, `output_file`.
