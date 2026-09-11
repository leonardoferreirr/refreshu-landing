#!/usr/bin/env python3
"""
Gera as versoes traduzidas do site a partir do ingles.

O ingles e a fonte da verdade. Mexeu no texto de uma pagina? Roda este script
e os outros idiomas acompanham. Nunca editar /es/ ou /pt/ na mao.

    python3 i18n_traduzir.py           # todos os idiomas
    python3 i18n_traduzir.py es        # so o espanhol

O que este script faz e o antigo nao fazia:

  · troca texto por POSICAO, nao por busca. Chave curta nao corrompe mais
    frase longa, e a ordem do dicionario deixou de importar.
  · reclama de texto que ficou sem traducao, nao so de chave que sobrou.
  · corrige o link para pagina que nao existe no idioma. Antes, /pt/ apontava
    para legal.html dentro da propria pasta e dava 404 em 23 links.
  · monta o seletor de idioma a partir de um so lugar, e so oferece o idioma
    em que aquela pagina realmente existe.

Matriz de idiomas: a Plataforma (portal, vendas, console e os logins deles)
sai em ingles e espanhol. O site publico pode ter portugues tambem. Essa
divisao veio da Agata em 10/09/2026 e substitui a que estava no Anexo A.
"""
import os, re, sys, json, shutil
import i18n_core as core

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIC = os.path.join(RAIZ, 'i18n')

# Todas as paginas em ingles, que e a fonte.
TODAS = [
    'index.html', 'destination-sao-paulo.html', 'destination-rio.html',
    'legal.html', 'assessment.html',
    'signin.html', 'portal.html', 'recover.html',
    'signin-sales.html', 'sales.html',
    'signin-team.html', 'console.html',
]

# O site publico, aberto a quem nao tem conta. E o unico lugar onde o
# portugues pode continuar: a Agata pediu a Plataforma em ingles e espanhol.
PUBLICO = ['index.html', 'destination-sao-paulo.html', 'destination-rio.html',
           'legal.html', 'assessment.html']
PLATAFORMA = [p for p in TODAS if p not in PUBLICO]

IDIOMAS = {
    'es': {'lang': 'es', 'rotulo': 'Español', 'curto': 'ES', 'paginas': TODAS},

    # Portugues so na home, que e o que ja existia traduzido menos a
    # Plataforma. Estender para o site publico inteiro e trocar esta linha
    # por PUBLICO, e depende de decisao de escopo: sao 9.200 palavras a mais.
    'pt': {'lang': 'pt-BR', 'rotulo': 'Português', 'curto': 'PT',
           'paginas': ['index.html']},
}

RAIZ_IDIOMA = {'lang': 'en', 'rotulo': 'English', 'curto': 'EN',
               'paginas': TODAS}

MARCA_INI = core.MARCA_INI
MARCA_FIM = core.MARCA_FIM


# ---------------------------------------------------------------- caminhos --
def corrige_caminhos(html, paginas_do_idioma):
    """Ajusta os caminhos para uma pagina que agora vive um nivel abaixo.

    Pagina que nao existe neste idioma passa a apontar para a versao em
    ingles na raiz, em vez de gerar 404 dentro da propria pasta.
    """
    for attr in ('href', 'src', 'srcset'):
        html = html.replace(f'{attr}="assets/', f'{attr}="../assets/')
    html = html.replace('content="assets/', 'content="../assets/')

    def ajusta(m):
        alvo, resto = m.group(2), m.group(3)
        if alvo in paginas_do_idioma:
            return m.group(0)
        return f'{m.group(1)}="../{alvo}{resto}"'

    return re.sub(r'\b(href|action)="([\w-]+\.html)([^"]*)"', ajusta, html)


# ------------------------------------------------------------ idioma da tag --
def marca_idioma(html, codigo):
    return re.sub(r'<html([^>]*?)\blang="[^"]*"', rf'<html\1lang="{codigo}"', html, count=1)


# ------------------------------------------------------------- seletor -------
def url(pagina, de, para):
    """Endereco da `pagina` no idioma `para`, visto de dentro do idioma `de`.

    O ingles mora na raiz; os outros idiomas em uma pasta com o codigo deles.
    """
    indice = pagina == 'index.html'
    if de == para:
        if indice:
            return 'index.html' if de == 'en' else './'
        return pagina
    subir = '' if de == 'en' else '../'
    if para == 'en':
        return subir + ('' if indice else pagina) or './'
    return subir + para + '/' + ('' if indice else pagina)


def seletor(pagina, idioma_atual):
    """Monta o seletor de idioma da pagina, com os idiomas que a tem.

    Sem bandeira, de proposito. Bandeira nomeia pais, nao idioma, e quem fala
    espanhol aqui esta nos Estados Unidos: uma bandeira da Espanha diria a
    coisa errada para uma cliente mexicana ou colombiana. Tres letras dizem
    a coisa certa em qualquer um dos casos.

    So entra o idioma em que aquela pagina existe de verdade, para o seletor
    nunca oferecer um caminho que termina em 404.
    """
    itens = []
    for cod, cfg in [('en', RAIZ_IDIOMA)] + sorted(IDIOMAS.items()):
        if pagina not in cfg['paginas']:
            continue
        atual = cod == idioma_atual
        itens.append(
            '<a class="lang__b{on}" href="{href}" hreflang="{lang}"{marca}'
            ' title="{rotulo}" aria-label="{rotulo}">'
            '<span class="lang__c">{curto}</span></a>'.format(
                on=' is-on' if atual else '',
                href=url(pagina, idioma_atual, cod),
                lang=cfg['lang'],
                marca=' aria-current="page"' if atual else '',
                rotulo=cfg['rotulo'],
                curto=cfg['curto'],
            )
        )
    if len(itens) < 2:
        return ''
    return ('<div class="lang" role="group" aria-label="Language">'
            + ''.join(itens) + '</div>')


def troca_seletor(html, pagina, idioma):
    novo = seletor(pagina, idioma)
    return re.sub(
        re.escape(MARCA_INI) + r'.*?' + re.escape(MARCA_FIM),
        lambda _: MARCA_INI + novo + MARCA_FIM,
        html, flags=re.S,
    )


# ------------------------------------------------------------------ build ----
def gera(codigo, cfg, dicionario):
    destino = os.path.join(RAIZ, codigo)
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    os.makedirs(destino)

    relatorio = []
    for pagina in cfg['paginas']:
        origem = os.path.join(RAIZ, pagina)
        if not os.path.exists(origem):
            print(f'  !! falta {pagina}')
            continue
        html = open(origem, encoding='utf-8').read()

        faltando = []
        html = core.aplicar(html, dicionario, faltando)
        html = corrige_caminhos(html, cfg['paginas'])
        html = marca_idioma(html, cfg['lang'])
        html = troca_seletor(html, pagina, codigo)

        open(os.path.join(destino, pagina), 'w', encoding='utf-8').write(html)
        relatorio.append((pagina, len(faltando), faltando))
    return relatorio


def main():
    alvo = sys.argv[1] if len(sys.argv) > 1 else ''
    idiomas = {k: v for k, v in IDIOMAS.items() if not alvo or k == alvo}
    if not idiomas:
        print('idioma desconhecido:', alvo, '· disponiveis:', ', '.join(IDIOMAS))
        return 1

    # o ingles tambem passa pelo build, so para o seletor ficar consistente
    for pagina in TODAS:
        caminho = os.path.join(RAIZ, pagina)
        if os.path.exists(caminho):
            html = open(caminho, encoding='utf-8').read()
            novo = troca_seletor(html, pagina, 'en')
            if novo != html:
                open(caminho, 'w', encoding='utf-8').write(novo)

    houve_falta = False
    for codigo, cfg in sorted(idiomas.items()):
        arq = os.path.join(DIC, f'{codigo}.json')
        if not os.path.exists(arq):
            print(f'\n{codigo}: sem dicionario em i18n/{codigo}.json'); continue
        dicionario = json.load(open(arq, encoding='utf-8'))
        print(f'\n{codigo}  ({cfg["rotulo"]}, {len(dicionario)} trechos no dicionario)')
        print('  ' + '-' * 58)
        rel = gera(codigo, cfg, dicionario)
        for pagina, n, _ in rel:
            estado = 'completa' if n == 0 else f'{n} trechos em ingles'
            print(f'  {codigo}/{pagina:<30}{estado}')
            houve_falta |= n > 0

        pendentes = [(p, f) for p, n, f in rel if n]
        if pendentes:
            saida = os.path.join(DIC, f'pendente-{codigo}.json')
            json.dump(
                {p: [u['texto'] for u in f] for p, f in pendentes},
                open(saida, 'w', encoding='utf-8'),
                ensure_ascii=False, indent=1,
            )
            print(f'\n  o que falta traduzir esta em i18n/pendente-{codigo}.json')

    if not houve_falta:
        print('\n  nenhum texto ficou em ingles.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
