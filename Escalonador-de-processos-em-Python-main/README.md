# Comentários Gerais sobre o Desenvolvimento do Trabalho

## Estrutura do Projeto

O trabalho foi desenvolvido em Python, com foco em organização, clareza e modularidade. As funcionalidades foram divididas em arquivos distintos:

- `processo.py`: define a classe `Processo`, que encapsula todos os atributos necessários para a simulação.
- `utils.py`: contém a função `ler_entrada`, responsável por converter os dados do arquivo de entrada em objetos `Processo`.
- `escalonador.py`: implementa os quatro algoritmos de escalonamento exigidos, todos com suporte a operações de entrada/saída (E/S).
- `main.py`: coordena a leitura dos dados, a execução dos algoritmos e a geração dos arquivos de saída.

## Estruturas de Dados Utilizadas

- A classe `Processo` centraliza as informações de cada processo, como tempos de CPU, prioridade, parâmetros de E/S e estado.
- Listas são utilizadas para armazenar os processos, filas de prontos e a lista de bloqueados (E/S).
- A estrutura `deque` (fila dupla) foi utilizada nos algoritmos FIFO e Round Robin, proporcionando maior eficiência no gerenciamento das filas.
- Tuplas do tipo `(processo, tempo_retorno)` representam processos em E/S junto com o tempo em que devem retornar à fila de prontos.

## Implementação da Entrada/Saída (E/S)

A lógica de E/S foi implementada em todos os algoritmos. Quando um processo atinge o tempo configurado para início de E/S, ele é movido para a lista de bloqueados. Após o tempo de E/S, o processo retorna à fila de prontos (no início da fila no caso do FIFO).

## Algoritmos Implementados

- **FIFO**: executa os processos na ordem de chegada, sem preempção. Suporte total à E/S.
- **SJF Preemptivo**: escolhe sempre o processo com menor tempo restante. A lógica de E/S está corretamente integrada.
- **Prioridade Preemptivo**: executa o processo com maior prioridade (menor valor numérico). Compatível com operações de E/S.
- **Round Robin**: alterna entre os processos com um quantum fixo. Implementação completa da lógica de E/S, incluindo bloqueio e retorno dos processos.

## Geração dos Arquivos de Saída

Para cada entrada no formato `entrada.txt`, foram gerados arquivos de saída com os resultados de cada algoritmo, seguindo o padrão:

- `fifo_entrada.txt`
- `sjf_preemptivo_entrada.txt`
- `prioridade_preemptivo_entrada.txt`
- `round_robin_entrada.txt`

Os arquivos são salvos no mesmo diretório do arquivo de entrada, conforme as especificações do enunciado.

## Observações Finais

O código foi desenvolvido seguindo boas práticas de programação, incluindo:

- Comentários explicativos em todas as funções;
- Uso adequado e eficiente de estruturas de dados;
- Separacão clara de responsabilidades entre os módulos;
- Testes com diversas combinações de entrada, incluindo cenários com e sem E/S.

No entanto, ainda não foi possível obter a saída correta para alguns casos. Por exemplo:

- Saída de `fifo_entrada.txt`:  
  ```
  60,10  
  35,15  
  ```

- Saída de `prioridade_preemptivo_entrada.txt`:  
  ```
  70,20  
  20,0  
  ```

Esses resultados ainda não correspondem ao esperado, e não consegui resolver.

