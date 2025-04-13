from utils import ler_entrada
from escalonador import fifo, sjf_preemptivo, prioridade_preemptivo, round_robin

def salvar_saida(nome_arquivo_saida, processos, algoritmo):
    """
    Salva os resultados da simulação em um arquivo de saída.
    Cada linha contém: tempo_finalizacao, tempo_espera para cada processo.
    Exemplo:
        16,7
        9,3
    """
    with open(nome_arquivo_saida, 'w') as arq:
        for proc in processos:
            arq.write(f"{proc.tempo_finalizacao},{proc.tempo_espera}\n")
    print(f"Saída salva em '{nome_arquivo_saida}' para o algoritmo {algoritmo}")

def main():
    # Nome do arquivo de entrada (deve estar no mesmo diretório)
    nome_arquivo_entrada = 'entrada.txt'

    # Leitura dos processos e do quantum para o Round Robin
    processos, quantum = ler_entrada(nome_arquivo_entrada)

    # -------------------------------
    # Algoritmo FIFO (sem preempção)
    # -------------------------------
    processos_fifo = fifo(processos)
    salvar_saida(f"fifo_{nome_arquivo_entrada}", processos_fifo, "FIFO")

    # ---------------------------------------
    # Algoritmo SJF Preemptivo (menor restante)
    # ---------------------------------------
    processos_sjf = sjf_preemptivo(processos)
    salvar_saida(f"sjf_preemptivo_{nome_arquivo_entrada}", processos_sjf, "SJF Preemptivo")

    # ----------------------------------------
    # Algoritmo de Prioridade Preemptivo
    # ----------------------------------------
    processos_prioridade = prioridade_preemptivo(processos)
    salvar_saida(f"prioridade_preemptivo_{nome_arquivo_entrada}", processos_prioridade, "Prioridade Preemptivo")

    # ----------------------------------------
    # Algoritmo Round Robin com nova leitura
    # (precisa recarregar processos para não usar os já modificados)
    # ----------------------------------------
    processos_rr, quantum = ler_entrada(nome_arquivo_entrada)
    processos_rr = round_robin(processos_rr, quantum)
    salvar_saida(f"round_robin_{nome_arquivo_entrada}", processos_rr, "Round Robin")

if __name__ == '__main__':
    # Ponto de entrada principal do programa
    main()
