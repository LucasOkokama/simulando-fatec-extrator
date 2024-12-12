from vestibulares.fuvest.fuvest_format_questions import fuvestFormatarQuestoes

import os

for anoDaProva in range(2024, 2008, -1):
        prova_path = f"vestibulares/fatec/pdf/fatecProva_{anoDaProva}.pdf"
        gabarito_path = f"vestibulares/fatec/pdf/fatecGabarito_{anoDaProva}.pdf"

        if os.path.isfile(prova_path) and os.path.isfile(gabarito_path):
            fuvestFormatarQuestoes(anoDaProva)