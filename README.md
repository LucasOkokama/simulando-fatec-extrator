# Extrair questões da FATEC
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
