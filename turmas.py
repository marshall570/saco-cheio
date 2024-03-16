import os

from dotenv import load_dotenv

load_dotenv()

class Turmas():
    i_adm_ai = {
        'turma': '1º Administração (Tarde)',
        'componente': 'Aplicativos Informatizados (AI)',
        'planilha': os.getenv('1ADM-AI')
    }

    i_adm_damppc = {
        'turma': '1º MTEC Administração',
        'componente': 'Desenvolvimento das Ações de Marketing (DAM)',
        'planilha': os.getenv('1MTEC-ADM-DAMPPC')
    }
