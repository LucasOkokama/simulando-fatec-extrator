from vestibulares.enem.enem_extract_questions import enemExtrairQuestoes
from  vestibulares.enem.enem_format_questions import enemFormatarQuestoes

for anoDaProva in range(2023, 2008, -1):
    enemExtrairQuestoes(anoDaProva)
    enemFormatarQuestoes(anoDaProva)