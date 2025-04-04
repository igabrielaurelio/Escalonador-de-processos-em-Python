from processos import Processo

def ler_arquivo(arquivo):
    processos = []
    
    with open(arquivo, "r") as f:
        linhas = f.readlines()

    quantum = int(linhas[-1].strip())  # Última linha contém o quantum
    for i, linha in enumerate(linhas[:-1]):  # Ignorar a última linha
        dados = linha.strip().split(",")  # Separar por vírgula
        
        # Converter para os tipos corretos, tratando valores vazios
        tempo_cpu = int(dados[0])
        precisa_es = int(dados[1])
        tempo_es = int(dados[2]) if dados[2] else 0
        inicio_es = int(dados[3]) if dados[3] else 0
        prioridade = int(dados[4])
        tempo_chegada = int(dados[5])

        # Criar um novo processo e adicioná-lo à lista
        processo = Processo(i + 1, tempo_cpu, precisa_es, tempo_es, inicio_es, prioridade, tempo_chegada)
        processos.append(processo)

    return processos, quantum
