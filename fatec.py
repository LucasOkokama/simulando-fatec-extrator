from vestibulares.fatec.fatec_format_questions import fatecFormatarQuestoes

import os

for anoDaProva in range(2024, 2008, -1):
    for semestreDaProva in range(1, 3):
        prova_path = f"vestibulares/fatec/pdf/FatecProva_{anoDaProva}_{semestreDaProva}.pdf"
        gabarito_path = f"vestibulares/fatec/pdf/FatecGabarito_{anoDaProva}_{semestreDaProva}.pdf"

        if os.path.isfile(prova_path) and os.path.isfile(gabarito_path):
            fatecFormatarQuestoes(anoDaProva, semestreDaProva)