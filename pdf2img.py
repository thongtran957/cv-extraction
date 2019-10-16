from pdf2image import convert_from_path 
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import os

def get_first_pages_from_pdf(pdf_path):
    inputpdf = PdfFileReader(open(pdf_path, "rb"))
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(0))
    with open('pdf/pdf-' + str(round(time.time())) +'.pdf' , 'wb') as outfile:
        output.write(outfile)
        return outfile.name

def pdf_2_img(pdf_path):
    first_page_pdf = get_first_pages_from_pdf(pdf_path)
    images = convert_from_path(first_page_pdf)
    for image in images:
        image_path = 'images/image-' + str(round(time.time())) + '.jpg'
        image.save(image_path, 'JPEG')
        os.remove(first_page_pdf)
        return image_path
    

