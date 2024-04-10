from pypdf import PdfReader, PdfWriter

import os
import logging


class Relatorio():
    def verificar_modelos(qtd_tarefas, dados):
        cod_etec = dados['PLANILHA'][0:3]

        arquivo = f'{cod_etec}-template-{qtd_tarefas}t_'

        if Relatorio.tratar_avaliacao(dados):
            arquivo += 'av'
        else:
            arquivo += 'sa'

        return arquivo

    def tratar_avaliacao(dados):
        if 'MENÇÃO - AVALIAÇÃO' in dados:
            return True
        else:
            return False

    def tratar_campos(qtd_tarefas, dados, bases):
        if qtd_tarefas == 4:
            campos = {
                'txt_nome': dados['NOME'],
                'txt_turma': dados['TURMA'],
                'txt_componente': dados['COMPONENTE'],
                'txt_mencao': dados['MENÇÃO FINAL'],
                'label_tarefa_01': bases['NOME TAREFA 01'],
                'label_tarefa_02': bases['NOME TAREFA 02'],
                'label_tarefa_03': bases['NOME TAREFA 03'],
                'label_tarefa_04': bases['NOME TAREFA 04'],
                'txt_tarefa01': dados['MENÇÃO - TAREFA 01'],
                'txt_tarefa02': dados['MENÇÃO - TAREFA 02'],
                'txt_tarefa03': dados['MENÇÃO - TAREFA 03'],
                'txt_tarefa04': dados['MENÇÃO - TAREFA 04'],
                'txt_positivo': dados['POSITIVOS'],
                'txt_negativo': dados['NEGATIVOS'],
                'txt_comportamento': dados['MENÇÃO - COMPORTAMENTO']
            }

        else:
            campos = {
                'txt_nome': dados['NOME'],
                'txt_turma': dados['TURMA'],
                'txt_componente': dados['COMPONENTE'],
                'txt_mencao': dados['MENÇÃO FINAL'],
                'label_tarefa_01': bases['NOME TAREFA 01'],
                'label_tarefa_02': bases['NOME TAREFA 02'],
                'label_tarefa_03': bases['NOME TAREFA 03'],
                'txt_tarefa01': dados['MENÇÃO - TAREFA 01'],
                'txt_tarefa02': dados['MENÇÃO - TAREFA 02'],
                'txt_tarefa03': dados['MENÇÃO - TAREFA 03'],
                'txt_positivo': dados['POSITIVOS'],
                'txt_negativo': dados['NEGATIVOS'],
                'txt_comportamento': dados['MENÇÃO - COMPORTAMENTO']
            }

        if Relatorio.tratar_avaliacao(dados):
            campos['txt_avaliacao'] = dados['MENÇÃO - AVALIAÇÃO']

        return campos

    def gerar_relatorio(dados, bases, bimestre):
        try:
            qtd_tarefas = sum(
                [1 for key in dados.keys() if key.startswith('TAREFA')]
            )

            path = os.path.expanduser('~') + '/Documentos/Etec/Relatorios/'
            file = Relatorio.verificar_modelos(qtd_tarefas, dados)

            reader = PdfReader(f'templates/{file}.pdf')
            writer = PdfWriter()

            writer.append(reader)

            writer.update_page_form_field_values(
                writer.pages[0],
                fields=Relatorio.tratar_campos(qtd_tarefas, dados, bases)
            )

            path += f'''{bimestre}BIM/{dados['TURMA'].replace(' ', '_')}'''

            os.makedirs(path, exist_ok=True)

            with open(f'''{path}/{dados['NOME'].replace(' ', '-').lower()}.pdf''', 'wb') as output_stream:
                writer.write(output_stream)

            logging.info(f'''{dados['NOME']}: OK''')

        except Exception as error:
            logging.critical(error)
