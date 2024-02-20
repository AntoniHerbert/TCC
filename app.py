from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import shutil
import os
import random
import time

app = Flask(__name__)





CORS(app)

# Define o diretório onde os vídeos serão salvos
VIDEO_UPLOAD_FOLDER = 'video_uploads'
DATA_UPLOAD_FOLDER = 'data_uploads'
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['DATA_UPLOAD_FOLDER'] = DATA_UPLOAD_FOLDER

def initialize():
    # Remove o conteúdo da pasta data_uploads
    if os.path.exists(DATA_UPLOAD_FOLDER):
        shutil.rmtree(DATA_UPLOAD_FOLDER)
    os.makedirs(DATA_UPLOAD_FOLDER)

    # Remove o conteúdo da pasta video_uploads
    if os.path.exists(VIDEO_UPLOAD_FOLDER):
        shutil.rmtree(VIDEO_UPLOAD_FOLDER)
    os.makedirs(VIDEO_UPLOAD_FOLDER)
    
initialize()
# Página inicial com formulário para upload de vídeo

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'videoFile' in request.files:
            video = request.files['videoFile']
            video.filename = 'meu_video.mp4'
            # Salva o vídeo no diretório de uploads
            video.save(os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], video.filename))
            # Redireciona para a página de pré-visualização, passando o nome do arquivo como parâmetro
            return redirect(url_for('preview', filename=video.filename))
    return render_template('index.html')

# Página de pré-visualização do vídeo
@app.route('/preview/<filename>')
def preview(filename):
    return render_template('preview.html', filename=filename)

# Endpoint para servir o vídeo armazenado
@app.route('/get-video')
def get_video():
    video_filename = 'meu_video.mp4'  # Nome do vídeo a ser recuperado
    return send_from_directory(app.config['VIDEO_UPLOAD_FOLDER'], video_filename)

# Novo endpoint para receber e armazenar os dados do vídeo enviado pela página
@app.route('/save-image', methods=['POST'])
def save_image():
    if 'image' in request.json:
        # Decodifica a imagem base64
        image_data = request.json['image'].split(',')[1].encode()
        
        # Salva a imagem no diretório de uploads
        with open(os.path.join(app.config['DATA_UPLOAD_FOLDER'], 'selected_area.png'), 'wb') as f:
            f.write(image_data)
        
        return 'Imagem salva com sucesso.', 200
    else:
        return 'Dados da imagem não encontrados.', 400


# Novo endpoint para gerar e retornar um número aleatório 30 vezes por segundo
@app.route('/random-number')
def random_number():
    # Gera um único número aleatório
    random_num = str(random.random())
    
    # Retorna o número aleatório como resposta
    return random_num


if __name__ == '__main__':
    app.run(debug=True)
