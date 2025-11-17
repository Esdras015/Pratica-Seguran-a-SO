# pratica_ES_mod.py
import random
import sys

def ler_intervalo():
    while True:
        try:
            minimo = int(input("Informe bloco mínimo (ex.: 0): ").strip())
            maximo = int(input("Informe bloco máximo (ex.: 100): ").strip())
            if minimo >= maximo:
                print("O bloco mínimo deve ser menor que o máximo. Tente novamente.")
                continue
            return minimo, maximo
        except ValueError:
            print("Entrada inválida. Informe números inteiros.")

def ler_requisicoes(bloco_min, bloco_max):
    print("Como deseja fornecer as requisições?")
    print(" 1 - Lista manual (ex.: 34,2,89,10)")
    print(" 2 - Gerar aleatoriamente (formato: r <quantidade>, ex.: r 10)")
    escolha = input("Escolha 1 ou 2 / ou digite 'r N': ").strip()
    if escolha.startswith('r') or escolha.startswith('R'):
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
    # escolha 2
    if escolha == '2':
        n = int(input("Quantas requisições aleatórias gerar? "))
        return [random.randint(bloco_min, bloco_max) for _ in range(n)]
    # fallback
    return []

def escolher_algoritmo():
    while True:
        a = input("Escolha algoritmo (scan / cscan / both): ").strip().lower()
        if a in ('scan','cscan','both'):
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
        for o,d,t in self.partial_times:
            print(f"  {o} -> {d} = {t} u.t.")
        print(f"\nTempo total de seek: {self.total_seek} u.t.")

class ScanSimulator(SimuladorBase):
    def __init__(self, bloco_min, bloco_max, requisicoes, direcao_inicial=1, posicao_inicial=None):
        super().__init__(bloco_min, bloco_max, posicao_inicial)
        self.reqs = requisicoes[:]  # copia
        self.direcao = direcao_inicial  # 1 crescente, -1 decrescente

    def run(self):
        print("=============================== SCAN ==================================")
        print(f"Intervalo: [{self.bloco_min}, {self.bloco_max}] - Posição inicial: {self.posicao} - Direção inicial: {'crescente' if self.direcao==1 else 'decrescente'}")
        # separar em dois grupos
        left = sorted([r for r in self.reqs if r < self.posicao])
        right = sorted([r for r in self.reqs if r >= self.posicao])

        if self.direcao == 1:
            # processar direita (asc)
            for r in right:
                self.mover_para(r)
            # se houver requisições à esquerda, mover até extremidade máxima (se não estiver já), contar seek
            if left:
                if self.posicao != self.bloco_max:
                    self.mover_para(self.bloco_max)
                # inverter e processar left em ordem decrescente
                for r in reversed(left):
                    self.mover_para(r)
        else:
            # direcao decrescente: processar left (desc)
            for r in reversed(left):
                self.mover_para(r)
            if right:
                if self.posicao != self.bloco_min:
                    self.mover_para(self.bloco_min)
                for r in right:
                    self.mover_para(r)

        self.resumo()

class CScanSimulator(SimuladorBase):
    def __init__(self, bloco_min, bloco_max, requisicoes, posicao_inicial=None):
        super().__init__(bloco_min, bloco_max, posicao_inicial)
        self.reqs = requisicoes[:]

    def run(self):
        print("============================== C-SCAN =================================")
        print(f"Intervalo: [{self.bloco_min}, {self.bloco_max}] - Posição inicial: {self.posicao} - Direção: crescente (circular)")
        # processa tudo >= pos em ordem asc
        right = sorted([r for r in self.reqs if r >= self.posicao])
        left = sorted([r for r in self.reqs if r < self.posicao])

        for r in right:
            self.mover_para(r)

        if left:
            # mover até o final (max) e então pular para min (contabilizando seek do max->min)
            if self.posicao != self.bloco_max:
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

def main():
    print("Simulador de escalonamento de braço de disco (SCAN / C-SCAN) - Versão melhorada")
    bloco_min, bloco_max = ler_intervalo()
    requisicoes = ler_requisicoes(bloco_min, bloco_max)
    algoritmo = escolher_algoritmo()
    # posição inicial opcional
    pos_inicial = input("Deseja informar posição inicial? (Enter p/aleatória ou digite número): ").strip()
    pos = None
    if pos_inicial != '':
        pos = int(pos_inicial)

    if algoritmo in ('scan','both'):
        direc = input("Direção inicial para SCAN (1 para crescente / -1 para decrescente) [default 1]: ").strip()
        direc_val = 1
        if direc == '-1':
            direc_val = -1
        scan = ScanSimulator(bloco_min, bloco_max, requisicoes, direc_val, pos)
        scan.run()

    if algoritmo in ('cscan','both'):
        cscan = CScanSimulator(bloco_min, bloco_max, requisicoes, pos)
        cscan.run()

if __name__ == "__main__":
    main()
