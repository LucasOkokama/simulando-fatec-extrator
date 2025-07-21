# 📦 Bibliotecas padrão
import os
import time
import json
import pathlib

# 📦 Bibliotecas de terceiros
from dotenv import load_dotenv

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


def formatarQuestoes(
        anoDaProva,
        semestreDaProva,
        provaPath,
        gabaritoPath,
        questaoInicial=1,
        questoesSelecionadas=None
):
  try:
    # Array contendo os arquivos (PDF's)
    files = [
      pathlib.Path(provaPath),
      pathlib.Path(gabaritoPath),
    ]

    # Armazena o PROMPT geral
    with open('prompt/geminiai-extracao-questao.txt', 'r', encoding="utf-8") as my_file:
      prompt_questao = my_file.read()

    # Armazena o PROMPT do JSON base
    with open('prompt/questao-base.json', 'r', encoding="utf-8") as my_file:
      prompt_jsonBase = json.load(my_file)
    # Transforma o JSON em uma String
    prompt_jsonBase_string = json.dumps(prompt_jsonBase)

    # Loop para gerar o JSON das 54 Questões
    for num_questao in range(questaoInicial, 55):
      if questoesSelecionadas is None or num_questao in questoesSelecionadas:
        try:
          # Retorna o JSON da questão formatada
          print(f"> Criando JSON da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
          prompt = f"Faça tudo isso utilizando como base a questão de número {num_questao:02}\n\n"
          prompt += prompt_questao
          prompt += prompt_jsonBase_string
          response = client.models.generate_content(
            model=geminiai_model,
            contents=[
              prompt,
              types.Part.from_bytes(
                data=files[0].read_bytes(),
                mime_type='application/pdf',
              ),
              types.Part.from_bytes(
                data=files[1].read_bytes(),
                mime_type='application/pdf',
              )
            ]
          )
          print(f"{response.usage_metadata.total_token_count} tokens usados\n")

          # Remove as marcações do "fenced code block" (aspas triplas)
          questao_formatada = response.text.replace('```json', '').replace('```', '')

          # Passa de string (com formatação JSON) para um dicionário do Python
          questao_formatada = json.loads(questao_formatada)

          # Adiciona valores à alguns campos
          questao_formatada['prova']['id']['ano'] = anoDaProva
          questao_formatada['prova']['id']['semestre'] = semestreDaProva
          questao_formatada['numQuestao'] = num_questao



          # Diretório onde o arquivo será salvo
          prova_questao_path = f"fatec_formatado/{anoDaProva}_{semestreDaProva}/{num_questao}"
          os.makedirs(prova_questao_path, exist_ok=True)

          # Salva o arquivo JSON no caminho especificado
          dir_final = os.path.join(prova_questao_path, f"fatec_questao{num_questao}.json")
          with open(dir_final, 'w', encoding='utf-8') as file:
            json.dump(questao_formatada, file, indent=4, ensure_ascii=False)


          time.sleep(6)

        except Exception as e:
          # Mostra o erro e permite continuação da execução
          print(f">>> Erro ao processar a questão {num_questao}: {e}<<<\n\n\n")
          time.sleep(6)

  except Exception as e:
    print(f"[QUESTÃO_JSON] Erro inesperado: {e}")
    time.sleep(6)