import cv2
import face_recognition
import pickle
import os

#import students image
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentsIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentsIds.append(os.path.splitext(path)[0])

def findEncoding(imagesList):
    encodingsList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodingsList.append(encode)

    return encodingsList

print("Encoding Start")
encodeListKnow = findEncoding(imgList)
encodeListKnowWithIds = [encodeListKnow,studentsIds]
print(encodeListKnow)
print("Encoding Complete")

file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnowWithIds,file)
file.close()
print("File Save")