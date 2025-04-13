from processo import Processo

def ler_entrada(nome_arquivo):
    """
    Lê o arquivo de entrada e converte seus dados em uma lista de objetos Processo.
    
    Espera um arquivo com múltiplas linhas:
        - Cada linha representa um processo no formato:
            tempo_cpu, tem_e_s, tempo_e_s, inicio_e_s, prioridade, tempo_chegada
        - A última linha contém apenas o quantum (usado no Round Robin)

    Retorna:
        - Lista de objetos Processo
        - Valor inteiro do quantum
    """
    processos = []
    quantum = None

    # Abre o arquivo e lê todas as linhas, ignorando linhas vazias
    with open(nome_arquivo, 'r') as arq:
        linhas = [linha.strip() for linha in arq if linha.strip()]

    # Última linha do arquivo deve conter apenas o quantum
    try:
        quantum = int(linhas[-1])
    except ValueError:
        raise ValueError("A última linha do arquivo deve ser o quantum (um valor inteiro).")

    # Processa todas as linhas menos a última (quantum)
    for linha in linhas[:-1]:
        partes = [item.strip() for item in linha.split(',')]

        # Validação: cada linha de processo precisa ter pelo menos 6 campos
        if len(partes) < 6:
            print("Linha com dados insuficientes:", linha)
            continue

        try:
            # Conversão segura dos campos para inteiros
            tempo_cpu = int(partes[0])
            tem_e_s = int(partes[1])
            tempo_e_s = int(partes[2]) if partes[2] else 0
            inicio_e_s = int(partes[3]) if partes[3] else 0
            prioridade = int(partes[4])
            tempo_chegada = int(partes[5])
        except ValueError:
            print("Erro na conversão dos dados na linha:", linha)
            continue

        # Cria objeto Processo com os dados da linha
        processos.append(Processo(tempo_cpu, tem_e_s, tempo_e_s, inicio_e_s, prioridade, tempo_chegada))

    return processos, quantum

# Teste simples da função de leitura (executado se rodar o script diretamente)
if __name__ == '__main__':
    processos, quantum = ler_entrada('entrada.txt')
    print("Processos:", processos)
    print("Quantum:", quantum)
