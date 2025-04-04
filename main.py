from ler_arquivo import ler_arquivo

# Lendo processos do arquivo
processos, quantum = ler_arquivo("arquivo.txt")

# Exibindo os processos lidos
for p in processos:
    print(p)

print(f"Quantum (para Round Robin): {quantum}s")
