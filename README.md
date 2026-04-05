# 🚀 Mug Render Engine Pro (Python + Blender)

Este é um motor de renderização automatizado para mockups de canecas 3D. O sistema utiliza **Flask** para receber dados de um site e o **Blender** para processar vídeos em alta fidelidade.

## 🛠️ Como Funciona?
1. O usuário ajusta a arte e a cor da caneca no site (Blogger/HTML).
2. O site envia os dados para o servidor local Python (`servidor_render.py`).
3. O Python dispara o Blender em background, troca as texturas e gera o vídeo 360°.
4. O vídeo final é salvo automaticamente na pasta do projeto.

## 📦 Requisitos
- Blender 4.0 (ou superior) instalado.
- Python 3.x.
- Bibliotecas: `pip install flask flask-cors`

## 🚀 Como Executar
1. Certifique-se de que o Blender está no caminho: `C:\Program Files\Blender Foundation\Blender 4.0\blender.exe`
2. Execute o servidor:
   ```bash
   python servidor_render.py
