import bpy
import os
import sys

def renderizar_video_premium(caminho_arte, cor_hex_caneca, nome_saida):
    # 1. Abre o seu modelo oficial
    # Certifique-se que o arquivo .blend está na mesma pasta
    bpy.ops.wm.open_mainfile(filepath="seu_modelo_caneca.blend")
    
    # 2. Converte HEX para RGB (Blender usa 0.0 a 1.0)
    hex_color = cor_hex_caneca.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4)) + (1,)

    # 3. Aplica a Arte do Cliente
    material_arte = bpy.data.materials.get("Cor_Arte")
    if material_arte:
        # Localiza o nó de imagem e carrega a nova arte
        nodes = material_arte.node_tree.nodes
        tex_node = nodes.get("Textura de Imagem") # Nome que demos no Blender
        if tex_node:
            nova_img = bpy.data.images.load(caminho_arte)
            tex_node.image = nova_img

    # 4. Aplica a Cor da Caneca
    mat_caneca = bpy.data.materials.get("Cor_caneca")
    if mat_caneca:
        mat_caneca.node_tree.nodes["Principled BSDF"].inputs[0].default_value = rgb

    # 5. Configura a Animação (360 graus)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120 # 4 segundos a 30fps
    
    # Configura a saída para MP4 de alta qualidade
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH' # Qualidade máxima
    scene.render.filepath = os.path.join(os.getcwd(), nome_saida)

    # 6. Roda o Render
    print("Iniciando renderização de luxo...")
    bpy.ops.render.render(animation=True)
    print(f"Vídeo salvo como: {nome_saida}")

# Para rodar via linha de comando:
# blender -b -P render_caneca.py -- "caminho/da/arte.png" "#FF0000" "resultado.mp4"