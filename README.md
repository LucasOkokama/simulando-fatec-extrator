# Simulando Fatec | Extractor
Este repositório faz parte do projeto [`SIMULANDO FATEC`](https://github.com/pedro-Trovo/simulando-fatec) que visa desenvolver uma plataforma gratuita para estudantes realizarem simulados do Vestibular FATEC.

Para que a plataforma funcione corretamente, é necessário ter um banco de dados populado com questões organizadas e bem estruturadas. Pensando nisso, este repositório foi criado com o objetivo de automatizar a extração das questões diretamente dos PDFs das provas e gabaritos oficiais da FATEC, convertendo-as para o formato JSON.

O script analisa os arquivos PDF da prova e do gabarito, localiza e extrai as questões de forma estruturada, transformando-as em um JSON padronizado. Esse JSON pode então ser cadastrado em um banco de dados e mostrados na tela.

> [!TIP]
> Confira também o [`Front-end`](https://github.com/pedro-Trovo/simulando-fatec-frontend) e [`Back-end`](https://github.com/pedro-Trovo/simulando-fatec-backend) do Simulando Fatec!

<br>


## 🛠️ Tech Stack
O projeto foi desenvolvido utilizando Python, linguagem escolhida pela sua versatilidade e poderosas bibliotecas de manipulação de arquivos e dados estruturados. O script em Python é responsável por abrir e ler os PDFs da prova e do gabarito, processar os textos e organizar as informações extraídas no formato JSON.

Para auxiliar na interpretação e organização das questões, foi utilizado o Gemini AI, uma inteligência artificial desenvolvida pela Google. Com a ajuda dessa IA, foi possível identificar padrões e extrair dados de forma mais precisa e eficiente.

O ambiente de desenvolvimento utilizado foi o PyCharm, uma IDE robusta para Python que contribuiu com recursos como destaque de sintaxe, depuração, execução rápida e organização geral do projeto.

<table align="center">
    <tr>
        <th>Linguagem</th>
        <th>Biblioteca</th>
        <th>Editor/IDE</th>
    </tr>
    <tr>
        <th>
            <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
        </th>
        <td>
            <img alt="Gemini AI" src="https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white"/>
        </td>
        <td>
            <img alt="PyCharm" src="https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green"/>
        </td>
    </tr>
</table>


<br>


## 📁 Estrutura do Projeto
`fatec.py`: Responsável por percorrer os anos e semestres das provas da FATEC.

`fatec_format_questions.py`: Responsável por formatar cada questão individual em JSON.

`prompt/`: Contém os arquivos utilizados para instruir o Gemini AI durante o processo de extração e formatação das questões.
- `geminiai-prompt.txt`: Contém o texto de instruções enviado ao Gemini AI para orientar a conversão das questões.
- `questao-base-prompt.json`: Arquivo modelo com o formato desejado da questão em JSON.

`fatec_formatado/`: Pasta onde serão salvos os arquivos JSON contendo as questões formatadas.

`pdf/`: Diretório destinado ao armazenamento dos PDFs das provas e dos gabaritos da FATEC.

`.gitignore`: Arquivo de configuração do Git que define quais arquivos ou pastas devem ser ignorados no versionamento.

```
> ESTRUTURA VISUAL

📦
├── fatec.py
├── fatec_format_questions.py
├── prompt/
│   ├── geminiai-prompt.txt
│   └── questao-base-prompt.json
├── fatec_formatado/
├── pdf/
│   ├── FatecProva_<ANO>_<SEMESTRE>.pdf
│   └── FatecGabarito_<ANO>_<SEMESTRE>.pdf
├── .gitignore
```

> [!WARNING]
> Os arquivos PDF's devem seguir a seguinte nomenclatura: <br><br>
> Modelo: FatecProva_ANO_SEMESTRE.pdf <br>
> Ex: FatecProva_2024_1.pdf <br><br>
> Modelo: FatecGabarito_ANO_SEMESTRE.pdf <br>
> Ex: FatecGabarito_2024_1.pdf


<br>


## ⚙️ Pré-requisitos
- Ter o [Python](https://www.python.org/downloads/) instalado no sistema.
- Gerar uma [API Key](https://aistudio.google.com/apikey) para utilizar o GeminiAI.
- Baixar o [PyCharm](https://www.jetbrains.com/pycharm/) para facilitar a execução e organização do código (opcional). 


<br>


## 🚀 Inicializando o projeto
> [!NOTE]  
> Em caso de dúvidas, veja a [documentação oficial](https://ai.google.dev/gemini-api/docs) da API da Gemini AI!

> [!CAUTION]
> O Gemini AI tende a errar os valores dos campos `enunciado` e `pergunta`. Por isso, é bom revisá-los!

1. Faça um `git clone` do repositório:
```console
git clone https://github.com/LucasOkokama/simulando-fatec-extrator
cd simulando-fatec-extrator
```

2. Instale as `depêndencias` do projeto:
```
pip install -r requirements.txt
```

3. Crie um arquivo `.env` para armazenar sua API Key:
```
GEMINIAI_KEY=<SUA_GEMINIAI_API_KEY>   
```

4. Execute o `scrip` principal:
```
py fatec.py
```
