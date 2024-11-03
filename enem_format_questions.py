import json
import os
import re

def enemFormatarQuestoes(anoDaProva):
    # Diretório para acessar as questões NÃO FORMATADAS
    dir_questions_txt = "vestibulares/enem"
    # Diretório para onde as questões FORMATADAS irão
    dir_questions_json = f"vestibulares/enemFormatado/{anoDaProva}"

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
                    "enunciado": "",
                    "imgs": [],
                    "pergunta": question_dict['alternativesIntroduction'].replace("\n", "<br>"),
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
                        path_image_complete = os.path.join(dir_questions_number_json, arquivo).replace("\\","/")
                        # Armazena esse caminho no array 'imgs' do dict formatado
                        question_dict_formatted['imgs'].append(path_image_complete)


                # Implementa tag de img no enunciado
                imgCount = 1
                textoEnunciadoTagImg = question_dict['context']
                for linkImg in question_dict_formatted['imgs']:
                    pattern = r'!\[\]\((.*?)\)'

                    '''
                    !      => Procura pelo carácter "!"
                    \\[     => Procura pelo carácter "[". A barra invertida >\\< serve para fazer o escape
                    \\]     => Procura pelo carácter "]". A barra invertida >\\< serve para fazer o escape
                    \\(     => Procura pelo carácter "(". A barra invertida >\\< serve para fazer o escape
                    (.*?)  => Procura por qualquer carácter (.) que apareça zero ou mais vezes (*) 
                                no menor espaço possível para satisfazer a condição (? ou não-guloso)
                    \\)     ==> Procura pelo carácter ")". A barra invertida >\\< serve para fazer o escape
                    '''

                    # Cria a tag da imagem já com o respectivo link e alt
                    img_html_tag = f'<img src="{linkImg}" alt="imagem {imgCount} da questão">'
                    imgCount += 1
                    # Procura no texto o padrão criado, e se achado ele substitui pelo img_html_tag.
                    # O count=1 diz que ele só deverá substituir a primeira instância por comando
                    textoEnunciadoTagImg = re.sub(pattern, img_html_tag, textoEnunciadoTagImg, count=1)

                # Substitui "\n" por "<br>" para o navegador/html entenderem e armazena o novo enunciado no dict formatado
                question_dict_formatted['enunciado'] = str(textoEnunciadoTagImg).replace("\n", "<br>")

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
                            path_image_complete = os.path.join(dir_questions_number_json, arquivo).replace("\\", "/")
                            # Armazena esse caminho no array 'alter_img' do dict formatado da alternativa
                            alternativa_formatted['alter_img'].append(path_image_complete)
                            break

                    # Adiciona o objeto da alternativa criado na list 'alternativas' do json formatado
                    question_dict_formatted['alternativas'].append(alternativa_formatted);


                # Converte dict para json
                question_json_formatted = json.dumps(question_dict_formatted, indent=4, ensure_ascii=False)

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