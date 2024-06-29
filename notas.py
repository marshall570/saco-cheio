PORCENTAGEM_R = 45
PORCENTAGEM_B = 65
PORCENTAGEM_MB = 85


class Notas():
    def converter_mencao(nota, max):
        porcentagem = (nota / max) * 100

        if porcentagem < PORCENTAGEM_R:
            mencao = 'I'
        elif porcentagem < PORCENTAGEM_B:
            mencao = 'R'
        elif porcentagem < PORCENTAGEM_MB:
            mencao = 'B'
        else:
            mencao = 'MB'

        return mencao

    def processar_tarefas(dados, bases):
        nota_tarefas = 0

        total_tarefas = sum(
            [1 for key in dados.keys() if key.startswith('TAREFA')]
        )

        for i in range(total_tarefas):
            if dados[f'TAREFA 0{int(i)+1}'] != 'NA':
                nota_tarefas += float(dados[f'TAREFA 0{int(i)+1}'])

                dados[f'MENÇÃO - TAREFA 0{int(i)+1}'] = Notas.converter_mencao(
                    dados[f'TAREFA 0{int(i)+1}'],
                    float(bases[f'MAX TAREFA 0{int(i)+1}'])
                )
            else:
                nota_tarefas += 0
                dados[f'MENÇÃO - TAREFA 0{int(i)+1}'] = 'NA'

        return nota_tarefas

    def processar_atividade(atividade, dados, bases):
        if dados[atividade] != 'NA':
            nota = float(dados[atividade])

            dados[f'MENÇÃO - {atividade}'] = Notas.converter_mencao(
                nota,
                float(bases[f'MAX {atividade}'])
            )
        else:
            nota = 0
            dados[f'MENÇÃO - {atividade}'] = 'NA'

        return nota

    def tratar_atividade(atividade, dados, bases):
        if atividade in dados:
            dados[f'NOTA {atividade}'] = Notas.processar_atividade(
                atividade, dados, bases)
        else:
            return False

    def tratar_nota_final(dados):
        dados['NOTA FINAL'] = float(dados['NOTA TAREFAS'])

        if 'NOTA AVALIAÇÃO' in dados:
            dados['NOTA FINAL'] += float(dados['NOTA AVALIAÇÃO'])

        if 'RECUPERAÇÃO' in dados:
            dados['NOTA FINAL'] += float(dados['NOTA RECUPERAÇÃO'])

        if 'KAHOOT' in dados:
            dados['NOTA FINAL'] += float(dados['NOTA KAHOOT'])
