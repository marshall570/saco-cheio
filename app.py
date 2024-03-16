from pypdf import PdfReader, PdfWriter
import pandas

import os
import logging

from turmas import Turmas

logging.basicConfig(
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()],
    encoding='utf-8',
    format='%(asctime)s [%(levelname)s: %(filename)s (line %(lineno)d)] %(message)s',
    datefmt='%d/%m/%Y - %H:%M:%S',
    level=logging.INFO
)


def escolher_planilha(turma, bimestre):
    data_frame = pandas.read_excel(
        turma,
        sheet_name=f'{bimestre}º BIMESTRE'
    )

    return data_frame


def processar_comportamento(positivos, negativos):
    comportamento = (6.5 + (positivos * 1.5) - (negativos * 1.5))

    if comportamento > 10:
        comportamento = 10
    elif comportamento < 0:
        comportamento = 0

    if comportamento != 0:
        comportamento = comportamento / 10

    return comportamento


def processar_tarefas(dados):
    nota_tarefas = 0

    total_tarefas = sum(
        [1 for key in dados.keys() if key.startswith('TAREFA')]
    )

    for i in range(total_tarefas):
        if dados[f'TAREFA 0{int(i)+1}'] != 'NE':
            nota_tarefas += float(dados[f'TAREFA 0{int(i)+1}'])
        else:
            nota_tarefas += 0

    return nota_tarefas


def converter_mencao(nota_final):
    if nota_final < 5:
        mencao_final = 'I'
    elif nota_final < 7:
        mencao_final = 'R'
    elif nota_final < 8.5:
        mencao_final = 'B'
    else:
        mencao_final = 'MB'

    return mencao_final


def gerar_relatorio(dados, bimestre):
    try:
        reader = PdfReader('templates/template-4t.pdf')
        writer = PdfWriter()

        page = reader.pages[0]
        fields = reader.get_fields()

        writer.append(reader)

        writer.update_page_form_field_values(
            writer.pages[0],
            {
                'txt_nome': dados['NOME'],
                'txt_turma': dados['TURMA'],
                'txt_componente': dados['COMPONENTE'],
                'txt_mencao': dados['MENÇÃO FINAL'],
                'txt_tarefa01': dados['TAREFA 01'],
                'txt_tarefa02': dados['TAREFA 02'],
                'txt_tarefa03': dados['TAREFA 03'],
                'txt_tarefa04': dados['TAREFA 04'],
                'txt_avaliacao': dados['AVALIAÇÃO'],
                'txt_positivo': dados['POSITIVOS'],
                'txt_negativo': dados['NEGATIVOS'],
                'txt_comportamento': dados['COMPORTAMENTO'],
            },
        )

        path = f'{os.path.expanduser('~')}/Documentos/Etec/Relatorios/{dados['TURMA'].replace(' ','_')}/{bimestre}BIM'

        os.makedirs(path, exist_ok=True)

        with open(f'{path}/{dados['NOME'].replace(' ', '-').lower()}.pdf', 'wb') as output_stream:
            writer.write(output_stream)
        
        logging.info(f'{dados['NOME']}: OK')

    except Exception as error:
        logging.critical(error)


def processar_planilha(turma, bimestre):
    for (key, value) in escolher_planilha(turma['planilha'], bimestre).iterrows():
        dados = value.fillna('0')
        dados['TURMA'] = turma['turma']
        dados['COMPONENTE'] = turma['componente']
        dados['NOTA TAREFAS'] = processar_tarefas(dados)
        dados['POSITIVOS'] = dados['COMPORTAMENTO'].count('+')
        dados['NEGATIVOS'] = dados['COMPORTAMENTO'].count('-')
        dados['COMPORTAMENTO'] = processar_comportamento(dados['POSITIVOS'], dados['NEGATIVOS'])
        dados['NOTA FINAL'] = float(dados['COMPORTAMENTO']) + float(dados['NOTA TAREFAS']) + float(dados['AVALIAÇÃO'])
        dados['MENÇÃO FINAL'] = converter_mencao(dados['NOTA FINAL'])

        gerar_relatorio(dados, bimestre)


processar_planilha(Turmas.i_adm_damppc, 1)