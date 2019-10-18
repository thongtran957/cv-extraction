import cv2
from pdf2image import convert_from_path 
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import time

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
        
def face_recognize(pdf_path):
    image_path = pdf_2_img(pdf_path)
    # Bước 1: Tấm ảnh và tệp tin xml
    face_cascade_path = "C:/Users/Thong Tran/Anaconda3/Library/etc/haarcascades/"
    # face_cascade_path = "C:/Users/thongtran/Anaconda3/Library/etc/haarcascades/"
    face_cascade = cv2.CascadeClassifier(face_cascade_path + "haarcascade_frontalface_default.xml")
    image = cv2.imread(image_path)
    
    # Bước 2: Tạo một bức ảnh xám
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Bước 3: Tìm khuôn mặt
    faces = face_cascade.detectMultiScale(
        grayImage,
        scaleFactor  = 1.4,
        minNeighbors = 1,
        minSize= (30,30),
    )
    
    # Bước 4: Vẽ các khuôn mặt đã nhận diện được lên tấm ảnh gốc
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x-w, y-h), (x+(2*w), y+(2*h)), (0, 255, 0), 2)
        roi_color = image[y-h:y + 2*h, x-w:x + 2*w]
        image_face_path = 'images/face-' + str(round(time.time())) + '.jpg'
        cv2.imwrite(image_face_path, roi_color)
        os.remove(image_path) 
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return image_face_path
    
