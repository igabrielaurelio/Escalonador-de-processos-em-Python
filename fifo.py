def escalonador_fifo(processos):
    tempo_atual = 0
    resultados = []

    for processo in processos:
        tempo_chegada = processo.tempo_chegada

        # Se o processo chegou depois do tempo atual, avança o tempo
        if tempo_atual < tempo_chegada:
            tempo_atual = tempo_chegada  

        # Tempo de espera = tempo atual - tempo que o processo chegou
        tempo_espera = tempo_atual - tempo_chegada

        # Tempo total = tempo atual + tempo de CPU necessário
        tempo_total = tempo_atual + processo.tempo_cpu

        # Salva os resultados
        resultados.append((tempo_total, tempo_espera))

        # Atualiza o tempo atual
        tempo_atual = tempo_total  

    return resultados