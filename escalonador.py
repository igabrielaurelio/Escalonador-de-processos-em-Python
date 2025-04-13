import copy

def fifo(processos_orig):
    """
    Simula o escalonamento FIFO com suporte a E/S.
    FIFO (First-In-First-Out): processos são executados na ordem de chegada,
    sem preempção. Um processo pode ser interrompido apenas se precisar realizar E/S.
    """
    from collections import deque

    # Ordena os processos por tempo de chegada
    processos = sorted(copy.deepcopy(processos_orig), key=lambda p: p.tempo_chegada)
    tempo_global = 0
    finalizados = 0
    fila = deque()
    bloqueados = []  # Processos em E/S: (processo, tempo_de_retorno)
    index_prox_proc = 0
    processo_executando = None

    while finalizados < len(processos):
        # Adiciona processos que chegaram à fila de prontos
        while index_prox_proc < len(processos) and processos[index_prox_proc].tempo_chegada <= tempo_global:
            fila.append(processos[index_prox_proc])
            index_prox_proc += 1

        # Libera processos que terminaram E/S
        desbloquear = []
        for proc, retorno in bloqueados:
            if tempo_global >= retorno:
                desbloquear.append(proc)

        for proc in desbloquear:
            bloqueados = [b for b in bloqueados if b[0] != proc]
            fila.appendleft(proc)  # Volta pro início da fila

        # Se nenhum processo está executando, pega o próximo
        if not processo_executando and fila:
            processo_executando = fila.popleft()

        if not processo_executando:
            tempo_global += 1
            continue

        tempo_executado = processo_executando.tempo_cpu - processo_executando.tempo_restante

        # Se é hora de fazer E/S, envia pra bloqueados
        if processo_executando.tem_e_s and tempo_executado == processo_executando.inicio_e_s:
            retorno = tempo_global + processo_executando.tempo_e_s
            bloqueados.append((processo_executando, retorno))
            processo_executando.tempo_restante -= 1
            tempo_global += 1
            processo_executando = None
            continue

        # Executa 1 unidade
        processo_executando.tempo_restante -= 1
        tempo_global += 1

        # Soma tempo de espera pros que estão na fila
        for p in fila:
            if p.tempo_restante > 0:
                p.tempo_espera += 1

        if processo_executando.tempo_restante == 0:
            processo_executando.tempo_finalizacao = tempo_global
            finalizados += 1
            processo_executando = None

    return processos


def sjf_preemptivo(processos_orig):
    """
    SJF Preemptivo (Shortest Job First) com E/S.
    Sempre escolhe o processo com o menor tempo restante entre os disponíveis.
    """
    processos = copy.deepcopy(processos_orig)
    tempo_global = 0
    finalizados = 0
    processo_executando = None
    prontos = []
    bloqueados = []

    while finalizados < len(processos):
        # Novos processos
        for proc in processos:
            if proc.tempo_chegada == tempo_global:
                prontos.append(proc)

        # Retorno de E/S
        desbloquear = []
        for proc, retorno in bloqueados:
            if tempo_global >= retorno:
                desbloquear.append(proc)
        for proc in desbloquear:
            bloqueados = [b for b in bloqueados if b[0] != proc]
            prontos.append(proc)

        # Finaliza processo
        if processo_executando and processo_executando.tempo_restante == 0:
            processo_executando.tempo_finalizacao = tempo_global
            finalizados += 1
            processo_executando = None

        # Seleciona processo com menor tempo restante
        candidatos = prontos + ([processo_executando] if processo_executando else [])
        candidatos = [p for p in candidatos if p and p.tempo_restante > 0]
        if candidatos:
            menor = min(candidatos, key=lambda p: p.tempo_restante)
            if processo_executando != menor:
                processo_executando = menor
        else:
            processo_executando = None

        if processo_executando:
            tempo_executado = processo_executando.tempo_cpu - processo_executando.tempo_restante

            # Verifica E/S
            if processo_executando.tem_e_s and tempo_executado == processo_executando.inicio_e_s:
                retorno = tempo_global + processo_executando.tempo_e_s
                bloqueados.append((processo_executando, retorno))
                processo_executando.tempo_restante -= 1
                tempo_global += 1
                processo_executando = None
                continue

            processo_executando.tempo_restante -= 1

            # Soma tempo de espera para os outros prontos
            for p in prontos:
                if p != processo_executando and p.tempo_restante > 0:
                    p.tempo_espera += 1

        # Remove finalizados da fila de prontos
        prontos = [p for p in prontos if p.tempo_restante > 0]
        tempo_global += 1

    return processos


def prioridade_preemptivo(processos_orig):
    """
    Prioridade Preemptivo com E/S.
    Sempre executa o processo com maior prioridade (menor valor numérico).
    """
    processos = copy.deepcopy(processos_orig)
    tempo_global = 0
    finalizados = 0
    processo_executando = None
    prontos = []
    bloqueados = []

    while finalizados < len(processos):
        # Novos processos
        for proc in processos:
            if proc.tempo_chegada == tempo_global:
                prontos.append(proc)

        # Desbloqueio de E/S
        desbloquear = []
        for proc, retorno in bloqueados:
            if tempo_global >= retorno:
                desbloquear.append(proc)
        for proc in desbloquear:
            bloqueados = [b for b in bloqueados if b[0] != proc]
            prontos.append(proc)

        # Finaliza processo atual
        if processo_executando and processo_executando.tempo_restante == 0:
            processo_executando.tempo_finalizacao = tempo_global
            finalizados += 1
            processo_executando = None

        # Seleciona processo de maior prioridade (menor valor)
        candidatos = prontos + ([processo_executando] if processo_executando else [])
        candidatos = [p for p in candidatos if p and p.tempo_restante > 0]
        if candidatos:
            melhor = min(candidatos, key=lambda p: p.prioridade)
            if processo_executando != melhor:
                processo_executando = melhor
        else:
            processo_executando = None

        if processo_executando:
            tempo_executado = processo_executando.tempo_cpu - processo_executando.tempo_restante

            # Vai pra E/S
            if processo_executando.tem_e_s and tempo_executado == processo_executando.inicio_e_s:
                retorno = tempo_global + processo_executando.tempo_e_s
                bloqueados.append((processo_executando, retorno))
                processo_executando.tempo_restante -= 1
                tempo_global += 1
                processo_executando = None
                continue

            processo_executando.tempo_restante -= 1

            # Soma tempo de espera para outros prontos
            for p in prontos:
                if p != processo_executando and p.tempo_restante > 0:
                    p.tempo_espera += 1

        # Remove da fila os processos já finalizados
        prontos = [p for p in prontos if p.tempo_restante > 0]
        tempo_global += 1

    return processos


def round_robin(processos_orig, quantum):
    """
    Round Robin com suporte a E/S.
    Cada processo executa por no máximo 'quantum' unidades de tempo.
    Se for para E/S, ele é bloqueado e retorna depois do tempo especificado.
    """
    from collections import deque

    processos = copy.deepcopy(processos_orig)
    tempo_global = 0
    finalizados = 0
    fila = deque()
    bloqueados = []
    esperando = set()

    processos.sort(key=lambda p: p.tempo_chegada)

    while finalizados < len(processos):
        # Desbloqueia processos que terminaram E/S
        desbloquear = []
        for proc, retorno in bloqueados:
            if tempo_global >= retorno:
                desbloquear.append(proc)
        for proc in desbloquear:
            bloqueados = [b for b in bloqueados if b[0] != proc]
            fila.append(proc)

        # Adiciona processos recém-chegados
        for proc in processos:
            if proc.tempo_chegada == tempo_global and proc not in esperando and proc not in fila:
                fila.append(proc)
                esperando.add(proc)

        if not fila:
            tempo_global += 1
            continue

        processo = fila.popleft()
        tempo_exec = 0

        while tempo_exec < quantum and processo.tempo_restante > 0:
            tempo_executado = processo.tempo_cpu - processo.tempo_restante

            # E/S se for o momento
            if processo.tem_e_s and tempo_executado == processo.inicio_e_s:
                retorno = tempo_global + processo.tempo_e_s
                bloqueados.append((processo, retorno))
                processo.tempo_restante -= 1
                tempo_global += 1
                break

            # Executa 1 unidade
            processo.tempo_restante -= 1
            tempo_global += 1
            tempo_exec += 1

            # Atualiza espera dos outros
            for p in fila:
                if p.tempo_restante > 0:
                    p.tempo_espera += 1

        # Volta pra fila se não terminou
        if processo.tempo_restante > 0:
            if not any(b[0] == processo for b in bloqueados):
                fila.append(processo)
        else:
            processo.tempo_finalizacao = tempo_global
            finalizados += 1

    return processos
