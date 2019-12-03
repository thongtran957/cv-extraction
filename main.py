import pdf2text
import re
import os
import pandas as pd
import spacy
import pattern as pt
import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords 
from face_recognize import face_recognize
import sys

# if code not working
# import os
# java_path = "C:/Program Files/Java/jdk1.8.0_221/bin/java.exe"
# os.environ['JAVAHOME'] = java_path

def main(file_path):
    # file_path = '/home/thongtran/projects/cv-extraction/pdf/Elliot-Alderson-Resume-Software-Developer-1.pdf'
    text = ''
    for page in pdf2text.extract_text_from_pdf(file_path):
        text += ' ' + page
    email = extract_email(text)
    phone = extract_mobile_number(text)
    address = extract_address(text)
    person_name = extract_person_name(text)
    skills = extract_skills(text)
    education = extract_education(text)
    print('Fullname:')
    print(person_name)
    print('Email: ')
    print(email)
    print('Phone: ')
    print(phone)
    print('Address: ')
    print(address)
    print('Job Skills: ')
    print(skills)
    print('Education: ')
    print(education)

def extract_person_name(text):
    person_name = ''
    try:
        st = StanfordNERTagger('/home/thongtran/projects/cv-extraction/stanford-ner/english.all.3class.distsim.crf.ser.gz',
                        '/home/thongtran/projects/cv-extraction/stanford-ner/stanford-ner.jar')
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

def extract_skills(text):
    tokens = nltk.tokenize.word_tokenize(text)
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    return skillset

def extract_education(text):
    education = []
   
    tokens = nltk.tokenize.word_tokenize(text)
    for index, token in enumerate(tokens):
        if token.upper() in pt.EDUCATION and token not in pt.STOPWORDS:
            temp = ""
            for i in range(0,4):
                temp += tokens[index + i] + ' '
            education.append(temp)
            
    return education
    

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False

# def extract_text(file_path, extension):
#     '''
#     Wrapper function to detect the file extension and call text extraction function accordingly

#     :param file_path: path of file of which text is to be extracted
#     :param extension: extension of file `file_name`
#     '''
#     text = ''
#     if extension == '.pdf':
#         for page in extract_text_from_pdf(file_path):
#             text += ' ' + page
#     elif extension == '.docx':
#         text = extract_text_from_docx(file_path)
#     return text

if __name__ == '__main__':
    file_path = sys.argv[1]
    main(file_path)