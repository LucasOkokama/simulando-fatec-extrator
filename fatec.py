from fatec_format_questions import fatecFormatarQuestoes
import os

for anoDaProva in range(2024, 2008, -1):
    for semestreDaProva in range(1, 3):
        provaPath = f"pdf/FatecProva_{anoDaProva}_{semestreDaProva}.pdf"
        gabaritoPath = f"pdf/FatecGabarito_{anoDaProva}_{semestreDaProva}.pdf"

        if os.path.isfile(provaPath) and os.path.isfile(gabaritoPath):
            fatecFormatarQuestoes(anoDaProva, semestreDaProva, provaPath, gabaritoPath)