# 📂 Estrutura Geral do Código

Este código Python realiza a extração e formatação de questões de provas da FATEC a partir de arquivos PDF (prova e gabarito), utilizando a API da Gemini AI para gerar objetos JSON estruturados com base nas questões.

A seguir, o código será dividido por seções com explicações de cada parte.


<br>


# 📦 Importações de bibliotecas

```python
# 📦 Bibliotecas padrão
import os
import time
import json
import pathlib

# 📦 Bibliotecas de terceiros
from dotenv import load_dotenv

# 📦 Bibliotecas da Google (genai)
from google import genai
from google.genai import types
```

Esta seção importa bibliotecas padrão do Python, como `os` (operações com o sistema), `time` (temporização), `json` (manipulação de JSON) e `pathlib` (manipulação de caminhos de arquivos).

Também carrega a biblioteca `dotenv` (para ler variáveis de ambiente do arquivo `.env`) e bibliotecas do SDK da Gemini AI (`genai`).


<br>


# 🔑 Configuração da API Gemini

```python
# Carrega .env
load_dotenv()

# Armazena e Configura a API Key da Gemini
geminiai_key = os.getenv("GEMINIAI_KEY")
client = genai.Client(api_key=geminiai_key)

# Modelo da GeminiAI usado
geminiai_model = "gemini-2.5-flash"
```

Aqui, o código carrega as variáveis do arquivo `.env`, resgata a chave da API `GEMINIAI_KEY`, configura o cliente Gemini AI e define o modelo que será utilizado (`gemini-2.5-flash`).


<br>


# 🧠 Função Principal: `formatarQuestoes`

```python
def formatarQuestoes(
        anoDaProva,
        semestreDaProva,
        provaPath,
        gabaritoPath,
        questaoInicial=1,
        questoesSelecionadas=None
):
```

A função `formatarQuestoes` é a principal do script. Ela recebe o ano e semestre da prova, os caminhos dos arquivos PDF da prova e do gabarito, e parâmetros opcionais como a questão inicial e uma lista de questões específicas a processar.


<br>


# 📄 Carregando arquivos e prompts

```python
files = [
  pathlib.Path(provaPath),
  pathlib.Path(gabaritoPath),
]

with open('prompt/geminiai-extracao-questao.txt', 'r', encoding="utf-8") as my_file:
  prompt_questao = my_file.read()

with open('prompt/questao-base.json', 'r', encoding="utf-8") as my_file:
  prompt_jsonBase = json.load(my_file)
prompt_jsonBase_string = json.dumps(prompt_jsonBase)
```

- Cria uma lista com os caminhos dos arquivos PDF.
- Carrega dois arquivos de prompt:
  - Um texto explicativo para a Gemini AI (`geminiai-extracao-questao.txt`).
  - Um JSON base com a estrutura da questão (`questao-base.json`), que é convertido para string.


<br>


# 🔁 Loop para gerar os arquivos JSON das questões

```python
for num_questao in range(questaoInicial, 55):
  if questoesSelecionadas is None or num_questao in questoesSelecionadas:
```

O loop percorre as questões da 1 até a 54. Caso `questoesSelecionadas` esteja definido, apenas as questões presentes na lista serão processadas.


<br>


# 🤖 Montagem do prompt e chamada à Gemini AI

```python
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
```

Aqui, o código:
- Monta o prompt final com o conteúdo dos arquivos TXT e o JSON base.
- Envia o prompt e os dois arquivos PDF para a API da Gemini AI.
- A resposta (`response`) será o JSON da questão formatada.


<br>


# 🧹 Tratamento da resposta da Gemini

```python
print(f"{response.usage_metadata.total_token_count} tokens usados\n")

questao_formatada = response.text.replace('```json', '').replace('```', '')
questao_formatada = json.loads(questao_formatada)
```

- Imprime o número de tokens utilizados.
- Remove as marcações da `Fenced Code Block` do texto gerado.
- Converte a string JSON em um dicionário Python.


<br>


# 📝 Adiciona dados extras e salva arquivo

```python
questao_formatada['prova']['id']['ano'] = anoDaProva
questao_formatada['prova']['id']['semestre'] = semestreDaProva
questao_formatada['numQuestao'] = num_questao

prova_questao_path = f"fatec_formatado/{anoDaProva}_{semestreDaProva}/{num_questao}"
os.makedirs(prova_questao_path, exist_ok=True)

dir_final = os.path.join(prova_questao_path, f"fatec_questao{num_questao}.json")
with open(dir_final, 'w', encoding='utf-8') as file:
  json.dump(questao_formatada, file, indent=4, ensure_ascii=False)
```

- Preenche os campos `ano`, `semestre` e número da questão no dicionário.
- Cria a pasta destino com base na prova e questão.
- Salva o arquivo JSON final no diretório `fatec_formatado`.


<br>


# 💤 Pausa entre execuções e tratamento de exceções

```python
time.sleep(6)
```

Um `sleep` de 6 segundos é usado para evitar sobrecarga ou limitação da API.
