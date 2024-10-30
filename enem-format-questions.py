import json
import os


# Variáveis de Configuração
__anoDaProva = 2023

# Diretório para acessar as questões NÃO FORMATADAS
dir_questions_txt = "vestibulares/enem"
# Diretório para onde as questões FORMATADAS irão
dir_questions_json = f"vestibulares/enemFormatado/{__anoDaProva}"

# Cria o diretório se ele não existir
os.makedirs(dir_questions_txt, exist_ok=True)
os.makedirs(dir_questions_json, exist_ok=True)

# Número da última questões a ser extraida
num_questions = 5

for i in range(1, num_questions + 1):
    path_questions = os.path.join(dir_questions_txt, f"enem_questao{i}.txt")

    try:
        with open(path_questions, 'r') as path_questions:
            question_json =  json.load(path_questions)

    except json.JSONDecodeError as error:
        print("O conteúdo do arquivo não está em um formato JSON válido.\n", error);
        question_json = None;