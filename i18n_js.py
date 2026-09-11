#!/usr/bin/env python3
"""
Levanta o texto de tela que nasce dentro do JavaScript.

Parte da interface nao esta no HTML: o rodape legal, os selos de confianca,
o catalogo de procedimentos e os rotulos que mudam por acao da pessoa. Esse
texto nao passa pelo extrator de paginas, e por isso saiu em ingles na
primeira versao em espanhol do app de vendas.

Duas fontes:

  1. o que esta escrito dentro de traduz('...'), inclusive quando a frase
     vem quebrada em varias linhas com +
  2. os campos de texto das listas de dados que o JS renderiza depois, que
     chegam em traduz() por variavel e nao por literal

    python3 i18n_js.py          # lista as chaves encontradas
"""
import os, re, sys, json

RAIZ = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(RAIZ, 'assets', 'js')

# 1. traduz('...'), aceitando concatenacao com + entre linhas
LITERAL = re.compile(
    r"traduz\(\s*((?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")(?:\s*\+\s*"
    r"(?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"))*)\s*[,)]",
    re.S,
)
PEDACO = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"")

# 2. listas de dados renderizadas depois. Cada regra e explicita de proposito:
#    varrer todo literal do arquivo traria seletor de CSS e nome de classe.
DADOS = {
    'foot.js': [re.compile(r"\[\s*'((?:[^'\\]|\\.)+)'\s*,\s*'legal\.html")],
    'trust.js': [re.compile(r"^\s*name:\s*'((?:[^'\\]|\\.)+)'", re.M),
                 re.compile(r"^\s*body:\s*'((?:[^'\\]|\\.)+)'", re.M)],
    'assessment.js': [re.compile(r"^\s*label:\s*'((?:[^'\\]|\\.)+)'", re.M),
                      re.compile(r"\bname:\s*'((?:[^'\\]|\\.)+)'"),
                      re.compile(r"\bdesc:\s*'((?:[^'\\]|\\.)+)'")],
}

# O catalogo tem um medico de exemplo que nenhuma tela renderiza. Sem esta
# excecao o extrator pediria traducao para nome proprio e para "19 years".
IGNORA = re.compile(r'^(Dr\.|[A-Z]{2}$)')


def desescapa(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')


def arquivos_de(paginas, raiz=RAIZ):
    """Quais .js as paginas dadas realmente carregam.

    Serve para o relatorio nao cobrar de um idioma o texto de uma tela que
    esse idioma nao tem. O portugues so publica a home, entao o rodape legal
    do portal nao e uma pendencia dele.
    """
    usados = set()
    for nome in paginas:
        caminho = os.path.join(raiz, nome)
        if not os.path.exists(caminho):
            continue
        html = open(caminho, encoding='utf-8').read()
        usados.update(re.findall(r'src="assets/js/([\w.\-]+\.js)"', html))
    usados.discard('i18n.js')
    return usados


def chaves(apenas=None):
    achadas = []
    for arq in sorted(os.listdir(JS)):
        if not arq.endswith('.js') or arq == 'i18n.js':
            continue
        if apenas is not None and arq not in apenas:
            continue
        src = open(os.path.join(JS, arq), encoding='utf-8').read()

        for m in LITERAL.finditer(src):
            partes = [desescapa(a if a is not None else b)
                      for a, b in PEDACO.findall(m.group(1))]
            frase = ''.join(partes).strip()
            if frase and frase not in achadas:
                achadas.append(frase)

        for rx in DADOS.get(arq, []):
            for m in rx.finditer(src):
                frase = desescapa(m.group(1)).strip()
                if frase and not IGNORA.match(frase) and frase not in achadas:
                    achadas.append(frase)
    return achadas


def main():
    ks = chaves()
    for k in ks:
        print(' ·', k[:110])
    print(f'\n{len(ks)} trechos de tela vivem no JavaScript')
    json.dump(ks, open(os.path.join(RAIZ, 'i18n', 'js-chaves.json'), 'w',
                       encoding='utf-8'), ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
