from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
import shutil
import os
import random
import time
import d_computeareaframe
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import base64
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
    n_area, imagem = d_computeareaframe.computeArea(img)    
    # Aplicar um limiar para binarização
    
    return n_area, imagem
    
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
area_all_images = []

@app.route('/save-image', methods=['POST'])
def save_image():
    global image_counter  # Usa a variável global para contar as imagens

    if 'image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de imagem encontrado na solicitação.'}), 400
    
    file = request.files['image']

    img = Image.open(file.stream)
    img = np.array(img)

    # Converte a imagem para o formato BGR
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    filename = f'image_{image_counter}.png'
    image_counter += 1

    save_path = os.path.join(app.config['DATA_UPLOAD_FOLDER'], filename)
    cv2.imwrite(save_path, img_bgr)

    return jsonify({"message": "Imagem convertida para BGR com sucesso!"})

current_index = app.config['START_INDEX']


# Novo endpoint para gerar e retornar um número aleatório 30 vezes por segundo
@app.route('/random-number', methods=['GET'])
def get_area():

    index = request.args.get('index', type=int)

    if index is None:
        return 'Parâmetro de índice ausente', 400

    # Formatar o nome do arquivo da imagem com base no índice atual
    image_filename = f"{app.config['IMAGE_PREFIX']}{index}{app.config['IMAGE_SUFFIX']}"
    image_path = os.path.join(app.config['DATA_UPLOAD_FOLDER'], image_filename)

    # Verificar se o arquivo existe
    if not os.path.isfile(image_path):
        return 'Imagem não encontrada', 404

    # Processar imagem e calcular a área
    area, foto = process_image(image_path)

    area_all_images.append(area)

    if not isinstance(foto, np.ndarray):
        return 'Erro ao processar a imagem', 500

    # Converter a imagem NumPy para PIL.Image
    img_pil = Image.fromarray(foto)

    buffered = BytesIO()
    img_pil.save(buffered, format="png")  # Supondo que a imagem seja em formato JPEG
    foto_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    print(area_all_images)

    # Retornar a área calculada como uma string simples
    return jsonify({
        'numero': str(area),
        'image': f"data:image/jpeg;base64,{foto_base64}"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
