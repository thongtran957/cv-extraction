from __future__ import unicode_literals, print_function

import plac #  wrapper over argparse
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar
import json
import sys
import pdf2text

def test(file_path):
    output_dir=Path("/home/thongtran/projects/cv-extraction/model-1")
    nlp2 = spacy.load(output_dir)
    text = ''
    for page in pdf2text.extract_text_from_pdf(file_path):
        text += ' ' + page
    doc = nlp2(text)
    # print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    for ent in doc.ents:
        print(ent.label_ + ':' + ent.text)
    # print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

if __name__ == '__main__':
    file_path = sys.argv[1]
    test(file_path)
