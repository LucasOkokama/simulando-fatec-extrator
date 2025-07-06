from google import genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
import json
import os
import time

# Carrega .env
load_dotenv()


def fatecFormatarQuestoes(anoDaProva, semestreDaProva, provaPath, gabaritoPath):
  try:
    # Modelo da GeminiAI usado
    geminiai_model = "gemini-2.0-flash"

    # Armazena e Configura a API Key da Gemini
    geminiai_key = os.getenv("GEMINIAI_KEY")
    client = genai.Client(api_key=geminiai_key)



    # Array contendo os arquivos (PDF's)
    files = [
      pathlib.Path(provaPath),
      pathlib.Path(gabaritoPath),
    ]

    # Armazena o PROMPT do Enunciado, Pergunta e Alternativas
    with open('prompt/geminiai-prompt.txt', 'r', encoding="utf-8") as my_file:
      prompt_questao = my_file.read()

    # Armazena o PROMPT do JSON base
    with open('prompt/questao-base-prompt.json', 'r', encoding="utf-8") as my_file:
      prompt_jsonBase = json.load(my_file)
    # Transforma o JSON em uma String
    prompt_jsonBase_string = json.dumps(prompt_jsonBase)



    # Loop para gerar o JSON das 54 Questões
    for num_questao in range(1, 55):
      try:
        # Retorna o Enunciado, Pergunta e Alternativa
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

        # Passa de string (com formatação JSON) para um dicionario do Python
        questao_formatada = json.loads(questao_formatada)

        # Adiciona valores à alguns campos
        questao_formatada['prova']['id']['ano'] = anoDaProva
        questao_formatada['prova']['id']['semestre'] = semestreDaProva
        questao_formatada['numQuestao'] = num_questao



        # Diretório onde o arquivo será salvo
        dir_prova_questao = f"fatec_formatado/{anoDaProva}_{semestreDaProva}/{num_questao}"
        os.makedirs(dir_prova_questao, exist_ok=True)

        # Salva o arquivo JSON no caminho especificado
        dir_final = os.path.join(dir_prova_questao, f"fatec_questao{num_questao}.json")
        with open(dir_final, 'w', encoding='utf-8') as file:
          json.dump(questao_formatada, file, indent=4, ensure_ascii=False)



        time.sleep(6)

      except Exception as e:
        # Mostra o erro e permite continuação da execução
        print(f">>> Erro ao processar a questão {num_questao}: {e}<<<\n\n\n")
        time.sleep(6)

  except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado.")

  except PermissionError:
    print("Erro: Permissão negada para abrir o arquivo.")

  except Exception as e:
    print(f"Erro inesperado: {e}")