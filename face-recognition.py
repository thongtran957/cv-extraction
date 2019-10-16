import cv2
 
# Bước 1: Tấm ảnh và tệp tin xml
face_cascade_path = "C:/Users/Thong Tran/Anaconda3/Library/etc/haarcascades/"
face_cascade = cv2.CascadeClassifier(face_cascade_path + "haarcascade_frontalface_default.xml")
image = cv2.imread("images/Bill Gates.jpg")
 
# Bước 2: Tạo một bức ảnh xám
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
#Bước 3: Tìm khuôn mặt
faces = face_cascade.detectMultiScale(
    grayImage,
    scaleFactor  = 1.1,
    minNeighbors = 5,
)
 
# Bước 4: Vẽ các khuôn mặt đã nhận diện được lên tấm ảnh gốc
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x-30, y-30), (x+w+15, y+h+15), (0, 255, 0), 1)
 
# Bước 5: Vẽ lên màn hình
cv2.imshow("Faces found", image)
 
cv2.waitKey(0)
cv2.destroyAllWindows()