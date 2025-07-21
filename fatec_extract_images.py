# 📦 Bibliotecas padrão
import os
import time
import json
import shutil

# 📦 Bibliotecas de terceiros
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import fitz  # PyMuPDF

# 📦 Bibliotecas da Google (genai)
from google import genai
from google.genai import types


# Carrega .env
load_dotenv()

# Armazena e Configura a API Key da Gemini
geminiai_key = os.getenv("GEMINIAI_KEY")
client = genai.Client(api_key=geminiai_key)

# Modelo da GeminiAI usado
geminiai_model = "gemini-2.5-flash"


def extrairImagens(
        anoDaProva,
        semestreDaProva,
        provaPath,
        salvarImagensNoArrayDoJSON=True
):
  try:
    prova = fitz.open(provaPath)
    prova_formatada_path = os.path.join("fatec_formatado", f"{anoDaProva}_{semestreDaProva}")
    img_extraidas_refs = set()

    print("> Extraindo imagens da prova")
    # Itera sobre as páginas (e imagens de cada página) da prova
    for pagina in prova:
      for img in pagina.get_images(full=True):
        img_ref = img[0]

        # Verifica se a imagem já não foi baixada antes
        if img_ref not in img_extraidas_refs:
          img_extraidas_refs.add(img_ref)

          # Extrai os dados da imagem
          img_data = prova.extract_image(img_ref)
          width = img_data.get("width", 0)
          height = img_data.get("height", 0)

          # Filtro para evitar baixar imagens menores (que normalmente não fazem parte de nenhuma questão)
          if width > 150 and height > 150:
            img_bytes = img_data["image"]
            img_ext = img_data["ext"]
            img_file_nome = f"img_{img_ref}.{img_ext}"

            img_extraida_path = os.path.join(prova_formatada_path, img_file_nome)

            # Salva a imagem
            with open(img_extraida_path, "wb") as file:
              file.write(img_bytes)



            # Cria aréa para escrever
            img_extraida = Image.open(img_extraida_path).convert("RGBA")
            txt_camada = Image.new("RGBA", img_extraida.size, (255, 255, 255, 0))
            txt_camada_desenho = ImageDraw.Draw(txt_camada)

            # Prepara fonte e posição do texto
            texto = str(img_ref)
            font_size = 30
            posicao = (20, 20)
            fonte = ImageFont.truetype("arial.ttf", font_size)

            # Caixa preta de fundo
            largura_texto = txt_camada_desenho.textlength(texto, font=fonte)
            altura_texto = font_size
            margem = 10
            background = (
              posicao[0] - margem, # Posição da borda ESQUERDA
              posicao[1] - margem, # Posição da borda SUPERIOR
              posicao[0] + largura_texto + margem, # Posição da borda DIREITA
              posicao[1] + altura_texto + margem # Posição da borda INFERIOR
            )
            txt_camada_desenho.rectangle(background, fill="black")

            # Escreve o ref na imagem
            txt_camada_desenho.text(posicao, texto, font=fonte, fill="red")

            # Salvar imagem com texto
            imagem_final_txt = Image.alpha_composite(img_extraida, txt_camada)
            imagem_final_txt.convert("RGB").save(os.path.join(prova_formatada_path, f"img_{img_ref}_txtcamada.{img_ext}"))



    # Salva as imagens no array de imagens de cada arquivo JSON
    if salvarImagensNoArrayDoJSON:

      # Limpa o array de imagens de todos os JSON
      for questao_json_numero in range(1, 55):
        dir_final = os.path.join(prova_formatada_path, str(questao_json_numero), f"fatec_questao{questao_json_numero}.json")
        with open(dir_final, 'r', encoding='utf-8') as f:
          questao_json = json.load(f)

        questao_json["imgs"] = []

        with open(dir_final, "w", encoding="utf-8") as f:
          json.dump(questao_json, f, indent=4, ensure_ascii=False)



      # Armazena o PROMPT de extração de imagem
      with open('prompt/geminiai-extracao-imagem.txt', 'r', encoding="utf-8") as my_file:
        prompt_imagem = my_file.read()

      # Armazena o PROMPT do JSON base
      with open('prompt/extracao-imagem-base.json', 'r', encoding="utf-8") as my_file:
        prompt_jsonImagemBase = json.load(my_file)
      # Transforma o JSON em uma String
      prompt_imagem += json.dumps(prompt_jsonImagemBase)

      # Recupera o path dos arquivos .png extraidos anteriormente
      image_files = [
        os.path.join(prova_formatada_path, img_file)
        for img_file in sorted(os.listdir(prova_formatada_path))
        if img_file.lower().endswith("txtcamada.png")
      ]

      # Prepara os arquivos para serem uploadizados no GeminiAI (imagens + prompt + pdf da prova)
      contents = (
        [types.Part.from_bytes(
          data=open(img_path, "rb").read(),
          mime_type='image/png',
        ) for img_path in image_files] +
        [prompt_imagem] +
        [types.Part.from_bytes(
          data=open(provaPath, "rb").read(),
          mime_type='application/pdf',
        )]
      )

      response = client.models.generate_content(
        model=geminiai_model,
        contents=contents
      )
      print(f"{response.usage_metadata.total_token_count} tokens usados\n")



      # Cria JSON relacionando as imagens com as suas respectivas questões
      imagem_extraida_json = response.text.replace('```json', '').replace('```', '')
      imagem_extraida_json = json.loads(imagem_extraida_json)

      # Itera sobre as imagens do JSON
      for imagem_nome, questoes_correspondentes in imagem_extraida_json["questoes"].items():
        # Itera sobre o array de questões de cada imagem do JSON
        if questoes_correspondentes is not None and len(questoes_correspondentes) > 0:
          for questao_correspondente in questoes_correspondentes:
            dir_final = os.path.join(prova_formatada_path, str(questao_correspondente),f"fatec_questao{questao_correspondente}.json")
            imagem_path = os.path.join(prova_formatada_path, str(questao_correspondente), imagem_nome).replace(os.sep, "/")

            # Pega uma imagem e armazena ela na questão (pasta) correspondente
            origem_copiar_imagem = os.path.join(prova_formatada_path, imagem_nome)
            destino_colar_imagem = os.path.join(prova_formatada_path, str(questao_correspondente))
            shutil.copy(origem_copiar_imagem, destino_colar_imagem)

            # Adiciona o caminho da imagem no JSON da questão
            with open(dir_final, 'r', encoding='utf-8') as f:
              questao_json = json.load(f)

            questao_json["imgs"].append(imagem_path)

            with open(dir_final, "w", encoding="utf-8") as f:
              json.dump(questao_json, f, indent=4, ensure_ascii=False)



      # Deleta imagens com a camada de texto (mas mantém imagens da prova no diretório geral)
      for imagem_txtcamada in os.listdir(prova_formatada_path):
        if imagem_txtcamada.lower().endswith("txtcamada.png"):
          imagem_txtcamada_path = os.path.join(prova_formatada_path, imagem_txtcamada)
          if os.path.isfile(imagem_txtcamada_path):
            os.remove(imagem_txtcamada_path)



  except Exception as e:
    print(f"[IMAGEM] Erro inesperado: {e}")
    time.sleep(6)