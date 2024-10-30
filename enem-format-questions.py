import json
import os
import re


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
num_questions = 110

for i in range(110, num_questions + 1):
    path_questions = os.path.join(dir_questions_txt, f"enem_questao{i}.txt")

    try:
        with open(path_questions, 'r') as path_questions:
            question_json =  json.load(path_questions)

            question_json_formatted = {
                "vestibular": 1,
                "ano": question_json['year'],
                "num_questao": question_json['index'],
                "disciplina": question_json['discipline'],
                "enunciado": question_json['context'],
                "imgs": [],
                "pergunta": question_json['alternativesIntroduction'],
                "gabarito": question_json['correctAlternative'],
                "alternativas": []
            }


            dir_questions_number_json = os.path.join(dir_questions_json, str(i))
            os.makedirs(dir_questions_number_json, exist_ok=True)

            pattern_img_questao = re.compile(r'.*img\d+\.png$')
            '''
            .* ==> O "." representa qualquer caractere, e o "*" significa "zero ou mais vezes"
            img ==> indica literalmente a palavra "img"
            \d+ ==> corresponde a um ou mais dígitos (2, 45, 856, etc)
            \.png ==>  indica literalmente a palavra ".png" 
            $ ==> indica o fim da string
            '''

            for arquivo in sorted(os.listdir(dir_questions_number_json)):
                if pattern_img_questao.match(arquivo):
                    path_image_complete = os.path.join(dir_questions_number_json, arquivo)
                    question_json_formatted['imgs'].append(path_image_complete)


            for alternativa in question_json['alternatives']:
                alternativa_formatted = {
                    "alter_letra": alternativa['letter'],
                    "alter_texto": alternativa['text'],
                    "alter_img": []
                }

                pattern_img_alternativa = re.compile(rf'.*alter-{alternativa['letter']}\.png$')
                for arquivo in sorted(os.listdir(dir_questions_number_json)):
                    if pattern_img_alternativa.match(arquivo):
                        path_image_complete = os.path.join(dir_questions_number_json, arquivo)
                        alternativa_formatted['alter_img'].append(path_image_complete)
                        break;

                question_json_formatted['alternativas'].append(alternativa_formatted);

    except json.JSONDecodeError as error:
        print("O conteúdo do arquivo não está em um formato JSON válido.\n", error)
        question_json = None