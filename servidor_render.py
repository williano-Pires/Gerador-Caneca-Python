from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import base64

app = Flask(__name__)
CORS(app) # Permite que seu site no Blogger converse com seu PC

# CONFIGURAÇÕES - AJUSTE O CAMINHO DO SEU BLENDER AQUI
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))

@app.route('/renderizar', methods=['POST'])
def renderizar():
    dados = request.json
    arte_base64 = dados.get('imagem') # Imagem cortada do site
    cor_hex = dados.get('cor', '#ffffff')
    
    # 1. Salva a imagem recebida temporariamente
    caminho_arte = os.path.join(PASTA_PROJETO, "arte_recebida.png")
    with open(caminho_arte, "wb") as fh:
        fh.write(base64.b64decode(arte_base64.split(",")[1]))

    # 2. Comando para disparar o motor do Blender
    # Note que usamos o arquivo 'render_caneca.py' que você já criou
    comando = [
        BLENDER_PATH,
        "-b", os.path.join(PASTA_PROJETO, "Caneca.blend1"), # Usando seu arquivo de backup
        "-P", os.path.join(PASTA_PROJETO, "render_caneca.py"),
        "--", caminho_arte, cor_hex, "video_produzido.mp4"
    ]

    try:
        subprocess.run(comando, check=True)
        return jsonify({"status": "sucesso", "mensagem": "Vídeo renderizado com sucesso!"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)