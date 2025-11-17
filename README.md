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

O programa imprime:

Lista final de blocos visitados

Caminho percorrido

Movimentos (origem → destino)

Seek parcial e seek total ao final
