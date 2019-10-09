import docx

def extract_text_from_doc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return ' '.join(fullText)

# file_path = "file-sample_100kB.docx"
# print(extract_text_from_doc(file_path))