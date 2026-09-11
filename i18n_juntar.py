#!/usr/bin/env python3
"""
Junta um lote de traducoes ao dicionario de um idioma.

    python3 i18n_juntar.py es lote.json
    python3 i18n_juntar.py pt lote.json --forcar

Sem --forcar, uma chave que ja existe com valor diferente e mostrada e NAO e
sobrescrita. E de proposito: traducao ja revisada nao deve ser trocada por
engano num lote novo.

Entrada valida: um objeto JSON de "trecho em ingles" para "trecho traduzido".
"""
import os, sys, json

RAIZ = os.path.dirname(os.path.abspath(__file__))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    forcar = '--forcar' in sys.argv
    if len(args) != 2:
        print(__doc__.strip())
        return 2
    idioma, lote = args

    destino = os.path.join(RAIZ, 'i18n', f'{idioma}.json')
    atual = json.load(open(destino, encoding='utf-8')) if os.path.exists(destino) else {}
    novo = json.load(open(lote, encoding='utf-8'))

    entrou, igual, choque = 0, 0, []
    for k, v in novo.items():
        if k in atual:
            if atual[k] == v:
                igual += 1
                continue
            choque.append((k, atual[k], v))
            if not forcar:
                continue
        atual[k] = v
        entrou += 1

    json.dump(atual, open(destino, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, sort_keys=True)

    print(f'  {idioma}: {entrou} entraram, {igual} ja iguais, '
          f'{len(choque)} em conflito, {len(atual)} no total')
    for k, a, b in choque[:10]:
        print(f'   · {k[:66]!r}')
        print(f'       tinha: {a[:70]!r}')
        print(f'       lote:  {b[:70]!r}')
    if choque and not forcar:
        print('     (nao sobrescrito. use --forcar se o lote e que esta certo)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
