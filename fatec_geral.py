from fatec_format_questions import formatarQuestoes
from fatec_extract_images import extrairImagens
import os


for anoDaProva in range(2024, 2008, -1):
    for semestreDaProva in range(1, 3):
        provaPath = f"pdf/FatecProva_{anoDaProva}_{semestreDaProva}.pdf"
        gabaritoPath = f"pdf/FatecGabarito_{anoDaProva}_{semestreDaProva}.pdf"

        if os.path.isfile(provaPath) and os.path.isfile(gabaritoPath):
            formatarQuestoes(anoDaProva, semestreDaProva, provaPath, gabaritoPath)
            extrairImagens(anoDaProva, semestreDaProva, provaPath)
            print("\n\n\n\n")