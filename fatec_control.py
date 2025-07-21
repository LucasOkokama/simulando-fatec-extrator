# 📦 Funções customizadas
from fatec_format_questions import formatarQuestoes
from fatec_extract_images import extrairImagens
import os


# Dados para a extração funcionar (OBRIGATÓRIO)
anoDaProva = 2024
semestreDaProva = 1
provaPath = f"pdf/FatecProva_{anoDaProva}_{semestreDaProva}.pdf"
gabaritoPath = f"pdf/FatecGabarito_{anoDaProva}_{semestreDaProva}.pdf"

# Extração específica de questões (OPCIONAL)
questaoInicial=1
questoesSelecionadas=None
# questoesSelecionadas=[54] # --> Apenas extrai as questões específicadas


# Extração específica de imagens (OPCIONAL)
extrairSomenteImagens = False
salvarImagensNoArrayDoJSON = True


if os.path.isfile(provaPath) and os.path.isfile(gabaritoPath):
  if extrairSomenteImagens:
    extrairImagens(anoDaProva, semestreDaProva, provaPath, salvarImagensNoArrayDoJSON)
  else:
    formatarQuestoes(anoDaProva, semestreDaProva, provaPath, gabaritoPath, questaoInicial, questoesSelecionadas)
    extrairImagens(anoDaProva, semestreDaProva, provaPath, salvarImagensNoArrayDoJSON)