# Simulando Fatec - Extractor
Este repositório faz parte de um projeto maior que visa desenvolver uma plataforma gratuita para estudantes realizarem simulados de vestibulares, com foco inicial na FATEC.

Para que a plataforma funcione corretamente, é necessário ter um banco de dados populado com questões organizadas e bem estruturadas. Pensando nisso, este mini projeto foi criado com o objetivo de automatizar a extração das questões diretamente dos PDFs das provas e gabaritos oficiais da FATEC, convertendo-as para o formato JSON.

O script analisa os arquivos PDF da prova e do gabarito, localiza e extrai as questões de forma estruturada, transformando-as em um JSON padronizado. Esse JSON pode então ser utilizado por outro projeto (responsável pelo backend) para cadastrar as informações no banco de dados de maneira automatizada.



## ⚙️ Tech Stack
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



## Extrair questões da FATEC
> [!NOTE]  
> Em caso de dúvidas, veja a [documentação oficial](https://ai.google.dev/gemini-api/docs) da API da Gemini AI para facilitar!

> [!CAUTION]
> O Gemini AI tende a errar os valores dos campos `enunciado` e `pergunta`. Por isso, é bom revisá-los!

> [!IMPORTANT]
> Nenhum imagem é extraída, estas devem ser feitas manualmente.

1. As questões do Vestibular FATEC serão extraidas usando o [Gemini AI](https://gemini.google.com/) da Google. Para isso, você deve [**criar uma chave de API**](https://aistudio.google.com/apikey) gratuitamente, além de ter uma [conta Google](#conta-google-para-o-gemini-ai).
2. Faça um `git clone` do repositório:
```console
git clone https://github.com/LucasKazuhiro/vestibular-extrair-questoes.git
```
3. Copie sua API Key do Gemini AI e cole no arquivo `gemini-api-key.txt`
4. Na pasta root do projeto `vestibular-extrair-questoes`, execute o seguinte comando:
```console
git update-index --assume-unchanged gemini-api-key.txt
```
5. Instale os pacotes para usar o Gemini AI:
```console
pip install -q -U google-generativeai
```
6. E em seguida:
```console
py fatec.py
```
