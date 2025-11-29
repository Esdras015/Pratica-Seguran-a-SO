"""
Demo separado para `pratica_ES.final.py`.
Este script carrega o arquivo principal com `runpy.run_path` (sem executar o main) e executa cenários de demonstração
utilizando as classes definidas no arquivo principal.

Use: python demo_pratica_ES.py
"""
import runpy
import os
import random

BASE = os.path.dirname(__file__)
MAIN_SCRIPT = os.path.join(BASE, 'pratica_ES.final.py')

# Carrega o namespace do arquivo principal sem executar __main__
ns = runpy.run_path(MAIN_SCRIPT, run_name='pratica_module')

# Extrair simuladores
ScanSimulator = ns['ScanSimulator']
CScanSimulator = ns['CScanSimulator']

def demo():
    print('\n=== DEMONSTRAÇÃO: Cenários usando classes do script principal ===')

    bloco_min, bloco_max = 0, 199
    reqs = [98, 183, 37, 122, 14, 124, 65, 67]
    pos_inicial = 53

    print(f"\nCenário A: intervalo [{bloco_min},{bloco_max}], posição inicial {pos_inicial}, requisições: {reqs}")
    print("SCAN clássico (ir até extremidade)")
    s1 = ScanSimulator(bloco_min, bloco_max, reqs, direcao_inicial=1, posicao_inicial=pos_inicial, go_to_ends=True)
    s1.run()

    print("\nSCAN otimizado (não vai até a extremidade física sem necessidade)")
    s2 = ScanSimulator(bloco_min, bloco_max, reqs, direcao_inicial=1, posicao_inicial=pos_inicial, go_to_ends=False)
    s2.run()

    print("\nC-SCAN (circular)")
    c1 = CScanSimulator(bloco_min, bloco_max, reqs, posicao_inicial=pos_inicial)
    c1.run()

    # Cenário aleatório
    bloco_min2, bloco_max2 = 0, 99
    random_reqs = [random.randint(bloco_min2, bloco_max2) for _ in range(12)]
    pos2 = random.randint(bloco_min2, bloco_max2)
    print(f"\nCenário B (aleatório): intervalo [{bloco_min2},{bloco_max2}], posição inicial {pos2}, requisições: {random_reqs}")
    s3 = ScanSimulator(bloco_min2, bloco_max2, random_reqs, direcao_inicial=-1, posicao_inicial=pos2, go_to_ends=False)
    s3.run()

if __name__ == '__main__':
    demo()
