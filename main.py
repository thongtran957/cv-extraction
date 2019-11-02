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

# if code not working
# import os
# java_path = "C:/Program Files/Java/jdk1.8.0_221/bin/java.exe"
# os.environ['JAVAHOME'] = java_path

def main():
    file_path = 'pdf/PHP Web Developer Resume.pdf'
    text = ''
    for page in pdf2text.extract_text_from_pdf(file_path):
        text += ' ' + page

    emails = extract_email(text)
    phone = extract_mobile_number(text)
    address = extract_address(text)
    person_name = extract_person_name(text)
    # avatar_path = face_recognize(file_path)
    skills = extract_skills(text)
    # education = extract_education(text)
    # experience = extract_experience(text)
    # competencie = extract_competencie(text, experience)
    print(person_name)
    print(emails)
    print(phone)
    print(address)
    # print(avatar_path)
    print(skills)
    # print(education)
    # print(experience)
    # print(competencie)


def extract_experience(text):
    word_tokens = nltk.tokenize.word_tokenize(text)
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = pt.STOPWORDS
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words] 
    sent = nltk.pos_tag(filtered_sentence)
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)
    
    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)
    
    test = []
    
    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x

def extract_competencie(text, experience_list):
    '''
    Helper function to extract competencies from resume text
    :param resume_text: Plain resume text
    :return: dictionary of competencies
    '''
    experience_text = ' '.join(experience_list)
    competency_dict = {}

    for competency in pt.COMPETENCIES.keys():
        for item in pt.COMPETENCIES[competency]:
            if string_found(item, experience_text):
                if competency not in competency_dict.keys():
                    competency_dict[competency] = [item]
                else:
                    competency_dict[competency].append(item)

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

def extract_skills(text):
    tokens = nltk.tokenize.word_tokenize(text)
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    return skillset

def extract_education(atext):
    edu = {}
    for index, text in enumerate(atext):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in pt.EDUCATION and tex not in pt.STOPWORDS:
                edu[tex] = text + atext[index + 1]

    education = []
    for key in edu.keys():
        year = re.search(re.compile(pt.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False

main()
