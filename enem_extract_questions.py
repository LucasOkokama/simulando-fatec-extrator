import requests
import json
import os
import time


def enemExtrairQuestoes(anoDaProva):
  # URL da API do Enem
  urlSelfHosting = f"http://localhost:3000/v1/exams/{anoDaProva}/questions/"
  '''
  Hostear servidor para evitar rate limit:
  -> Fazer deploy da api: https://github.com/yunger7/enem-api
      Instruções da doc: https://docs.enem.dev/self-hosting

  -> lib/api/rate-limit.ts
      Aumentar numero máximo de requisições
        linha 11
        antes ===>  this.maxRequests = maxRequests || 10;
        depois ===> this.maxRequests = 10000;
  '''

  urlWebsite = f"https://api.enem.dev/v1/exams/{anoDaProva}/questions/"
  '''
  Se não for hostear:
  -> Trocar "urlSelfHosting" para "urlWebsite" no código
  -> Descomentar o ultimo bloco para habilitar o cooldown
  '''

  # Diretorio para onde as questoes irão
  dir_questions = "vestibulares/enem"
  # Diretorio para onde as imagens irão
  dir_images = f"vestibulares/enemFormatado/{anoDaProva}"

  # Cria o diretório se ele não existir
  os.makedirs(dir_questions, exist_ok=True)
  os.makedirs(dir_images, exist_ok=True)

  # Número da ultima questões a ser extraida
  num_questions = 180

  for i in range(1, num_questions + 1):
    
    # Modifica a URL para buscar a questão com índice específico
    response = requests.get(f"{urlSelfHosting}{i}")

    # Se a requisição deu certo (code 200)
    if response.status_code == 200:
      # Cria arquivo cujo nome sera construido com base no índice da questão
      # O arquivo criado já é juntado com o "dir_questions" para ir para o local correto
      question_path = os.path.join(dir_questions, f"enem_questao{i}.txt")

      # Converte o texto da questão para um dicionário (para facilitar na formatação)
      question_data = json.loads(response.text)

      # Salva o conteúdo no path/arquivo.extensão com nome definido acima
      with open(question_path, "w", encoding="utf-8")  as question_path:
        # Converte dicionario para json e escreve os dados formatados no arquivo
        json.dump(question_data, question_path, ensure_ascii=False, indent=4)

      # Mensagem de sucesso
      # print(f"Questão {i} salva em {question_path}")




      # Salvando imagens da questao
      img_index = 1
      # Verifica se key 'files' existe no dicionario 'question_data'
      if 'files' in question_data:
        # Cria um loop que itera sobre cada item de 'files' (ou seja, cada imagem)
        for img_url in question_data['files']:
          # Faz um request get para pegar a url da img
          img_response = requests.get(img_url)

          # Se a requisição deu certo (code 200)
          if img_response.status_code == 200:
            # Completa o path criando uma pasta para cada questão
            dir_images_mais_questao = os.path.join(dir_images, str(i))
            os.makedirs(dir_images_mais_questao, exist_ok=True)

            # Cria o path da imagem levando em consideração o index da img e da questao
            img_path = os.path.join(dir_images_mais_questao, f"enem_questao{i}_img{img_index}.png")

            # Salva o conteúdo no path/arquivo.extensão com nome definido acima
            with open(img_path, "wb") as img_path:
              img_path.write(img_response.content)

            # Mensagem de sucesso
            # print(f"> Imagem {img_index} salva em {img_path}")
            # Avança o index de imagem
            img_index+=1




      if 'alternatives' in question_data:
        for alternativa_index in range (len(question_data['alternatives'])):
          alter_img_url = question_data['alternatives'][alternativa_index]['file']

          if alter_img_url:
            alter_img_url_response = requests.get(alter_img_url)
            if alter_img_url_response.status_code == 200: 
              # Completa o path criando uma pasta para cada questão
              dir_images_mais_questao = os.path.join(dir_images, str(i))
              os.makedirs(dir_images_mais_questao, exist_ok=True)

              # Cria o path da img da alternativa levando em consideração o index da questao
              alter_letra = question_data['alternatives'][alternativa_index]['letter']
              alter_img_path = os.path.join(dir_images_mais_questao, f"enem_questao{i}_alter-{alter_letra}.png")

              with open(alter_img_path, "wb") as alter_img_path:
                alter_img_path.write(alter_img_url_response.content)

              # Mensagem de sucesso
              # print(f">> Imagem da Alternativa '{alter_letra}' salva em {alter_img_path}")




    else:
      # Mensagem de erro
      print(f"Falha ao obter a questão {i}: Status_Code {response.status_code}")


    # Espaçamento para facilitar leitura do console
    print("\n")



    # Espera 10 segundos a cada 10 iterações
    # if i % 10 == 0:
    #     print("\n\nAGUARDA 10 SEGUNDOS PARA NÃO ESTOURAR O LIMITE DE REQUISIÇÕES!\n\n\n")
    #     time.sleep(10)