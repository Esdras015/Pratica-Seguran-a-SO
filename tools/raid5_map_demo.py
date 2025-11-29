# Demonstração do mapeamento RAID-5 (paridade rotativa)
D = 3
# Mapa final do demo_run.py: 'O' ocupado, '-' livre
map_str = 'OOOOOOOOOOOOO-O-'
num = len(map_str)
blocks = [c == 'O' for c in map_str]

print('Mapa linear (índice : ocupado):')
for i, occ in enumerate(blocks):
    print(f'{i:2d}: {"O" if occ else "-"}')

print('\nMapeamento por disco (RAID-5, paridade rotativa):')
# disks collect chars
disks = [[] for _ in range(D)]
for i in range(num):
    disk = i % D
    stripe = i // D
    parity_disk = stripe % D
    occupied = blocks[i]
    if occupied:
        ch = 'P' if disk == parity_disk else 'O'
    else:
        ch = '-'
    disks[disk].append(ch)

for d in range(D):
    print(f'Disco {d}: {"".join(disks[d])}')

print('\nInterpretação:')
print('- Cada stripe (grupo de D blocos) tem 1 bloco de paridade (P) em disco parity_disk = stripe % D')
print('- Assim, cada disco terá "P" em múltiplas posições (uma por stripe onde o disco é dedicado à paridade)\n')
