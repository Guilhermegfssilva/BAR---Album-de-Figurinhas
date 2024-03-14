import os
import pickle
import cv2
import face_recognition
import numpy as np
from flask import Flask, jsonify
import base64

app = Flask(__name__)

# Carregar o arquivo de codificação
print("Carregando arquivo de codificação...")
file = open('EncodeFile.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, studentsIds = encodeListKnowWithIds
print(studentsIds)
print("Arquivo de codificação carregado...")

# Inicializar a captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Função para realizar o reconhecimento facial
def reconhecimento_facial():
    success, img = cap.read()
    if not success:
        return "Erro ao capturar imagem da câmera"

    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurrentFrame)

    for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnow, encodeFace)

        matchIdx = np.argmin(faceDistance)
        print('matchIdx', matchIdx)
        print(faceDistance)
        if matches[matchIdx]:
            print('Rosto conhecido detectado')
            print(studentsIds[matchIdx])
            # Carrega a imagem do rosto reconhecido
            img_path = os.path.join('Images', studentsIds[matchIdx] + '.jpeg')
            img_saved = cv2.imread(img_path)
            # Codifica a imagem em base64
            _, img_encoded = cv2.imencode('.jpeg', img_saved)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            return img_base64
    return None

# Rota do Flask para reconhecimento facial
@app.route('/reconhecimento_facial', methods=['GET'])
def reconhecimento_facial_route():
    img_base64 = reconhecimento_facial()
    if img_base64:
        return jsonify({'mensagem': 'Rosto reconhecido', 'imagem_base64': img_base64})
    else:
        return jsonify({'mensagem': 'Rosto não reconhecido'})

if __name__ == '__main__':
    app.run(debug=True)
