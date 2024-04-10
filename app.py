import pandas

import logging

from turmas import Turmas
from nsa import NSA
from relatorio import Relatorio
from notas import Notas

logging.basicConfig(
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()],
    encoding='utf-8',
    format='%(asctime)s [%(levelname)s: %(filename)s (line %(lineno)d)] %(message)s',
    datefmt='%d/%m/%Y - %H:%M:%S',
    level=logging.INFO
)


def escolher_planilha(planilha, bimestre):
    import os

    path = os.path.expanduser('~') + '/Downloads/Planilhas'

    data_frame = pandas.read_excel(
        f'{path}/{planilha}.xlsx',
        sheet_name=f'{bimestre}º BIMESTRE',
        converters={'RM': str},
    )

    return data_frame


def processar_planilha(turma, bimestre, modo):
    dataset = pandas.DataFrame({})

    for chave, valor in escolher_planilha(turma['planilha'], bimestre).iterrows():
        bases = escolher_planilha(turma['planilha'], f'BASES {bimestre}')
        bases = bases.to_dict('records')[0]

        dados = valor.fillna('NA')
        dados['TURMA'] = turma['turma']
        dados['COMPONENTE'] = turma['componente']
        dados['PLANILHA'] = turma['planilha']
        dados['NOTA TAREFAS'] = Notas.processar_tarefas(dados, bases)
        Notas.tratar_comportamento(dados, bases)
        Notas.tratar_avaliacao(dados, bases)
        Notas.tratar_nota_final(dados)
        dados['MENÇÃO FINAL'] = Notas.converter_mencao(
            dados['NOTA FINAL'],
            bases['MAX NOTA']
        )

        dataset = pandas.concat([dataset, dados.to_frame().T])

        if modo == 'Relatorio':
            Relatorio.gerar_relatorio(dados, bases, bimestre)

    if modo == 'NSA':
        NSA.exportar_nsa(dataset, turma)


# for turma, item in Turmas.lista.items():
#     processar_planilha(item, 1, 'Relatorio')

processar_planilha(Turmas.lista['3 MTEC MKT PM'], 1, 'Relatorio')

