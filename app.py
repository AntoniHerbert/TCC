from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
import shutil
import os
import random
import time
import d_computeareaframe
import cv2
import asyncio
import websockets
import base64
from io import BytesIO
import numpy as np

app = Flask(__name__)





CORS(app)

# Define o diretório onde os vídeos serão salvos
VIDEO_UPLOAD_FOLDER = 'video_uploads'
DATA_UPLOAD_FOLDER = 'data_uploads'
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['DATA_UPLOAD_FOLDER'] = DATA_UPLOAD_FOLDER
app.config['IMAGE_PREFIX'] = 'image_'
app.config['IMAGE_SUFFIX'] = '.png'
app.config['START_INDEX'] = 0

def initialize():
    # Remove o conteúdo da pasta data_uploads
    if os.path.exists(DATA_UPLOAD_FOLDER):
        shutil.rmtree(DATA_UPLOAD_FOLDER)
    os.makedirs(DATA_UPLOAD_FOLDER)

    # Remove o conteúdo da pasta video_uploads
    if os.path.exists(VIDEO_UPLOAD_FOLDER):
        shutil.rmtree(VIDEO_UPLOAD_FOLDER)
    os.makedirs(VIDEO_UPLOAD_FOLDER)

def process_image(image_path):
    """
    Processa a imagem e retorna a área calculada.
    """
    # Ler imagem
    img = cv2.imread(image_path)

    # Processar imagem (exemplo simples: converter para escala de cinza e binarizar)
    n_area = d_computeareaframe.computeArea(img)    
    # Aplicar um limiar para binarização
    
    return n_area
    
initialize()
# Página inicial com formulário para upload de vídeo

@app.route('/initialize', methods=['POST'])
def initialize_folders():
    initialize()
    return jsonify({"message": "Pastas inicializadas com sucesso."}), 200

@app.route('/', methods=['POST'])
def index():
    if 'videoFile' in request.files:
        video = request.files['videoFile']
        video.filename = 'meu_video.mp4'
        # Salva o vídeo no diretório de uploads
        video.save(os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], video.filename))
        return jsonify({"message": "Vídeo enviado com sucesso!"}), 200
    else:
        return jsonify({"error": "Nenhum arquivo de vídeo enviado."}), 400


# Endpoint para servir o vídeo armazenado
@app.route('/get-video')
def get_video():
    video_filename = 'meu_video.mp4'  # Nome do vídeo a ser recuperado
    return send_from_directory(app.config['VIDEO_UPLOAD_FOLDER'], video_filename)

image_counter = 0

async def handle_image(websocket, path):
    global image_counter

    async for message in websocket:
        # Decodificar a imagem base64
        header, encoded = message.split(b',', 1)
        image_data = base64.b64decode(encoded)

        # Converte os dados da imagem para um array NumPy
        image_bytes = BytesIO(image_data)
        img_array = np.frombuffer(image_bytes.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Aqui a imagem é carregada como BGR

        # Cria um nome de arquivo sequencial
        filename = f'image_{image_counter}.png'
        image_counter += 1  # Incrementa o contador para a próxima imagem

        # Salva a imagem no diretório de uploads
        image_path = os.path.join(DATA_UPLOAD_FOLDER, filename)
        cv2.imwrite(image_path, img)

        # Chama a função d_computeareaframe.computeArea() passando a imagem
        area = d_computeareaframe.computeArea(img)

        # Converte o resultado para uma string
        area_str = str(area)

        # Envia a string de volta ao cliente
        await websocket.send(area_str)

async def main():
    async with websockets.serve(handle_image, "localhost", 8765):
        await asyncio.Future()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
