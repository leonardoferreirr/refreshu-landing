#!/usr/bin/env python3
"""
Recupera o dicionario pt-BR que ja existe, no formato novo.

A versao /pt/ foi gerada a partir do ingles pelo traduzir.py antigo, entao as
duas arvores tem a mesma estrutura e as unidades pareiam uma a uma. Isso deixa
migrar a traducao inteira sem redigitar nada, e sem perder o trabalho de copy
que ja passou por revisao.

O cuidado: o script antigo tambem reescrevia caminho (assets/ virava
../assets/) e o seletor de idioma. Esses pares diferem sem serem traducao, e
entrariam no dicionario como lixo. Eles sao detectados e separados aqui.

    python3 i18n_migrar_pt.py

Saida: i18n/pt.json  e um relatorio do que foi descartado.
"""
import os, re, json, sys
import i18n_core as core

RAIZ = os.path.dirname(os.path.abspath(__file__))
PARES = ['index.html', 'signin.html', 'portal.html']

# Diferencas que o script antigo produzia sem serem traducao.
RUIDO = (
    ('../assets/', 'assets/'),
    ('../console.html', 'console.html'),
    ('../sales.html', 'sales.html'),
    ('../assessment.html', 'assessment.html'),
    ('../signin-team.html', 'signin-team.html'),
    ('../signin-sales.html', 'signin-sales.html'),
    ('../signup.html', 'signup.html'),
    ('../recover.html', 'recover.html'),
)


def normaliza(s):
    """Desfaz as reescritas de caminho, para comparar so o texto."""
    for de, para in RUIDO:
        s = s.replace(de, para)
    s = s.replace('hreflang="pt-BR" aria-current="page"', 'hreflang="pt-BR"')
    s = s.replace('hreflang="en" aria-current="page"', 'hreflang="en"')
    s = re.sub(r'class="lang__b(?: is-on)?"', 'class="lang__b"', s)
    s = re.sub(r'href="(?:\.\./|\./|pt/)"', 'href=""', s)
    s = re.sub(r'href="pt/([\w.-]*)"', r'href="\1"', s)
    return s


def main():
    dic = {}
    conflitos, so_caminho, iguais = [], 0, 0

    for nome in PARES:
        en_html = open(os.path.join(RAIZ, nome), encoding='utf-8').read()
        pt_html = open(os.path.join(RAIZ, 'pt', nome), encoding='utf-8').read()
        en = core.unidades(en_html)
        pt = core.unidades(pt_html)
        if len(en) != len(pt):
            print(f'  {nome}: {len(en)} x {len(pt)} unidades, nao pareia. Pulando.')
            continue

        for a, b in zip(en, pt):
            o, t = a['texto'], b['texto']
            if o == t:
                iguais += 1
                continue
            if normaliza(o) == normaliza(t):
                so_caminho += 1
                continue
            if o in dic and dic[o] != t:
                conflitos.append((nome, o, dic[o], t))
                continue
            dic[o] = t

    os.makedirs(os.path.join(RAIZ, 'i18n'), exist_ok=True)
    destino = os.path.join(RAIZ, 'i18n', 'pt.json')
    json.dump(dic, open(destino, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, sort_keys=True)

    print(f'  traduzidos recuperados .....: {len(dic)}')
    print(f'  identicos nos dois idiomas ..: {iguais}  (nome proprio, numero, sigla)')
    print(f'  diferenca so de caminho .....: {so_caminho}  (descartados, viram regra)')
    print(f'  conflitos ...................: {len(conflitos)}')
    for nome, o, v1, v2 in conflitos[:12]:
        print(f'   · [{nome}] {o[:60]!r}')
        print(f'       ja tinha: {v1[:70]!r}')
        print(f'       agora:    {v2[:70]!r}')
    print(f'\n  dicionario em i18n/pt.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
