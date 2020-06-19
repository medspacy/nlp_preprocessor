# nlp_preprocessor
This package implements a SpaCy component for modifying the string of a doc before tokenizing. 

# Overview
This component is useful in clinical text processing for cleaning up text formatting, normalizing abbreviations or 
misspellings, and removing problematic semi-structured template texts. 

The `Preprocessor` class is instantiated with the tokenizer of a spaCy `Language` model. 
To add the preprocessor to your pipeline, you must set it to be the tokenizer: 
```python 
from nlp_preprocessor import Preprocessor

preprocessor = Preprocessor(nlp.tokenizer)
nlp.tokenizer = preprocessor
```

Processing steps are then added to the preprocessor by calling `preprocessor.add(rules)`. The
preprocessor then executes each of the processing steps and finally returns `tokenizer(text)`
to return a spaCy `Doc`.

You can access the original tokenizer through `preprocessor.tokenizer`.

The `PreprocessingRule` class offers one way to define preprocessing steps. This class takes a compiled regular 
expression pattern as well as an optional replacement string (default is a blank string) and description. 
When a rule is executed on the text it will replace any occurrences of the pattern with the replacement string.

```python 
from nlp_preprocessor import PreprocessingRule
import re

rule = PreprocessingRule(re.compile("there"), repl="world!")
preprocessor.add([rule])
doc = preprocessor("Hello, there")
print(doc)
>>> Hello, world!
```

You can use any Python callable as a rules, such as lambda functions or other objects, as long as they take the text as 
input and return the text as output.

# Usage
## Installation
You can install `nlp_preprocessor` using pip:
```bash
pip install nlp_preprocessor
```

Or clone this repository install using the `setup.py` script:
```bash
$ python setup.py install
```

Once you've installed the package and spaCy, make sure you have a spaCy language model installed (see https://spacy.io/usage/models):

```bash
$ python -m spacy download en_core_web_sm
```

## Example
In this short example below, we'll use the preprocessor to delete templated text, lower-case the document, and expand an
abbreviation.

```python
from nlp_preprocessor import Preprocessor, PreprocessingRule
import spacy
import re

text = "TOBACCO SCREENING: The patient does/does not smoke tobacco daily. Purpose of visit: R/O pneumonia."

nlp = spacy.blank("en")
preprocessor = Preprocessor(nlp.tokenizer)
nlp.tokenizer = preprocessor

rules = [
    PreprocessingRule(re.compile("TOBACCO SCREENING: The patient does/does not smoke tobacco daily."),
                                desc="Remove tobacco screening."),
    lambda x: x.lower(),
    PreprocessingRule(re.compile("r/o"), repl="rule out", desc="Normalize 'rule out' abbreviation."),
]
preprocessor.add(rules)

doc = nlp(text)
print(doc)
>>> purpose of visit: rule out pneumonia.
```