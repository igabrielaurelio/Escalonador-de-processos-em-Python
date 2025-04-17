class Processo:
    def __init__(self, tempo_cpu, tem_e_s, tempo_e_s, inicio_e_s, prioridade, tempo_chegada):
        # Tempo total que o processo precisa para ser executado na CPU
        self.tempo_cpu = tempo_cpu

        # Tempo restante de CPU (inicia igual ao tempo total e vai sendo decrementado)
        self.tempo_restante = tempo_cpu

        # Flag indicando se o processo realiza entrada/saída (0 = não, 1 = sim)
        self.tem_e_s = tem_e_s

        # Duração da operação de E/S (quantas unidades de tempo ele "fica fora")
        self.tempo_e_s = tempo_e_s

        # Momento em que o processo deve iniciar a E/S, contado a partir do início da execução
        self.inicio_e_s = inicio_e_s

        # Prioridade do processo (quanto menor o valor, maior a prioridade)
        self.prioridade = prioridade

        # Tempo em que o processo chega no sistema (momento da criação)
        self.tempo_chegada = tempo_chegada

        # Tempo exato em que o processo finaliza sua execução (definido ao fim da simulação)
        self.tempo_finalizacao = None

        # Tempo total que o processo ficou esperando na fila de prontos
        self.tempo_espera = 0

        # Estado do processo: 'pronto', 'executando', 'bloqueado', 'finalizado' (usado em debug ou extensões)
        self.estado = 'pronto'

    def __repr__(self):
        # Representação simplificada do processo para debug e logs
        return (f"Processo(cpu={self.tempo_cpu}, restante={self.tempo_restante}, "
                f"chegada={self.tempo_chegada}, prioridade={self.prioridade})")
