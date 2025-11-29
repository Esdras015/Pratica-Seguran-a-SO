"""
pratica_ES.final.py
Versão incrementada com menu interativo e modo de demonstração (--demo).

Este script implementa simuladores SCAN e C-SCAN e um modo de demonstração
que exibe explicitamente os requisitos solicitados pelo professor.
"""

import random
import sys
import argparse


def ler_intervalo(prompt_min="Informe bloco mínimo (ex.: 0): ", prompt_max="Informe bloco máximo (ex.: 199): "):
    while True:
        try:
            minimo = int(input(prompt_min).strip())
            maximo = int(input(prompt_max).strip())
            if minimo >= maximo:
                print("O bloco mínimo deve ser menor que o máximo. Tente novamente.")
                continue
            return minimo, maximo
        except ValueError:
            print("Entrada inválida. Informe números inteiros.")


def ler_requisicoes_interativas(bloco_min, bloco_max):
    print("\nComo deseja fornecer as requisições?")
    print(" 1 - Lista manual (ex.: 34,2,89,10)")
    print(" 2 - Gerar aleatoriamente ")
    print(" 3 - Formato rápido: r N (ex.: r 10) -> gera N aleatórias")
    escolha = input("Escolha 1, 2 ou 3 / ou digite 'r N': ").strip()
    if escolha.lower().startswith('r'):
        parts = escolha.split()
        if len(parts) == 2 and parts[1].isdigit():
            n = int(parts[1])
        else:
            n = int(input("Quantas requisições aleatórias gerar? "))
        return [random.randint(bloco_min, bloco_max) for _ in range(n)]
    if escolha == '1':
        s = input("Digite a lista de blocos separados por vírgula: ").strip()
        lista = [int(x.strip()) for x in s.split(',') if x.strip() != '']
        for b in lista:
            if b < bloco_min or b > bloco_max:
                raise ValueError(f"Bloco {b} fora do intervalo [{bloco_min}, {bloco_max}]")
        return lista
    if escolha == '2':
        n = int(input("Quantas requisições aleatórias gerar? "))
        return [random.randint(bloco_min, bloco_max) for _ in range(n)]
    print("Opção inválida. Retornando lista vazia.")
    return []


def escolher_algoritmo_interativo():
    while True:
        a = input("Escolha algoritmo (scan / cscan / both): ").strip().lower()
        if a in ('scan', 'cscan', 'both'):
            return a
        print("Opção inválida. Escolha scan, cscan ou both.")


class SimuladorBase:
    def __init__(self, bloco_min, bloco_max, posicao_inicial=None):
        self.bloco_min = bloco_min
        self.bloco_max = bloco_max
        self.posicao = posicao_inicial if posicao_inicial is not None else random.randint(bloco_min, bloco_max)
        self.visited = []
        self.partial_times = []
        self.total_seek = 0

    def reset(self, posicao_inicial=None):
        self.posicao = posicao_inicial if posicao_inicial is not None else random.randint(self.bloco_min, self.bloco_max)
        self.visited = []
        self.partial_times = []
        self.total_seek = 0

    def mover_para(self, destino):
        seek = abs(self.posicao - destino)
        self.partial_times.append((self.posicao, destino, seek))
        self.total_seek += seek
        self.visited.append(destino)
        # atualizar posição
        self.posicao = destino

    def resumo(self):
        print("\nOrdem de blocos visitados:")
        print(self.visited)
        print("\nDetalhes de seek (origem -> destino = u.t.):")
        for o, d, t in self.partial_times:
            print(f"  {o} -> {d} = {t} u.t.")
        print(f"\nTempo total de seek: {self.total_seek} u.t.")


class ScanSimulator(SimuladorBase):
    def __init__(self, bloco_min, bloco_max, requisicoes, direcao_inicial=1, posicao_inicial=None, go_to_ends=True):
        super().__init__(bloco_min, bloco_max, posicao_inicial)
        self.reqs = requisicoes[:]  # copia
        self.direcao = direcao_inicial  # 1 crescente, -1 decrescente
        self.go_to_ends = go_to_ends  # se True, mover até extremidades físicas (SCAN clássico); se False, otimiza indo só até último pedido

    def run(self):
        print("\n=============================== SCAN ==================================")
        print(f"Intervalo: [{self.bloco_min}, {self.bloco_max}] - Posição inicial: {self.posicao} - Direção inicial: {'crescente' if self.direcao==1 else 'decrescente'} - modo: {'extremidades' if self.go_to_ends else 'otimizado'}")
        # separar em dois grupos
        left = sorted([r for r in self.reqs if r < self.posicao])
        right = sorted([r for r in self.reqs if r >= self.posicao])

        if self.direcao == 1:
            # processar direita (asc)
            for r in right:
                self.mover_para(r)
            # se houver requisições à esquerda
            if left:
                # mover até extremidade máxima apenas se solicitada (caso contrário já estamos no último pedido)
                if self.go_to_ends and self.posicao != self.bloco_max:
                    self.mover_para(self.bloco_max)
                # inverter e processar left em ordem decrescente
                for r in reversed(left):
                    self.mover_para(r)
        else:
            # direcao decrescente: processar left (desc)
            for r in reversed(left):
                self.mover_para(r)
            if right:
                if self.go_to_ends and self.posicao != self.bloco_min:
                    self.mover_para(self.bloco_min)
                for r in right:
                    self.mover_para(r)

        self.resumo()


class CScanSimulator(SimuladorBase):
    def __init__(self, bloco_min, bloco_max, requisicoes, posicao_inicial=None, go_to_ends=True):
        super().__init__(bloco_min, bloco_max, posicao_inicial)
        self.reqs = requisicoes[:]
        # go_to_ends kept for API symmetry; C-SCAN typically moves to end before jumping
        self.go_to_ends = go_to_ends

    def run(self):
        print("\n============================== C-SCAN =================================")
        print(f"Intervalo: [{self.bloco_min}, {self.bloco_max}] - Posição inicial: {self.posicao} - Direção: crescente (circular)")
        # processa tudo >= pos em ordem asc
        right = sorted([r for r in self.reqs if r >= self.posicao])
        left = sorted([r for r in self.reqs if r < self.posicao])

        for r in right:
            self.mover_para(r)

        if left:
            # mover até o final (max) e então pular para min (contabilizando seek do max->min)
            if self.go_to_ends and self.posicao != self.bloco_max:
                self.mover_para(self.bloco_max)
            # salto circular max -> min (contabilizar seek)
            salto = abs(self.bloco_max - self.bloco_min)
            # representaremos o salto como movimento lógico (max -> min)
            # atualiza total_seek e registra salto como origem->destino
            self.partial_times.append((self.bloco_max, self.bloco_min, salto))
            self.total_seek += salto
            self.posicao = self.bloco_min
            # agora processar left em ordem asc
            for r in left:
                self.mover_para(r)

        self.resumo()


def demonstracao():
    """Roda cenários predefinidos para demonstrar requisitos da prática."""
    print("\n=== MODO DEMONSTRAÇÃO: validando requisitos da prática ===")

    # Cenário clássico (usado em muitas disciplinas):
    bloco_min, bloco_max = 0, 199
    reqs = [98, 183, 37, 122, 14, 124, 65, 67]
    pos_inicial = 53

    print(f"\nCenário 1: intervalo [{bloco_min},{bloco_max}], posição inicial {pos_inicial}, requisições: {reqs}")
    print("Executando SCAN (direção crescente)...")
    scan = ScanSimulator(bloco_min, bloco_max, reqs, direcao_inicial=1, posicao_inicial=pos_inicial)
    scan.run()

    print("\nExecutando C-SCAN (circular)...")
    cscan = CScanSimulator(bloco_min, bloco_max, reqs, posicao_inicial=pos_inicial)
    cscan.run()

    # Cenário aleatório para demonstrar geração automática
    bloco_min2, bloco_max2 = 0, 99
    random_reqs = [random.randint(bloco_min2, bloco_max2) for _ in range(12)]
    pos2 = random.randint(bloco_min2, bloco_max2)
    print(f"\nCenário 2 (aleatório): intervalo [{bloco_min2},{bloco_max2}], posição inicial {pos2}, requisições: {random_reqs}")
    scan2 = ScanSimulator(bloco_min2, bloco_max2, random_reqs, direcao_inicial=-1, posicao_inicial=pos2)
    scan2.run()

    print("\n--- Checklist de requisitos entregues ---")
    print("1) Informar intervalo de blocos: implementado (parâmetros nos cenários). ✅")
    print("2) Fornecer ordem de blocos: implementado (entrada manual ou gerada aleatoriamente). ✅")
    print("3) Implementar algoritmos: SCAN e C-SCAN implementados (C-SCAN é uma versão circular). ✅")
    print("4) Exibir ordem visitada: mostrado em cada execução (lista 'visited'). ✅")
    print("5) Exibir seek parcial e total: mostrado em cada execução (partial_times e total_seek). ✅")
    print("\nObservação: Para SCAN e C-SCAN, o tempo de seek inclui movimentos até extremidades e salto circular (C-SCAN).")


def menu_interativo():
    print("Simulador de escalonamento de braço de disco (SCAN / C-SCAN) - Menu interativo")
    bloco_min = None
    bloco_max = None
    requisicoes = []
    posicao = None
    while True:
        print("\nMenu:")
        print(" 1 - Definir intervalo de blocos")
        print(" 2 - Fornecer / gerar requisições")
        print(" 3 - Definir posição inicial (opcional)")
        print(" 4 - Executar SCAN")
        print(" 5 - Executar C-SCAN")
        print(" 6 - Executar ambos (SCAN e C-SCAN)")
        print(" 7 - Modo demonstração (pré-configurado)")
        print(" 0 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == '0':
            print("Saindo...")
            return
        if escolha == '1':
            bloco_min, bloco_max = ler_intervalo()
            print(f"Intervalo definido: [{bloco_min}, {bloco_max}]")
            continue
        if escolha == '2':
            if bloco_min is None:
                print("Defina o intervalo primeiro (opção 1).")
                continue
            requisicoes = ler_requisicoes_interativas(bloco_min, bloco_max)
            print(f"Requisições configuradas: {requisicoes}")
            continue
        if escolha == '3':
            if bloco_min is None:
                print("Defina o intervalo primeiro (opção 1).")
                continue
            val = input("Digite a posição inicial (ou Enter para aleatória): ").strip()
            if val == '':
                posicao = None
                print("Posição inicial aleatória selecionada.")
            else:
                try:
                    p = int(val)
                    if p < bloco_min or p > bloco_max:
                        print("Posição fora do intervalo.")
                    else:
                        posicao = p
                        print(f"Posição inicial definida: {posicao}")
                except ValueError:
                    print("Valor inválido.")
            continue
        if escolha in ('4','5','6'):
            if bloco_min is None or bloco_max is None:
                print("Defina o intervalo primeiro (opção 1).")
                continue
            if not requisicoes:
                print("Configure requisições primeiro (opção 2).")
                continue
            if escolha == '4' or escolha == '6':
                direc = input("Direção inicial para SCAN (1 crescente / -1 decrescente) [default 1]: ").strip()
                direc_val = 1
                if direc == '-1':
                    direc_val = -1
                scan = ScanSimulator(bloco_min, bloco_max, requisicoes, direc_val, posicao)
                scan.run()
            if escolha == '5' or escolha == '6':
                cscan = CScanSimulator(bloco_min, bloco_max, requisicoes, posicao)
                cscan.run()
            continue
        if escolha == '7':
            demonstracao()
            continue
        print("Opção inválida. Tente novamente.")


def parse_args():
    parser = argparse.ArgumentParser(description='Simulador SCAN / C-SCAN')
    parser.add_argument('--demo', action='store_true', help='Executar modo demonstração (pré-configurado)')
    parser.add_argument('--noninteractive', action='store_true', help='Executar sem menu interativo (não usado atualmente)')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.demo:
        demonstracao()
        return
    # modo interativo por padrão
    menu_interativo()


if __name__ == '__main__':
    main()
