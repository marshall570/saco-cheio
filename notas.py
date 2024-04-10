class Notas():
    def converter_mencao(nota, max):
        porcentagem = (nota / max) * 100

        if porcentagem < 50:
            mencao = 'I'
        elif porcentagem < 70:
            mencao = 'R'
        elif porcentagem < 85:
            mencao = 'B'
        else:
            mencao = 'MB'

        return mencao


    def processar_comportamento(positivos, negativos):
        comportamento = (6.5 + (positivos * 1.5) - (negativos * 1.5))

        if comportamento > 10:
            comportamento = 10
        elif comportamento < 0:
            comportamento = 0

        if comportamento != 0:
            comportamento = comportamento / 10

        return comportamento


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


    def processar_avaliacao(dados, bases):
        if dados['AVALIAÇÃO'] != 'NA':
            nota_avaliacao = float(dados['AVALIAÇÃO'])

            dados['MENÇÃO - AVALIAÇÃO'] = Notas.converter_mencao(
                nota_avaliacao,
                float(bases['MAX AVALIAÇÃO'])
            )
        else:
            nota_avaliacao = 0
            dados['MENÇÃO - AVALIAÇÃO'] = 'NA'

        return nota_avaliacao


    def tratar_comportamento(dados, bases):
        if 'COMPORTAMENTO' in dados:
            dados['POSITIVOS'] = dados['COMPORTAMENTO'].count('+')
            dados['NEGATIVOS'] = dados['COMPORTAMENTO'].count('-')

            dados['COMPORTAMENTO'] = Notas.processar_comportamento(
                dados['POSITIVOS'],
                dados['NEGATIVOS']
            )
            dados['MENÇÃO - COMPORTAMENTO'] = Notas.converter_mencao(
                float(dados['COMPORTAMENTO']),
                float(bases['MAX COMPORTAMENTO'])
            )
        else:
            return False


    def tratar_avaliacao(dados, bases):
        if 'AVALIAÇÃO' in dados:
            dados['NOTA AVALIAÇÃO'] = Notas.processar_avaliacao(dados, bases)
        else:
            return False


    def tratar_nota_final(dados):
        dados['NOTA FINAL'] = float(dados['NOTA TAREFAS'])

        if 'COMPORTAMENTO' in dados:
            dados['NOTA FINAL'] += float(dados['COMPORTAMENTO'])

        if 'NOTA AVALIAÇÃO' in dados:
            dados['NOTA FINAL'] += float(dados['NOTA AVALIAÇÃO'])
