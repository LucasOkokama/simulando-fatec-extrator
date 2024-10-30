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
num_questions = 180

for i in range(1, num_questions + 1):
    # Salva o caminho de uma questão específica (.txt)
    path_questions = os.path.join(dir_questions_txt, f"enem_questao{i}.txt")

    try:
        with open(path_questions, 'r') as path_questions:
            # Converte o txt em um dict
            question_dict =  json.load(path_questions)

            # Cria o dict formatado da questão e preenche alguns valores
            question_dict_formatted = {
                "vestibular": 1,
                "ano": question_dict['year'],
                "num_questao": question_dict['index'],
                "disciplina": question_dict['discipline'],
                "enunciado": question_dict['context'],
                "imgs": [],
                "pergunta": question_dict['alternativesIntroduction'],
                "gabarito": question_dict['correctAlternative'],
                "alternativas": []
            }

            # Salva o caminho para onde a questão formatada deve ir
            dir_questions_number_json = os.path.join(dir_questions_json, str(i))
            # Cria esse caminho caso ele não exista
            os.makedirs(dir_questions_number_json, exist_ok=True)

            # Regex para encontrar arquivos com nomes específicos. Eles são as imagens da questão
            pattern_img_questao = re.compile(r'.*img\d+\.png$')
            #   .* ==> O "." representa qualquer caractere, e o "*" significa "zero ou mais vezes"
            #   img ==> indica literalmente a palavra "img"
            #   \d+ ==> corresponde a um ou mais dígitos (2, 45, 856, etc)
            #   \.png ==>  indica literalmente a palavra ".png"
            #   $ ==> indica o fim da string


            # Itera sobre todos os arquivos que estão na pasta da questão
            # Organiza esses arquivos em ordem alfabética
            for arquivo in sorted(os.listdir(dir_questions_number_json)):
                # Se o padrão Regex for respeitado...
                if pattern_img_questao.match(arquivo):
                    # Salva o caminho do arquivo encontado
                    path_image_complete = os.path.join(dir_questions_number_json, arquivo)
                    # Armazena esse caminho no array 'imgs' do dict formatado
                    question_dict_formatted['imgs'].append(path_image_complete)


            # Itera sobre os objetos (dicts) da list 'alternatives'
            for alternativa in question_dict['alternatives']:
                # Cria um dict com base nos dados presentes nos dicts da list 'alternatives'
                alternativa_formatted = {
                    "alter_letra": alternativa['letter'],
                    "alter_texto": alternativa['text'],
                    "alter_img": []
                }

                # Regex para encontrar arquivos com nomes específicos. Eles são as imagens das alternativas
                pattern_img_alternativa = re.compile(rf'.*alter-{alternativa['letter']}\.png$')
                for arquivo in sorted(os.listdir(dir_questions_number_json)):
                    if pattern_img_alternativa.match(arquivo):
                        path_image_complete = os.path.join(dir_questions_number_json, arquivo)
                        # Armazena esse caminho no array 'alter_img' do dict formatado da alternativa
                        alternativa_formatted['alter_img'].append(path_image_complete)
                        break;

                # Adiciona o objeto da alternativa criado na list 'alternativas' do json formatado
                question_dict_formatted['alternativas'].append(alternativa_formatted);


            # Converte dict para json
            question_json_formatted = json.dumps(question_dict_formatted, indent=4)

            # Salva o arquivo json no caminho especificado
            path_json_formatted = os.path.join(dir_questions_number_json, f"enem_questao{i}.json")
            with open(path_json_formatted, 'w') as path_json_formatted:
                path_json_formatted.write(question_json_formatted)



    except json.JSONDecodeError as error:
        print("O conteúdo do arquivo não está em um formato JSON válido.\n", error)
        question_dict = None

    except FileNotFoundError:
        print(f"Arquivo {path_questions} não encontrado.")
        question_dict = None

    except PermissionError:
        print(f"Permissão negada ao acessar {path_questions} ou o diretório de destino.")
        question_dict = None

    except IsADirectoryError:
        print(f"{path_questions} é um diretório, não um arquivo.")
        question_dict = None

    except UnicodeDecodeError as error:
        print("Erro de codificação ao ler o arquivo.\n", error)
        question_dict = None

    except KeyError as error:
        print(f"Chave esperada ausente no JSON: {error}")
        question_dict = None

    except TypeError as error:
        print("Tipo inesperado de dados encontrado no JSON.\n", error)
        question_dict = None