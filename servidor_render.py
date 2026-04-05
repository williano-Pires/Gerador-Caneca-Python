from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import base64

app = Flask(__name__)
CORS(app) # Isso permite que o seu site no Blogger envie dados para o seu PC

# ==========================================================
# CONFIGURAÇÕES - VERIFIQUE SE O CAMINHO DO BLENDER ESTÁ CORRETO
# ==========================================================
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BLEND = "Caneca Teste.blend" # Nome exato do seu arquivo na pasta
ARQUIVO_MOTOR = "render_caneca.py"   # Nome do seu script de render
# ==========================================================

@app.route('/renderizar', methods=['POST'])
def renderizar():
    try:
        dados = request.json
        arte_base64 = dados.get('imagem') # Imagem que vem do Cropper do site
        cor_hex = dados.get('cor', '#ffffff')
        
        if not arte_base64:
            return jsonify({"status": "erro", "mensagem": "Nenhuma imagem recebida"}), 400

        # 1. Salva a imagem recebida temporariamente para o Blender ler
        caminho_arte = os.path.join(PASTA_PROJETO, "arte_recebida.png")
        with open(caminho_arte, "wb") as fh:
            # Remove o cabeçalho 'data:image/png;base64,' se existir
            if "," in arte_base64:
                header, data = arte_base64.split(",")
                fh.write(base64.b64decode(data))
            else:
                fh.write(base64.b64decode(arte_base64))

        # 2. Monta o comando para o Blender
        # Usamos caminhos absolutos para evitar erros de "arquivo não encontrado"
        caminho_full_blend = os.path.join(PASTA_PROJETO, ARQUIVO_BLEND)
        caminho_full_motor = os.path.join(PASTA_PROJETO, ARQUIVO_MOTOR)
        nome_video_saida = "video_produzido.mp4"

        comando = [
            BLENDER_PATH,
            "-b", caminho_full_blend,
            "-P", caminho_full_motor,
            "--", caminho_arte, cor_hex, nome_video_saida
        ]

        print(f"\n🚀 DISPARANDO RENDERIZAÇÃO...")
        print(f"🎨 Cor: {cor_hex} | 🖼️ Arte salva em: {caminho_arte}")

        # 3. Executa o Blender em segundo plano
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        
        print("✅ BLENDER FINALIZOU COM SUCESSO!")
        return jsonify({
            "status": "sucesso", 
            "mensagem": "Vídeo renderizado com qualidade profissional!",
            "arquivo": nome_video_saida
        })

    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO NO BLENDER:\n{e.stderr}")
        return jsonify({"status": "erro", "mensagem": "Erro interno no Blender. Verifique o terminal."}), 500
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   MOTOR DE RENDERIZAÇÃO ATIVO E AGUARDANDO SITE")
    print("   Endereço: http://127.0.0.1:5000/renderizar")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
