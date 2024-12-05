
# Executar o seguinte comando:
# pip install -q -U google-generativeai

import google.generativeai as genai
import json
import re
import os
import time



def upload_pdf(path, mime_type=None):
  # Carrega os arquivos para serem utilizados pelo Gemini
  file = genai.upload_file(path, mime_type=mime_type)
  # Mostra que o arquivo foi carregado com sucesso
  print(f"Arquivo carregado '{file.display_name}' como: {file.uri}")
  return file

def fatecFormatarQuestoes(anoDaProva, semestreDaProva):
  try:
    # Diretório para onde as questões FORMATADAS irão
    dir_questions_json = f"vestibulares/fatec/fatecFormatado/{anoDaProva}_{semestreDaProva}"
    # Cria o diretório se ele não existir
    os.makedirs(dir_questions_json, exist_ok=True)

    # Resgatando a API key do Gemini
    with open('gemini-api-key.txt', 'r', encoding='utf-8') as api_key_txt:
      # Armazena a API Key do Gemini
      gemini_api_key = api_key_txt.read();

      # Configura a API Key
      genai.configure(api_key=gemini_api_key)

      # Cria a configuração de modelo da IA
      generation_config = {
        "temperature": 0.1,
        "top_p": 0.1,
        "top_k": 1,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
      }

      # Define o modelo da IA
      model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
      )

      # Array contendo os arquivos (PDF's)
      files = [
        upload_pdf(f"vestibulares/fatec/pdf/fatecProva_{anoDaProva}_{semestreDaProva}.pdf", mime_type="application/pdf"),
        upload_pdf(f"vestibulares/fatec/pdf/fatecGabarito_{anoDaProva}_{semestreDaProva}.pdf", mime_type="application/pdf"),
      ]

      print("\n\n\n")


      with open('vestibulares/fatec/prompt-enunciado-pergunta-alternativas.txt', 'r', encoding="utf-8") as prompt_pedido_txt_file:
        # Armazena o pedido
        prompt_pedido = prompt_pedido_txt_file.read()

      with open('vestibulares/fatec/prompt-enunciadoExtra.txt', 'r', encoding="utf-8") as prompt_enunciadoExtra_txt_file:
        # Armazena o pedido
        prompt_enunciadoExtra = prompt_enunciadoExtra_txt_file.read()

      with open('question_formatted.json', 'r', encoding="utf-8") as prompt_question_json_file:
        # Armazena o JSON
        prompt_json_modelo = json.load(prompt_question_json_file)

      # Transforma o JSON em uma String e junta com o pedido
      prompt_json_modelo = json.dumps(prompt_json_modelo)


      for num_questao in range(1, 55):
        try:
          # Preenche um JSON com os valores de uma determinada questão
          prompt_modelo = f"Faça tudo isso utilizando como base a questão de número {num_questao:02}\n\n"
          prompt_modelo += prompt_pedido
          prompt_modelo += prompt_json_modelo
          response_JSON = model.generate_content([prompt_modelo, files[0]])
          print(f"> Criando JSON da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
          # Retorna o custo de Token da requisição
          print(response_JSON.usage_metadata)

          # Retorna o texto de suporte de uma determinada questão
          prompt_modelo = f"Faça isso para a questão {num_questao:02}\n\n"
          prompt_modelo += prompt_enunciadoExtra
          response_EnunciadoExtra = model.generate_content([prompt_modelo, files[0]])
          print(f"> Identificando o texto de suporte da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
          # Retorna o custo de Token da requisição
          print(response_EnunciadoExtra.usage_metadata)

          # Retorna somente a disciplina de uma determinada questão
          prompt_Disciplina = f"Me retorne somente a disciplina da questão {num_questao:03}"
          response_Disciplina = model.generate_content([prompt_Disciplina, files[1]])
          print(f"> Identificando disciplina da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
          # Retorna o custo de Token da requisição
          print(response_Disciplina.usage_metadata)

          # Retorna somente o gabarito de uma determinada questão
          prompt_Gabarito = f"Me retorne somente o gabarito da questão {num_questao:03}"
          response_Gabarito = model.generate_content([prompt_Gabarito, files[1]])
          print(f"> Identificando gabarito da questao {num_questao} ({anoDaProva}/{semestreDaProva})")
          # Retorna o custo de Token da requisição
          print(response_Gabarito.usage_metadata)
          print("\n")


          # Remove as marcações do "fenced code block" (aspas triplas)
          questao_formatada_json = response_JSON.text.replace('```json', '').replace('```', '')


          # Passa de string (com formatação JSON) para um dicionario do Python
          questao_formatada_json = json.loads(questao_formatada_json)

          # Adiciona valores à alguns campos
          questao_formatada_json['ano'] = anoDaProva
          questao_formatada_json['vestibular'] = 2
          questao_formatada_json['semestre'] = semestreDaProva
          questao_formatada_json['disciplina'] = response_Disciplina.text
          questao_formatada_json['gabarito'] = response_Gabarito.text

          if response_EnunciadoExtra.text != "Nao_Existe":
            backup_enunciado = questao_formatada_json['enunciado']
            questao_formatada_json['enunciado'] = response_EnunciadoExtra.text
            if backup_enunciado is not None:
              questao_formatada_json['enunciado'] += "\n\n"
              questao_formatada_json['enunciado'] += backup_enunciado


          if(questao_formatada_json['enunciado'] is not None):
            # Substitui os "\n" por "<br>"
            questao_formatada_json['enunciado'] = questao_formatada_json['enunciado'].replace('\n', '<br>')

          if(questao_formatada_json['pergunta'] is not None):
            # Substitui os "\n" por "<br>"
            questao_formatada_json['pergunta'] = questao_formatada_json['pergunta'].replace('\n', '<br>')


          # # Salva o caminho para onde a questão formatada deve ir
          dir_questions_number_json = os.path.join(dir_questions_json, str(num_questao))
          # # Cria esse caminho caso ele não exista
          os.makedirs(dir_questions_number_json, exist_ok=True)

          # # Salva o arquivo json no caminho especificado
          path_json_formatted = os.path.join(dir_questions_number_json, f"fatec_questao{num_questao}.json")
          with open(path_json_formatted, 'w') as path_json_formatted:
            # Passa o questao_formatada_json para JSON e salvar em um arquivo
            json.dump(questao_formatada_json, path_json_formatted, indent=4, ensure_ascii=False)


          time.sleep(3)

        except Exception as e:
          # Mostra o erro e permite continuação da execução
          print(f">>> Erro ao processar a questão {num_questao}: {e}")
          time.sleep(3)

  except FileNotFoundError:
    # Tratamento para arquivo não encontrado
    print("Erro: O arquivo não foi encontrado.")

  except PermissionError:
    # Tratamento para erro de permissão
    print("Erro: Permissão negada para abrir o arquivo.")

  except Exception as e:
    # Tratamento genérico para outros erros
    print(f"Erro inesperado: {e}")