from __future__ import unicode_literals, print_function

import plac #  wrapper over argparse
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar
import json
import sys


def train():
    model = None
    output_dir=Path("./model-1")
    n_iter=100

    TRAIN_DATA = read_file_json()

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

        # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in tqdm(TRAIN_DATA):
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)

    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
def test():
    model = None
    output_dir=Path("./model-1")
    n_iter=100
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    text = "Thong abc"
    doc = nlp2(text)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    # print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

def read_file_json():
    training_data = []
    lines=[]
    with open('traindata.json', 'r') as f:
        lines = f.readlines()

    for line in lines:
        data = json.loads(line)
        text = data['content']
        entities = []
        for annotation in data['annotation']:
            point = annotation['points'][0]
            labels = annotation['label']
            if not isinstance(labels, list):
                labels = [labels]
            for label in labels:
                entities.append((point['start'], point['end'] + 1 ,label))
        training_data.append((text, {"entities" : entities}))
    for i in training_data:
        print(i)
        sys.exit()
    # return training_data

def check_array():
    text = "Harini Komaravelli\nTest Analyst at Oracle, Hyderabad\n\nHyderabad, Telangana - Email me on Indeed: indeed.com/r/Harini-\nKomaravelli/2659eee82e435d1b\n\n➢ 6 Yrs. of IT Experience in Manual and Automation testing.\n\nWORK EXPERIENCE\n\nQA Analyst\n\nOracle\n\nTest Analyst at Oracle, Hyderabad\n\nInfosys Ltd -  Hyderabad, Telangana -\n\nNovember 2011 to February 2016\n\nHyderabad from Nov 2011 to Feb17 2016\n➢ Worked in Tata Consultancy Services, Hyderabad from Feb 24 to Apr 11 2017\n➢ Currently working as a Test Analyst at Oracle, Hyderabad\n\nQA Analyst with 6 years of IT experience\n\nOracle\n\nEDUCATION\n\nMCA\n\nOsmania University\n\nB.Sc. in Computer Science\n\nOsmania University\n\nSKILLS\n\nFunctional Testing, Blue Prism, Qtp\n\nADDITIONAL INFORMATION\n\nArea of Expertise:\n\n➢ Familiar with Agile Methodologies.\n➢ Having knowledge in Energy (Petroleum) & Health Care domains.\n➢ Involved in preparation of Test Scenarios.\n➢ Preparing Test Data for the test cases.\n\nhttps://www.indeed.com/r/Harini-Komaravelli/2659eee82e435d1b?isid=rex-download&ikw=download-top&co=IN\nhttps://www.indeed.com/r/Harini-Komaravelli/2659eee82e435d1b?isid=rex-download&ikw=download-top&co=IN\n\n\n➢ Experienced in development and execution of Test cases effectively.\n➢ Experienced in Functional testing, GUI testing, Smoke testing, Regression testing and\nIntegration Testing\n➢ Experienced in doing Accessibility testing of an application\n➢ Ability to understand user Requirements, Functional and Design specifications.\n➢ Good knowledge of SDLC and STLC processes.\n➢ Deciding the Severity and Priority of bugs.\n➢ Experience in using Microsoft Test Manager & Oracle Test Manager as Test Management Tools.\n➢ Having good experience in testing windows based & web based applications.\n➢ Involved in Client Interactions for reviews, issues and for any clarifications.\n➢ Web Services Testing\n➢ Writing Test Scripts in QTP, Testcomplete.\n➢ Creating Object Repositories and Function Libraries in QTP.\n➢ Enhanced QTP scripts using VB Script.\n➢ Strong experience in working with Blue Prism tool\n➢ Worked on different Environments like Windows Application & Web Application\n\nTechnical Skills:\n\n❑ Test Automation Tools: Blue Prism, QTP 10.0, Testcomplete\n❑ Test Management Tool: Microsoft Test Manager, Oracle Test Manager & JIRA\n❑ Databases: Oracle 10g, SQL Server.\n\n❑ Operating Systems: Windows 7\n\nProject 1:\nTitle: Cadence\nClient: Baker Hughes\n\nTechnologies: Microsoft Visual Studio and Microsoft Team Foundation Server\n\nClient Background:\nAn oilfield services company delivering focused efforts on shale gas and other oilfield services.\nIt provides services, tools and software for drilling and formation evaluation, well completion,\nproduction management, seismic data collection and interpretation.\n\nProject Description:\nAUT (Application under test) is the next generation revolutionary, robust, easy to use scalable\nwell site data acquisition processing and interpretation system for Client's Drilling Services to\ndeliver services that meets cross divisional business requirements consistently.\n\nProject 2:\n\nDescription:\nParagon supports your entire care team with one tool that your clinicians need to help deliver\nthe best patient care. Designed by physicians, nurses, pharmacists and mid level providers that\nhave a first-hand understanding of clinical workflow needs, Paragon clinical applications allow\nyour caregivers to focus on what matters most; spending time caring for patients. Since Paragon\nis fully-integrated across all applications and built around a single patient database, information\n\n\n\nentered anywhere in the system is immediately available to the entire care team. Immediate\naccess not only helps clinicians make better treatment decisions - it also helps promote patient\nsafety. Paragon offers a broad suite of multidisciplinary clinical software solutions together with\nanytime, anywhere access to the complete patient record.\n\nResponsibilities:\n\n• Performed Smoke testing and Regression testing.\n• Involved in Generating and Executing Test Script using Quick Test Pro & Blue Prism\n• Usability and User Interface Testing.\n• Involved in Defect tracking and reporting the bugs using TFS\n• Participated in frequent walk-through meetings with Internal Quality Assurance groups and with\ndevelopment groups.\n• Participated in client calls and clarifying the doubts by having AT&T sessions\n• Involved in functional, regression and smoke testing to validate the application data changes\ndone in windows application\n• Certifying the build status by running the scripts as part of smoke testing\n\nProject 3:\n\nDescription:\nFood & Beverages R&A: Easily manage business across multiple locations while reducing IT\ncost and complexity. Cloud-based point-of-sale (POS) solutions enable centralized enterprise\nmanagement with lower upfront costs and a smaller footprint.\n\nResponsibilities:\n\n• Performed Functional testing and Regression testing.\n• Involved in Generating and Executing Test Scripts using Blue Prism tool and Open script\n• Involved in preparing bots using Blue Prism tool.\n• Accessibility testing of the web application\n• Involved in Defect tracking and reporting the bugs using JIRA\n• WebServices testing by calling API's to export the data"
    for i in range(0,6):
        print(text[2235 + i])
# train()
# test()
# read_file_json()
check_array()