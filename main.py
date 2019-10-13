import pdf2text
import re
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
    extract_person_name(text)
    print(emails)
    print(phone)
    print(address)


def extract_person_name(text):
    st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1] in ["PERSON", "LOCATION", "ORGANIZATION"]:
                print(tag)

def extract_address(text):
    regular_expression = re.compile(r"[0-9]+ [a-z0-9,\.# ]+\bCA\b", re.IGNORECASE)
    result = re.search(regular_expression, text)
    if result:
        result = result.group()
    return result

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