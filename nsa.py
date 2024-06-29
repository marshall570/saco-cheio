import pandas

import os
import logging


class NSA():
    def exportar_nsa(bimestre, dados, turma):
        try:
            path = os.path.expanduser('~') + f'/Documentos/Etec/Planilhas/NSA/{bimestre}_BIM'

            os.makedirs(path, exist_ok=True)

            dados.to_excel(
                f'{path}/NSA - {turma['planilha']}.xlsx',
                index=None,
                columns=colunas_nsa(dados),
            )

            logging.info(f'''{turma['planilha']}: OK''')

        except Exception as error:
            logging.critical(error)


def colunas_nsa(dados):
    colunas = ['RM', 'NOME']

    if 'MENÇÃO - COMPORTAMENTO' in dados:
        colunas.append('MENÇÃO - COMPORTAMENTO')

    total_tarefas = sum(
        [1 for key in dados.keys() if key.startswith('TAREFA')]
    )

    for i in range(total_tarefas):
        colunas.append(f'MENÇÃO - TAREFA 0{i+1}')

    if 'MENÇÃO - AVALIAÇÃO' in dados:
        colunas.append('MENÇÃO - AVALIAÇÃO')

    if 'MENÇÃO - RECUPERAÇÃO' in dados:
        colunas.append('MENÇÃO - RECUPERAÇÃO')

    if 'MENÇÃO - KAHOOT' in dados:
        colunas.append('MENÇÃO - KAHOOT')

    colunas.append('MENÇÃO FINAL')
    colunas.append('NOTA FINAL')

    return colunas
