import spacy
import random
import os
import en_core_web_sm

def train():
        TRAIN_DATA = [
                ("Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
                ("Google rebrands its business apps", {"entities": [(0, 6, "ORG")]})]

        nlp = spacy.blank("en")
        optimizer = nlp.begin_training()
        for i in range(20):
                random.shuffle(TRAIN_DATA)
        for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer)
        nlp.to_disk("./model")
def test():
        text = "Uber blew through $1 million a week"
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        print("\nEntities found before training:")
        for ent in doc.ents:
                if ent.label_=='ORG':
                        print(ent.label_, ent.text)

        nlp = spacy.load('./model')
        doc = nlp(text)

        print("\\nEntities found after training:")
        for ent in doc.ents:
                if ent.label_=='ORG':
                        print(ent.label_, ent.text)
train()
test()