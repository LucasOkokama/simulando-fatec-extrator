import requests
import json
import os

# Variaveis de Configuração
__anoDaProva = 2023


# URL da API do Enem
url = f"https://api.enem.dev/v1/exams/{__anoDaProva}/questions/"
# Diretorio para onde as questoes irão
dir_questions = "vestibulares/enem"

# Cria o diretório se ele não existir
os.makedirs(dir_questions, exist_ok=True)

# Número da ultima questões a ser extraida
num_questions = 15

for i in range(10, num_questions + 1):
    # Modifica a URL para buscar a questão com índice específico
    response = requests.get(f"{url}{i}")

    # Se a requisição deu certo (code 200)
    if response.status_code == 200:
        # Cria arquivo cujo nome sera construido com base no índice da questão
        # O arquivo criado já é juntado com o "dir_questions" para ir para o local correto
        question_path = os.path.join(dir_questions, f"questoes_enem_{i}.txt")

        # Converte o texto da questão para um dicionário (para facilitar na formatação)
        question_data = json.loads(response.text)

        # Salva o conteúdo no arquivo com nome definido acima
        with open(question_path, "w", encoding="utf-8")  as question_path:
            # Converte dicionario para json e escreve os dados formatados no arquivo
            json.dump(question_data, question_path, ensure_ascii=False, indent=4)

        # Mensagem de sucesso
        print(f"Questão {i} salva em {question_path}")
    else:
        # Mensagem de erro
        print(f"Falha ao obter a questão {i}: Status_Code {response.status_code}")