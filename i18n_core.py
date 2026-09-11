#!/usr/bin/env python3
"""
Motor de idiomas do RefreshU. Um so tokenizador serve aos tres scripts:
extrair a lista de trabalho, traduzir e auditar o resultado.

A ideia central, e a diferenca para o traduzir.py antigo: cada trecho
traduzivel vem com as COORDENADAS dele dentro do arquivo. A traducao troca
fatias por posicao, de tras para frente, em vez de sair procurando texto pelo
documento. Isso elimina de uma vez:

  · a chave curta que corrompia frase longa ("Save" dentro de "Save. Refresh.")
  · a necessidade de ordenar o dicionario do maior para o menor
  · o texto que esta na pagina e nunca entrou no dicionario, porque agora o
    extrator ve a pagina inteira e nao depende de alguem ter lembrado da frase

O que e uma unidade: a fatia crua entre dois limites de bloco, com as tags
inline que estao no meio (<em>, <b>, um <a> dentro da frase). Guardar a frase
inteira e proposital, porque em espanhol e portugues a ordem das palavras muda
e traduzir pedaco solto quebraria a frase que tem <em> no meio.
"""
import re

# Tags que ficam DENTRO de uma frase e por isso viajam junto com ela.
INLINE = {
    'em', 'b', 'strong', 'i', 'span', 'small', 'sup', 'sub', 'code',
    'u', 'mark', 'abbr', 'time', 'wbr', 'q', 'cite', 'bdi', 'kbd', 'br',
}

# <a> e caso a parte: inline quando esta no meio de uma frase, limite quando
# e um link solto (menu, botao, lista de links). A regra esta em unidades().
ANCORA = 'a'

# Conteudo que nunca e texto de tela.
OPACAS = {'script', 'style', 'svg', 'noscript', 'template'}

# Elementos que nao tem fechamento, e por isso nunca contam no equilibrio.
VAZIAS = {
    'br', 'img', 'input', 'hr', 'meta', 'link', 'source', 'wbr',
    'area', 'base', 'col', 'embed', 'param', 'track',
}

# Atributos que chegam na pessoa, na tela ou no leitor de tela.
ATTRS = {
    'title', 'aria-label', 'alt', 'placeholder', 'aria-placeholder',
    'aria-roledescription', 'aria-valuetext', 'label',
    'data-label', 'data-empty', 'data-title', 'data-titulo',
}

# <meta> cujo content e texto de tela.
META_TRAD = {
    'description', 'og:title', 'og:description', 'og:site_name',
    'twitter:title', 'twitter:description',
    'apple-mobile-web-app-title', 'application-name',
}

# O seletor de idioma e montado pelo build, nao traduzido. Fica fora da
# extracao para que "English" e "Español" nao entrem no dicionario como se
# fossem texto de pagina.
MARCA_INI = '<!--LANG-->'
MARCA_FIM = '<!--/LANG-->'

TOKEN = re.compile(r'<[^>]*>|[^<]+', re.S)
TAG = re.compile(r'<\s*(/?)\s*([a-zA-Z][\w:-]*)([^>]*?)(/?)\s*>', re.S)
ATTR = re.compile(r'([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"', re.S)

# Sobra na ponta esquerda de uma unidade: uma tag de fechamento que nao abriu
# aqui dentro, ou um elemento vazio. Nos dois casos nao e texto e sai fora.
SOBRA_ESQ = re.compile(
    r'\s*(?:</[a-zA-Z][\w:-]*\s*>|<([a-zA-Z][\w:-]*)[^>]*>\s*</\1\s*>|'
    r'<[a-zA-Z][\w:-]*[^>]*/>)\s*'
)
# Tag de fechamento na ponta direita, candidata a sobra se nao abriu aqui.
SOBRA_DIR = re.compile(r'</([a-zA-Z][\w:-]*)\s*>\s*$')
# Tag de abertura na ponta direita: uma unidade nunca termina abrindo algo,
# porque nao sobrou conteudo dela para dentro.
ABRE_DIR = re.compile(r'<([a-zA-Z][\w:-]*)(?:\s[^>]*)?/?>\s*$')


def desequilibrio(html, ini, fim):
    """Acha as tags sem par dentro da fatia.

    Devolve (fim_do_ultimo_fechamento_orfao, inicio_da_primeira_abertura_orfa).
    Fechamento orfao e o que fechou algo aberto antes da fatia; abertura orfa
    e a que so vai fechar depois dela.
    """
    pilha, orfao_fecha, orfa_abre = [], None, None
    for m in TAG.finditer(html, ini, fim):
        nome = m.group(2).lower()
        if nome in VAZIAS or m.group(4):
            continue
        if m.group(1):
            if any(n == nome for n, _ in pilha):
                while pilha:
                    n, _ = pilha.pop()
                    if n == nome:
                        break
            else:
                orfao_fecha = m.end()
                pilha.clear()
                orfa_abre = None
        else:
            pilha.append((nome, m.start()))
    if pilha:
        orfa_abre = pilha[0][1]
    return orfao_fecha, orfa_abre


def apara(html, ini, fim):
    """Recorta a fatia ate ela ficar com as tags equilibradas.

    Sem isso a unidade chega ao tradutor com tag pendurada e volta como HTML
    invalido, porque a traducao substitui a fatia inteira. Acontece nas duas
    pontas: um </span> que fechou algo aberto antes do texto, e um <span> que
    so vai fechar depois do fim da unidade.
    """
    for _ in range(8):
        antes = (ini, fim)
        while ini < fim:
            m = SOBRA_ESQ.match(html, ini, fim)
            if not m or m.end() >= fim:
                break
            ini = m.end()
        while ini < fim:
            m = ABRE_DIR.search(html[ini:fim])
            if not m:
                break
            fim = ini + m.start()
        fecha_orfao, abre_orfa = desequilibrio(html, ini, fim)
        if fecha_orfao is not None:
            ini = fecha_orfao
        if abre_orfa is not None:
            fim = abre_orfa
        if (ini, fim) == antes:
            break
    return ini, min(max(fim, ini), len(html))

# Trecho que nao vale traducao: so numero, simbolo, entidade ou espaco.
SO_SIMBOLO = re.compile(
    r'^(?:\s|&[a-zA-Z]+;|&#\d+;|[\d.,:;/()\[\]{}#+%$*·•—–\-−|®©™°"\'!?…])*$'
)


def so_simbolo(s):
    return bool(SO_SIMBOLO.match(s))


def continua_a_frase(html, pos):
    """Depois de um </a>, diz se o que vem a seguir ainda e a mesma frase.

    Serve para separar duas coisas que parecem iguais no HTML: uma lista de
    links soltos, que sao unidades independentes, e um link no meio de um
    periodo, que tem que viajar junto com ele. A diferenca esta no que vem
    logo depois do fechamento: outro link ou uma tag de bloco encerram a
    frase; texto a continua.
    """
    sem_espaco = html[pos:pos + 400].lstrip()
    # So texto continua a frase. Qualquer tag logo depois do </a> significa
    # outro elemento, nao o resto do periodo: e a diferenca entre
    # "li a <a>Politica</a> e o <a>Aviso</a>." e um link de menu seguido do
    # proximo item.
    return bool(sem_espaco) and not sem_espaco.startswith('<')


def unidades(html):
    """Lista de trechos traduziveis, cada um com posicao no arquivo.

    Devolve dicts com:
      tipo  'texto' ou 'attr'
      ini   posicao inicial da fatia a substituir
      fim   posicao final
      texto conteudo atual da fatia
      attr  nome do atributo, quando tipo == 'attr'
    """
    achados = []
    opaca = 0            # >0: estamos dentro de script/style/svg
    ini = 0              # onde comeca a unidade de texto em construcao
    tem_texto = False    # a unidade ja tem texto, nao so tag
    pular_ate = 0        # fim do bloco do seletor de idioma, que nao e texto
    ancoras = 0          # <a> abertos DENTRO da unidade atual

    def fecha(fim):
        """Fecha a unidade, aparando as tags que sobraram nas pontas.

        Sem essa apara a unidade as vezes comeca com um </span> solto, que
        fechou algo aberto antes do texto, ou com um <span></span> vazio. Isso
        chega no tradutor como lixo e volta como HTML invalido.
        """
        nonlocal tem_texto, ancoras
        if tem_texto:
            comeco, termino = apara(html, ini, fim)
            bruto = html[comeco:termino]
            corte = bruto.strip()
            if corte and not so_simbolo(corte):
                desloc = len(bruto) - len(bruto.lstrip())
                achados.append({
                    'tipo': 'texto',
                    'ini': comeco + desloc,
                    'fim': comeco + desloc + len(corte),
                    'texto': corte,
                })
        tem_texto = False
        ancoras = 0

    for m in TOKEN.finditer(html):
        if m.start() < pular_ate:
            continue
        peca = m.group(0)

        # ---- texto solto ----
        if not peca.startswith('<'):
            if not opaca and peca.strip():
                tem_texto = True
            continue

        t = TAG.match(html, m.start())
        if not t:                        # comentario, doctype, condicional
            if peca.startswith('<!--'):
                fecha(m.start())
                # o bloco do seletor de idioma nao e texto de pagina
                if peca.strip() == MARCA_INI:
                    corte = html.find(MARCA_FIM, m.end())
                    pular_ate = len(html) if corte < 0 else corte + len(MARCA_FIM)
                    ini = pular_ate
                else:
                    ini = m.end()
            continue

        fechando = bool(t.group(1))
        nome = t.group(2).lower()

        # ---- regioes opacas ----
        if nome in OPACAS:
            fecha(m.start())
            opaca = max(0, opaca + (-1 if fechando else 1))
            ini = m.end()
            continue
        if opaca:
            continue

        # ---- atributos traduziveis da tag de abertura ----
        if not fechando:
            corpo_ini, corpo_fim = t.span(3)
            pares = {k.lower(): v for k, v in ATTR.findall(t.group(3))}
            for a in ATTR.finditer(html, corpo_ini, corpo_fim):
                nome_a = a.group(1).lower()
                valor = a.group(2)
                if not valor.strip() or so_simbolo(valor):
                    continue
                traduzivel = nome_a in ATTRS or (
                    nome == 'meta' and nome_a == 'content'
                    and (pares.get('name') or pares.get('property') or '').lower() in META_TRAD
                )
                if traduzivel:
                    achados.append({
                        'tipo': 'attr',
                        'ini': a.start(2),
                        'fim': a.end(2),
                        'texto': valor,
                        'attr': nome_a,
                    })

        # ---- limites de unidade ----
        if nome == ANCORA:
            # <a> que abre sem texto antes dele e link solto, e fica fora da
            # frase. <a> no meio de uma frase e inline e viaja junto com ela.
            # </a> encerra a unidade, o que impede dois links irmaos de virarem
            # uma chave so; quando ele fecha um <a> que abriu aqui dentro, a
            # unidade leva o </a> junto, para nao sair com tag pendurada.
            if fechando:
                if not tem_texto:
                    ini = m.end()
                elif continua_a_frase(html, m.end()):
                    # a frase segue depois do link: "li a <a>Politica</a> e o
                    # <a>Aviso</a>." e uma frase so, e tem que ser traduzida
                    # como uma frase so
                    if ancoras > 0:
                        ancoras -= 1
                else:
                    if ancoras > 0:
                        ancoras -= 1
                        fecha(m.end())
                    else:
                        fecha(m.start())
                    ini = m.end()
            elif not tem_texto:
                ini = m.end()
            else:
                ancoras += 1
            continue

        if nome in INLINE:
            continue

        fecha(m.start())
        ini = m.end()

    fecha(len(html))
    achados.sort(key=lambda u: u['ini'])
    return achados


def aplicar(html, dicionario, faltantes=None):
    """Reescreve o HTML trocando cada unidade pela traducao, por posicao.

    De tras para frente, para que uma troca nao desloque as coordenadas das
    seguintes. O que nao estiver no dicionario fica como esta e e registrado
    em `faltantes`, em vez de sumir em silencio.
    """
    us = unidades(html)
    for u in reversed(us):
        alvo = dicionario.get(u['texto'])
        if alvo is None:
            if faltantes is not None:
                faltantes.append(u)
            continue
        html = html[:u['ini']] + alvo + html[u['fim']:]
    return html


def textos_unicos(html):
    """Trechos distintos da pagina, na ordem em que aparecem."""
    vistos, saida = set(), []
    for u in unidades(html):
        if u['texto'] not in vistos:
            vistos.add(u['texto'])
            saida.append(u)
    return saida


def palavras(s):
    return len(re.sub(r'<[^>]*>', ' ', s).split())
