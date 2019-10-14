import pdf2text
import re

# if code not working
import os
java_path = "C:/Program Files/Java/jdk1.8.0_221/bin/java.exe"
os.environ['JAVAHOME'] = java_path

import nltk
from nltk.tag.stanford import StanfordNERTagger

def main():
    file_path = 'pdf/Elliot-Alderson-Resume-Software-Developer-1.pdf'
    text = ''
    for page in pdf2text.extract_text_from_pdf(file_path):
        text += ' ' + page

    emails = extract_email(text)
    phone = extract_mobile_number(text)
    address = extract_address(text)
    person_name = extract_person_name(text)
    print(person_name)
    print(emails)
    print(phone)
    print(address)

def extract_person_name(text):
    person_name = ''
    try:
        st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz',
                        'stanford-ner/stanford-ner.jar')
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = st.tag(tokens)
            for tag in tags:
                if tag[1] in ["PERSON"]:
                    person_name += tag[0] + ' '
    except Exception as e:
        print(e)
    return person_name
def extract_address(text):
    address = None
    try:
        regular_expression = re.compile(r"[0-9]+ [a-z0-9,\.# ]+\bCA\b", re.IGNORECASE)
        address = re.search(regular_expression, text)
        if address:
            address = address.group()
    except Exception as e:
        print(e)
    return address

def extract_email(text):
    email = None
    try:
        pattern = re.compile(r'\S*@\S*')
        matches = pattern.findall(text) 
        email = matches
    except Exception as e:
        print(e)
    return email

def extract_mobile_number(text):
    phones = None
    try:
        pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        matchs = pattern.findall(text)
        matchs = [re.sub(r'[,.]', '', el) for el in matchs if len(re.sub(r'[()\-.,\s+]', '', el))>6]
        matchs = [re.sub(r'\D$', '', el).strip() for el in matchs]
        matchs = [el for el in matchs if len(re.sub(r'\D','',el)) <= 15]
        try:
            for el in list(matchs):
                if len(el.split('-')) > 3: continue 
                for x in el.split("-"):
                    try:
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                match.remove(el)
                    except:
                        pass
        except:
            pass
        phones = list(dict.fromkeys(matchs))
    except Exception as e:
        print(e)
    return phones

main()