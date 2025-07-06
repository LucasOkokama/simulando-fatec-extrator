
# Executar o seguinte comando:
# pip install -q -U google-genai
from google import genai
from google.genai import types

import pathlib
from dotenv import load_dotenv
import json
import re
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

    # Diretório da pasta da prova
    dir_prova = f"fatec_formatado/{anoDaProva}_{semestreDaProva}"
    os.makedirs(dir_prova, exist_ok=True)



    # Array contendo os arquivos (PDF's)
    files = [
      pathlib.Path(provaPath),
      pathlib.Path(gabaritoPath),
    ]

    # Armazena o PROMPT do Enunciado, Pergunta e Alternativas
    with open('prompt/prompt-enunciado-pergunta-alternativas.txt', 'r', encoding="utf-8") as my_file:
      prompt_enunciado_pergunta_alternativa = my_file.read()

    # Armazena o PROMPT do Enunciado extra
    with open('prompt/prompt-enunciadoExtra.txt', 'r', encoding="utf-8") as my_file:
      prompt_enunciadoExtra = my_file.read()

    # Armazena o PROMPT do JSON base
    with open('prompt/question-formatted.json', 'r', encoding="utf-8") as my_file:
      prompt_jsonBase = json.load(my_file)

    # Transforma o JSON em uma String
    prompt_jsonBase_string = json.dumps(prompt_jsonBase)



    # Loop para gerar o JSON das 54 Questões
    for num_questao in range(1, 55):
      try:
        # Retorna o Enunciado, Pergunta e Alternativa
        print(f"> Criando JSON da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
        prompt = f"Faça tudo isso utilizando como base a questão de número {num_questao:02}\n\n"
        prompt += prompt_enunciado_pergunta_alternativa
        prompt += prompt_jsonBase_string
        response = client.models.generate_content(
          model=geminiai_model,
          contents=[
            prompt,
            types.Part.from_bytes(
              data=files[0].read_bytes(),
              mime_type='application/pdf',
            )
          ]
        )
        print(f"{response.usage_metadata.total_token_count} tokens usados")


        # Retorna o Enunciado extra (texto de suporte)
        print(f"> Identificando o texto de suporte da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
        prompt = f"Faça isso para a questão {num_questao:02}\n\n"
        prompt += prompt_enunciadoExtra
        response_EnunciadoExtra = client.models.generate_content(
          model=geminiai_model,
          contents=[
            prompt,
            types.Part.from_bytes(
              data=files[0].read_bytes(),
              mime_type='application/pdf',
            )
          ]
        )
        print(f"{response_EnunciadoExtra.usage_metadata.total_token_count} tokens usados")


        # Retorna somente a disciplina de uma determinada questão
        print(f"> Identificando disciplina da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
        prompt_Disciplina = (f"Me retorne somente a disciplina da questão {num_questao:03}, sendo ela representado somente por "
                             f"Matemática, Português, Física, Química, Biologia, História, Geografia, Inglês, Raciocínio Lógico ou Multidisciplinar")
        response_Disciplina = client.models.generate_content(
          model=geminiai_model,
          contents=[
            prompt_Disciplina,
            types.Part.from_bytes(
              data=files[1].read_bytes(),
              mime_type='application/pdf',
            )
          ]
        )
        print(f"{response_Disciplina.usage_metadata.total_token_count} tokens usados")


        # Retorna somente o gabarito de uma determinada questão
        print(f"> Identificando gabarito da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
        prompt_Gabarito = f"Me retorne somente o gabarito da questão {num_questao:03}, sendo ele representado somente por A, B, C, D ou E"
        response_Gabarito = client.models.generate_content(
          model=geminiai_model,
          contents=[
            prompt_Gabarito,
            types.Part.from_bytes(
              data=files[1].read_bytes(),
              mime_type='application/pdf',
            )
          ]
        )
        print(f"{response_Gabarito.usage_metadata.total_token_count} tokens usados")
        print("\n")



        # Remove as marcações do "fenced code block" (aspas triplas)
        questao_formatada_json = response.text.replace('```json', '').replace('```', '')

        # Passa de string (com formatação JSON) para um dicionario do Python
        questao_formatada_json = json.loads(questao_formatada_json)



        # Adiciona valores à alguns campos
        questao_formatada_json['prova']['id']['ano'] = anoDaProva
        questao_formatada_json['prova']['id']['semestre'] = semestreDaProva
        questao_formatada_json['disciplina'] = response_Disciplina.text
        questao_formatada_json['gabarito'] = response_Gabarito.text

        if response_EnunciadoExtra.text != "Nao_Existe":
          backup_enunciado = questao_formatada_json['enunciado']
          questao_formatada_json['enunciado'] = response_EnunciadoExtra.text
          if (backup_enunciado is not None) and (backup_enunciado != response_EnunciadoExtra.text):
            questao_formatada_json['enunciado'] += "\n\n"
            questao_formatada_json['enunciado'] += backup_enunciado



        # Substitui "\n" por "<br>"
        if(questao_formatada_json['enunciado'] is not None):
          # Substitui os "\n" por "<br>"
          questao_formatada_json['enunciado'] = questao_formatada_json['enunciado'].replace('\n', '<br>')

        if(questao_formatada_json['pergunta'] is not None):
          # Substitui os "\n" por "<br>"
          questao_formatada_json['pergunta'] = questao_formatada_json['pergunta'].replace('\n', '<br>')



        # Diretório para onde as questões formatada devem ir
        dir_questao_numero_json = os.path.join(dir_prova, str(num_questao))
        os.makedirs(dir_questao_numero_json, exist_ok=True)

        # Salva o arquivo json no caminho especificado
        dir_final = os.path.join(dir_questao_numero_json, f"fatec_questao{num_questao}.json")
        with open(dir_final, 'w', encoding='utf-8') as dir_final:
          # Passa o questao_formatada_json para JSON e salvar em um arquivo
          json.dump(questao_formatada_json, dir_final, indent=4, ensure_ascii=False)


        time.sleep(5)

      except Exception as e:
        # Mostra o erro e permite continuação da execução
        print(f">>> Erro ao processar a questão {num_questao}: {e}<<<\n\n\n")
        time.sleep(5)

  except FileNotFoundError:
    # Tratamento para arquivo não encontrado
    print("Erro: O arquivo não foi encontrado.")

  except PermissionError:
    # Tratamento para erro de permissão
    print("Erro: Permissão negada para abrir o arquivo.")

  except Exception as e:
    # Tratamento genérico para outros erros
    print(f"Erro inesperado: {e}")