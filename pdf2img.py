from pdf2image import convert_from_path 
import tempfile
def convert_pdf_2_img(pdf_path):
    image = convert_from_path(pdf_path)
    return image
