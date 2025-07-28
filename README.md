Option	Type	Default	Description	Where Used
use_lemmatization	bool	true	Whether to lemmatize words/phrases (reduce to base form, e.g., "running" → "run")	In normalize_word and phrase normalization
remove_stopwords	bool	true	Whether to remove common stopwords (e.g., "the", "and")	In extract_keywords
min_word_length	int	3	Minimum length for a word to be considered a keyword	In extract_keywords
min_phrase_length	int	2	Minimum number of words in a phrase to be considered a noun phrase	In extract_noun_phrases
top_n_keywords	int	200	Number of top keywords to output (by frequency)	In run() output
top_n_phrases	int	100	Number of top phrases to output (by frequency)	In run() output
extract_phrases	bool	true	Whether to extract noun phrases (multi-word expressions)	In extract_noun_phrases
spacy_model	str	en_core_web_sm	spaCy model to use for phrase extraction	In BasicKeywordExtractor.__init__
input_dir	str	documentation	Directory containing markdown files to process	In run()
output_file	str	domain_keywords_ranked.json	Output file for results	In run()
How Each Option Is Used
1. use_lemmatization
If true, words and phrases are lemmatized (e.g., "running" → "run").
Used in both keyword and phrase normalization.
2. remove_stopwords
If true, common English stopwords are removed from the keyword list.
Uses NLTK’s stopword list.
3. min_word_length
Only words with at least this many characters are considered as keywords.
4. min_phrase_length
Only noun phrases with at least this many words are considered as phrases.
5. top_n_keywords / top_n_phrases
Limits the number of keywords/phrases in the output JSON to the top N by frequency.
6. extract_phrases
If true, noun phrase extraction is performed using spaCy.
If false, only single-word keywords are extracted.
7. spacy_model
Specifies which spaCy model to use for phrase extraction.
Allows you to swap in larger or domain-specific models if needed.
8. input_dir
Directory to recursively search for .md files to process.
9. output_file
Path to the output JSON file where results are saved.
How the Config is Used in Code
The config is loaded at the start of the script and passed to the KeywordExtractor class.
Each option controls a specific aspect of the extraction process, as described above.
You can change the config and rerun the script to experiment with different extraction behaviors, without changing any code.



python -m scripts.run_keyword_extractor --config config.yaml