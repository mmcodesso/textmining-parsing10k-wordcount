# Python NLP Text Analysis

This project aims to analyze text data from 10-K forms, focusing on the core values such as "innovation", "integrity", "quality", "respect", and "teamwork". The program scans through a database of documents and identifies the frequency of these core values in different forms of n-grams (unigram, bigram, trigram). The results are then stored in a SQLite database.

## Requirements

The code requires the following Python libraries:
- `concurrent.futures` - for parallel processing.
- `spacy` - for NLP operations like tokenization, lemmatization, etc.
- `pandas` - for data handling.
- `sqlalchemy` - for handling the SQLite database.
- `textacy` - for creating ngrams.
- `glob` - for file handling.

Also, you need to have the `en_core_web_sm` Spacy model, which can be installed via:

```
python -m spacy download en_core_web_sm
```

The SQLite database `database.sqlite` should be present at the root directory. The text data is expected to be found under a directory structure `./data/YEAR/QUARTER/FILE.txt`.

## Installation

Clone the repository:

```bash
git clone https://github.com/mmcodesso/textmining-parsing10k-wordcount.git
cd textmining-parsing10k-wordcount
```

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate  # Unix/MacOS
.\env\Scripts\activate   # Windows
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Download the required Spacy model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

Run the script via the command line:

```bash
python main.py
```

The script generates a list of 10-K forms from the data directory, excluding previously processed files. Then, it uses multi-processing to process these files concurrently, cleaning the text, creating ngrams, and counting the occurrences of core values.

## Contribution

Contributions, issues and feature requests are welcome. Feel free to check [issues page](https://github.com/mmcodesso/textmining-parsing10k-wordcount/issues) if you want to contribute.

## License

This project is licensed under the terms of the MIT license.

```markdown
# MIT License

Copyright (c) 2023 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```