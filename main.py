import os
import pickle
import cv2
import face_recognition
import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)

# Carrega os encodes existentes
with open('EncodeFile.p', 'rb') as file:
    encodeListKnow, figurinhaIds = pickle.load(file)

@app.route('/comparar_imagem', methods=['POST'])
def comparar_imagem():
    if 'imagem' not in request.files:
        return jsonify({'mensagem': 'Nenhuma imagem enviada'}), 400

    file = request.files['imagem']
    if file.filename == '':
        return jsonify({'mensagem': 'Nome do arquivo vazio'}), 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurrentFrame)

    for encodeFace, _ in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnow, encodeFace)

        matchIdx = np.argmin(faceDistance)
        if matches[matchIdx]:
            id_figurinha = figurinhaIds[matchIdx]
            #busca imagem reconhecida na pasta Images e retorna em base64
            img_path = os.path.join('Images', figurinhaIds[matchIdx] + '.jpeg')
            img_saved = cv2.imread(img_path)
            # Codifica a imagem em base64
            _, img_encoded = cv2.imencode('.jpeg', img_saved)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            face_distance = faceDistance[matchIdx]
            similaridade = max(0.0, (1 - face_distance / 0.6) * 100)
            print(f"[{id_figurinha}] Distância: {face_distance:.4f} | Similaridade estimada: {similaridade:.2f}%")




                       
            
            
            
            return jsonify({
                "id": id_figurinha,
                "mensagem": f"Figurinha encontrada no álbum: {id_figurinha}",
                "img": img_base64
            })

    return jsonify({"mensagem": "Figurinha não encontrada :("}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)