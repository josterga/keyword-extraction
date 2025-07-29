from setuptools import setup, find_packages

setup(
    name="keyword_extraction",
    version="0.1.0",
    description="A flexible keyword extraction library with multiple strategies and configurable stopword pruning.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),  # This will include keyword_extractor and submodules
    install_requires=[
        "pyyaml",
        # Add other dependencies here, e.g.:
        # "scikit-learn", "spacy", "nltk"
    ],
    entry_points={
        "console_scripts": [
            "run-keyword-extractor=scripts.run_keyword_extractor:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.7",
)