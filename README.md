📄 Mini Simulador de Gerenciamento de E/S – SCAN e C-SCAN

Este projeto implementa um mini simulador de escalonamento de E/S em disco, atendendo aos requisitos da prática da disciplina de Sistemas Operacionais. O programa simula o funcionamento do braço de disco, calcula tempos de seek e exibe a ordem real de visitação dos blocos.

O simulador funciona no terminal e permite configurar totalmente a simulação.

🎯 Objetivos da Atividade

O programa implementa:

✔ Configuração do ambiente

Definição do intervalo mínimo e máximo de blocos do disco.

Fornecimento da lista de blocos a serem visitados:

Entrada manual pelo usuário

Ou geração de blocos aleatórios

Definição da posição inicial da cabeça de leitura (opcional).

✔ Algoritmos implementados

O simulador oferece dois algoritmos de escalonamento:

SCAN

C-SCAN

Ambos mostram:

Ordem real dos blocos visitados

Tempo de seek parcial em cada movimento

Tempo total de seek (incluindo movimentos até extremidades quando aplicável)

✔ Apresentação clara da simulação

# Mini Simulador de Gerenciamento de E/S – SCAN e C-SCAN

Este repositório contém um simulador de escalonamento de braço de disco desenvolvido para a prática da disciplina de Sistemas Operacionais. O simulador calcula tempos de seek, exibe a ordem real de visitação dos blocos e permite comparar variantes (SCAN clássico, SCAN otimizado e C-SCAN).

Principais arquivos
- `pratica_ES.final.py` — código principal com menu interativo, implementação de `ScanSimulator` e `CScanSimulator`, opção `go_to_ends` (modo clássico vs otimizado) e modo `--demo` embutido.
- `demo_pratica_ES.py` — demonstração separada que importa as classes do script principal e executa cenários predefinidos (útil para gravação de vídeo).

Funcionalidades implementadas
- Definir intervalo mínimo e máximo de blocos.
- Fornecer a ordem de blocos manualmente ou gerar aleatoriamente (geração com N elementos).
- Definir posição inicial da cabeça (opcional).
- Implementação dos algoritmos SCAN (clássico e otimizado) e C-SCAN (circular).
- Impressão detalhada de cada movimento no formato `origem -> destino = u.t.` e soma total de seek.

Saídas esperadas
- O programa imprimirá a lista de blocos visitados, cada movimento com seu tempo de seek parcial e o tempo total acumulado.
- No caso de C-SCAN será exibido o salto circular (ex.: `199 -> 0 = 199 u.t.`) e esse valor será contabilizado no total.

Participantes
- Esdras Rodrigues
- Rony Elias de Oliveira

Licença / Uso
- Código para fins acadêmicos.
