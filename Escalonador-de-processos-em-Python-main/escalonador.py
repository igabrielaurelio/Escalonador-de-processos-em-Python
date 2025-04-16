import copy
from collections import deque

def fifo(processos_orig):
    """
    Simula o escalonamento FIFO com suporte a E/S.
    FIFO (First-In-First-Out): processos são executados na ordem de chegada,
    sem preempção. Um processo pode ser interrompido apenas se precisar realizar E/S.
    """
    processos = sorted(copy.deepcopy(processos_orig), key=lambda p: p.tempo_chegada)
    
    tempo_global = 0
    finalizados = 0
    fila = deque()
    bloqueados = []  # Lista de tuplas (processo, tempo_de_retorno)
    index_prox_proc = 0
    processo_executando = None

    while finalizados < len(processos):
        # Adiciona novos processos que chegaram ao sistema
        while index_prox_proc < len(processos) and processos[index_prox_proc].tempo_chegada <= tempo_global:
            fila.append(processos[index_prox_proc])
            index_prox_proc += 1

        # Verifica desbloqueios de E/S
        desbloquear = []
        recem_desbloqueados = []

        for proc, retorno in bloqueados:
            if tempo_global >= retorno:
                desbloquear.append(proc)

        for proc in desbloquear:
            bloqueados = [b for b in bloqueados if b[0] != proc]
            fila.appendleft(proc)  # Retorna para o início da fila
            recem_desbloqueados.append(proc)

        # Se não há processo executando, pega o próximo
        if not processo_executando and fila:
            processo_executando = fila.popleft()

        # Se ainda não há processo, apenas avança o tempo
        if not processo_executando:
            tempo_global += 1
            continue

        # Calcula tempo já executado
        tempo_executado = processo_executando.tempo_cpu - processo_executando.tempo_restante

        # Verifica se deve realizar E/S
        if processo_executando.tem_e_s and tempo_executado == processo_executando.inicio_e_s:
            retorno = tempo_global + processo_executando.tempo_e_s
            bloqueados.append((processo_executando, retorno))
            processo_executando.tempo_restante -= 1
            processo_executando = None
            tempo_global += 1
            continue

        # Executa 1 unidade de tempo
        processo_executando.tempo_restante -= 1

        # Soma tempo de espera para processos prontos (exceto os recém-desbloqueados)
        for p in fila:
            if p.tempo_restante > 0 and p not in recem_desbloqueados:
                p.tempo_espera += 1

        # Se o processo terminou, registra a finalização no tempo ATUAL
        if processo_executando.tempo_restante == 0:
            processo_executando.tempo_finalizacao = tempo_global + 1  # finaliza ao final da execução
            finalizados += 1
            processo_executando = None

        # Avança o tempo global
        tempo_global += 1

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
        # Novos processos chegando
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

        # Seleciona processo com menor tempo restante (SJF)
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

            # Atualiza o tempo de espera dos outros processos na fila de prontos
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
        # Novos processos chegando
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

            # Atualiza o tempo de espera dos outros processos na fila de prontos
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
            if proc.tempo_chegada <= tempo_global and proc not in esperando and proc not in fila:
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
