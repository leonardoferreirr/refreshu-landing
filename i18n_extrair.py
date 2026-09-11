#!/usr/bin/env python3
"""
Levanta TODO texto traduzivel de cada pagina e escreve a lista de trabalho.

Por que existe: o traduzir.py antigo so sabia reclamar de chave do dicionario
que nao casou. Ele nao tinha como reclamar do contrario, que e o erro caro:
texto que esta na pagina e nunca entrou no dicionario. Esse texto sai em ingles
na versao traduzida e ninguem percebe ate o cliente abrir.

    python3 i18n_extrair.py            # todas as paginas
    python3 i18n_extrair.py portal     # so as que casam com 'portal'

Saida: i18n/unidades/<pagina>.json
"""
import os, sys, json
import i18n_core as core

RAIZ = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(RAIZ, 'i18n', 'unidades')


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    os.makedirs(DEST, exist_ok=True)
    paginas = sorted(f for f in os.listdir(RAIZ)
                     if f.endswith('.html') and filtro in f)
    if not paginas:
        print('nenhuma pagina casou com', repr(filtro))
        return 1

    print(f"{'pagina':<28}{'frases':>8}{'attrs':>7}{'palavras':>10}")
    print('-' * 53)
    tot_f = tot_a = tot_p = 0
    for nome in paginas:
        html = open(os.path.join(RAIZ, nome), encoding='utf-8').read()
        us = core.textos_unicos(html)
        frases = [u['texto'] for u in us if u['tipo'] == 'texto']
        attrs = [{'attr': u['attr'], 'texto': u['texto']}
                 for u in us if u['tipo'] == 'attr']
        pal = sum(core.palavras(s) for s in frases) \
            + sum(core.palavras(a['texto']) for a in attrs)
        json.dump(
            {'pagina': nome, 'frases': frases, 'atributos': attrs},
            open(os.path.join(DEST, nome.replace('.html', '.json')), 'w',
                 encoding='utf-8'),
            ensure_ascii=False, indent=1,
        )
        print(f'{nome:<28}{len(frases):>8}{len(attrs):>7}{pal:>10}')
        tot_f += len(frases); tot_a += len(attrs); tot_p += pal
    print('-' * 53)
    print(f"{'TOTAL':<28}{tot_f:>8}{tot_a:>7}{tot_p:>10}")
    print('\nlistas de trabalho em i18n/unidades/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
