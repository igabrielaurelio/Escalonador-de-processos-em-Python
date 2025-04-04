class Processo:
    def __init__(self, id, tempo_cpu, precisa_es, tempo_es, inicio_es, prioridade, tempo_chegada):
        self.id = id
        self.tempo_cpu = tempo_cpu
        self.precisa_es = precisa_es
        self.tempo_es = tempo_es
        self.inicio_es = inicio_es
        self.prioridade = prioridade
        self.tempo_chegada = tempo_chegada
        self.tempo_restante = tempo_cpu
        self.estado = "READY"

    def __str__(self):
        return (f"ID: {self.id} | CPU: {self.tempo_cpu}s | Prioridade: {self.prioridade} | "
                f"Estado: {self.estado} | Chegada: {self.tempo_chegada}s")