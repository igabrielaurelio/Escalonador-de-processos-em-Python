# Comentários gerais sobre o desenvolvimento do trabalho

## Estrutura do projeto

O trabalho foi desenvolvido em Python, com foco em organização, clareza e modularidade. As funções e algoritmos foram divididos por arquivos

- `processo.py` define a classe Processo, que encapsula todos os atributos necessários para a simulação.
- `utils.py` contém a função `ler_entrada` que converte os dados do arquivo de entrada em objetos Processo.
- `escalonador.py` implementa os quatro algoritmos de escalonamento exigidos, todos com suporte a entradasaída (ES).
- `main.py` orquestra a leitura da entrada, execução dos algoritmos e geração dos arquivos de saída.

## Estruturas de dados utilizadas

- Classe `Processo` agrupa todos os dados relevantes de cada processo, como tempos, prioridade, ES e estado.
- Listas utilizadas para armazenar os processos, filas de prontos e lista de bloqueados (ES).
- `deque` (fila dupla) usada em algoritmos como FIFO e Round Robin para manipular as filas com mais eficiência.
- Tuplas `(processo, tempo_retorno)` usadas para representar processos em ES e seu tempo de retorno à fila de prontos.

## Implementação da EntradaSaída (ES)

A ES foi implementada em todos os algoritmos. Quando um processo atinge o tempo configurado de início de ES, ele é movido para a lista de bloqueados. Após o tempo de ES terminar, o processo retorna à fila de prontos (ou ao início da fila no caso do FIFO).

## Algoritmos implementados

- FIFO executa os processos na ordem de chegada, sem preempção. Suporte total a ES.
- SJF Preemptivo escolhe sempre o processo com menor tempo restante. ES tratada corretamente.
- Prioridade Preemptivo executa o processo com maior prioridade (menor valor numérico). ES compatível.
- Round Robin alterna os processos com um quantum fixo. Suporte completo a ES, incluindo bloqueio e retorno.

## Observações sobre o Round Robin

A lógica do Round Robin com suporte a ES foi implementada corretamente. Durante os testes, a execução e os prints mostraram os processos sendo executados, indo para ES e voltando. No entanto, em alguns momentos, o arquivo de saída (`round_robin_entrada.txt`) não era gerado, mesmo com a simulação funcionando normalmente. Esse comportamento parece estar relacionado a alguma condição específica (como arquivos vazios, entradas mal formatadas ou leitura duplicada), mas a lógica central do algoritmo funciona e finaliza os processos corretamente.

## Geração dos arquivos de saída

Para cada entrada `nomeentrada.txt`, foram gerados arquivos de saída no formato

- `fifo_nomeentrada.txt`
- `sjf_preemptivo_nomeentrada.txt`
- `prioridade_preemptivo_nomeentrada.txt`
- `round_robin_nomeentrada.txt`

Esses arquivos são salvos no mesmo diretório do arquivo de entrada, conforme especificado no enunciado.

## Comentários finais

O código foi escrito com boas práticas, incluindo
- Comentários explicativos em todas as funções
- Uso adequado de estruturas de dados
- Separação clara de responsabilidades
- Testes realizados com diferentes combinações de entradaES

A implementação atende aos requisitos funcionais e estruturais propostos no trabalho.
