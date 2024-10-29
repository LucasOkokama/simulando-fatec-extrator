import requests
import json
import os
import time

# Variaveis de Configuração
__anoDaProva = 2023


# URL da API do Enem
url = f"https://api.enem.dev/v1/exams/{__anoDaProva}/questions/"
# Diretorio para onde as questoes irão
dir_questions = "vestibulares/enem"
# Diretorio para onde as imagens irão
dir_images = f"vestibulares/enemFormatado/{__anoDaProva}"

# Cria o diretório se ele não existir
os.makedirs(dir_questions, exist_ok=True)
os.makedirs(dir_images, exist_ok=True)

# Número da ultima questões a ser extraida
num_questions = 180

for i in range(1, num_questions + 1):

    # Modifica a URL para buscar a questão com índice específico
    response = requests.get(f"{url}{i}")

    # Se a requisição deu certo (code 200)
    if response.status_code == 200:
        # Cria arquivo cujo nome sera construido com base no índice da questão
        # O arquivo criado já é juntado com o "dir_questions" para ir para o local correto
        question_path = os.path.join(dir_questions, f"questao_enem_{i}.txt")

        # Converte o texto da questão para um dicionário (para facilitar na formatação)
        question_data = json.loads(response.text)

        # Salva o conteúdo no path/arquivo.extensão com nome definido acima
        with open(question_path, "w", encoding="utf-8")  as question_path:
            # Converte dicionario para json e escreve os dados formatados no arquivo
            json.dump(question_data, question_path, ensure_ascii=False, indent=4)

        # Mensagem de sucesso
        print(f"Questão {i} salva em {question_path}")




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
                    # Cria o path da imagem levando em consideração o index da img
                    img_path = os.path.join(dir_images, f"img_{img_index}_enem_{i}.png")

                    # Salva o conteúdo no path/arquivo.extensão com nome definido acima
                    with open(img_path, "wb") as img_path:
                        img_path.write(img_response.content)

                    # Mensagem de sucesso
                    print(f"> Imagem {img_index} salva em {img_path}")
                    # Avança o index de imagem
                    img_index+=1
    else:
        # Mensagem de erro
        print(f"Falha ao obter a questão {i}: Status_Code {response.status_code}")


    # Espaçamento para facilitar leitura do console
    print("\n")



    # Espera 2 segundos a cada 10 iterações
    if i % 10 == 0:
        print("\n\nAGUARDA 7 SEGUNDOS PARA NÃO ESTOURAR O LIMITE DE REQUISIÇÕES!\n\n\n")
        time.sleep(7)