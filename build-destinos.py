#!/usr/bin/env python3
"""
Gera destination-sao-paulo.html e destination-rio.html.

As duas paginas tem a mesma estrutura e mudam so o conteudo, entao sao
GERADAS e nao escritas a mao: assim uma nao evolui sem a outra. Para mudar
texto, foto ou passeio, editar o dicionario DESTINOS abaixo e rodar:

    python3 build-destinos.py

O cabecalho e o rodape sao recortados do index.html na hora, para que uma
mudanca no menu ou no rodape apareca aqui sem ninguem lembrar de copiar.

A regra que organiza a pagina inteira: o publico chega para um procedimento
e passa dias sem poder fazer esforco. Por isso os passeios sao agrupados por
ESFORCO FISICO, e nao por tipo. E por isso cada bloco repete que quem libera
atividade e o medico, nunca a RefreshU nem o tempo decorrido.
"""
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))


def pedaco(html, ini, fim):
    a = html.index(ini)
    b = html.index(fim) + len(fim)
    return html[a:b]


# ---------------------------------------------------------------- conteudo
DESTINOS = {
    'sao-paulo': {
        'arquivo': 'destination-sao-paulo.html',
        'cidade': 'São Paulo',
        'titulo': 'São Paulo',
        'subtitulo': 'The medical capital, and a city built around the table',
        'meta': 'São Paulo for a RefreshU journey: where you stay, what you can do while you recover, and where to eat. Neighbourhoods, distances and effort, said plainly.',
        'foto': 'assets/img/saopaulo.webp',
        'foto_alt': 'Avenida Paulista seen from above',
        'abertura': 'The largest concentration of clinics, hospitals and specialists in Latin America, in a city that has no beach and stopped apologising for it a long time ago. People come to São Paulo to work, and stay for the food.',
        'porque': [
            ('Why people choose it', 'The medical infrastructure is the deepest in the country, and the neighbourhoods we place you in are walkable, residential and close to the clinics. If the procedure is the reason for the trip, this is the city that is organised around it.'),
            ('What it asks of you', 'It is a big, dense, vertical city. The reward is a week of restaurants, museums and shops within a short drive; the trade is that there is no coastline to look at while you rest.'),
        ],
        'bairros': [],       # preenchido pela pesquisa
        'hoteis': [],
        'passeios': {'leve': [], 'medio': [], 'liberado': []},
        'mesa': [],
        'compras': [],
        'clima': [],
    },
    'rio': {
        'arquivo': 'destination-rio.html',
        'cidade': 'Rio de Janeiro',
        'titulo': 'Rio de Janeiro',
        'subtitulo': 'The recovery that happens by the sea',
        'meta': 'Rio de Janeiro for a RefreshU journey: where you stay, what you can do while you recover, and where to eat. Neighbourhoods, distances and effort, said plainly.',
        'foto': 'assets/img/beach.webp',
        'foto_alt': 'The coastline of Rio de Janeiro',
        'abertura': 'The same standard of clinic and the same concierge, in a city where the short walk your physician clears you for happens along the water. Rio is the destination for the stay where the days between appointments are the point.',
        'porque': [
            ('Why people choose it', 'Recovery does not feel like recovery here. The neighbourhoods we use are flat, quiet and close together, and a walk you are cleared for ends at the sea rather than at a traffic light.'),
            ('What it asks of you', 'The famous sights involve heat, sun and, in some cases, real climbing. Several of them are worth planning for the end of the stay rather than the beginning.'),
        ],
        'bairros': [],
        'hoteis': [],
        'passeios': {'leve': [], 'medio': [], 'liberado': []},
        'mesa': [],
        'compras': [],
        'clima': [],
    },
}

ESFORCO = [
    ('leve', 'Gentle', 'Little walking, no heat, no exertion. The kind of outing most people are cleared for early.'),
    ('medio', 'Moderate', 'More time on your feet, some sun. Usually a question for the middle of the stay.'),
    ('liberado', 'Ask first', 'Heat, climbing, water or crowds. These wait for your physician to release them, and never for time alone to pass.'),
]


def lista(itens, chave_titulo='nome', chave_texto='texto'):
    if not itens:
        return ('<p class="dpend">This block is filled from the destination guide. '
                'The content is being written and is not published yet.</p>')
    out = []
    for it in itens:
        extra = f'<span class="dcard__m">{it["meta"]}</span>' if it.get('meta') else ''
        out.append(f'<article class="dcard"><h3>{it[chave_titulo]}</h3>{extra}'
                   f'<p>{it[chave_texto]}</p></article>')
    return '<div class="dgrid">' + ''.join(out) + '</div>'


def completa(d):
    """A pagina so vai ao ar quando tem conteudo. Enquanto os blocos estiverem
    vazios ela sai com noindex, para nao entrar no Google meio pronta."""
    cheios = [d['bairros'], d['hoteis'], d['mesa'], d['compras'], d['clima']]
    cheios += list(d['passeios'].values())
    return all(x for x in cheios)


def pagina(chave, d, cabeca, rodape):
    outro = 'rio' if chave == 'sao-paulo' else 'sao-paulo'
    outro_nome = DESTINOS[outro]['cidade']
    robots = '' if completa(d) else '\n<meta name="robots" content="noindex,follow">'

    blocos_esforco = []
    for k, rotulo, explica in ESFORCO:
        blocos_esforco.append(
            f'<div class="deff"><div class="deff__h"><h3>{rotulo}</h3>'
            f'<p>{explica}</p></div>{lista(d["passeios"][k])}</div>')

    porque = ''.join(f'<div class="dwhy__i"><b>{t}</b><p>{p}</p></div>' for t, p in d['porque'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d['titulo']} · RefreshU</title>
<meta name="description" content="{d['meta']}">{robots}
<link rel="icon" href="assets/img/refreshu-mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{cabeca}

<main id="main">

  <section class="dhero">
    <div class="dhero__foto"><img src="{d['foto']}" alt="{d['foto_alt']}" width="1600" height="900" fetchpriority="high" decoding="async"></div>
    <div class="dhero__veu"></div>
    <div class="wrap dhero__g">
      <p class="dhero__k">Destination</p>
      <h1 class="display">{d['titulo']}</h1>
      <p class="dhero__s">{d['subtitulo']}</p>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <p class="dlead reveal">{d['abertura']}</p>
      <div class="dwhy reveal">{porque}</div>
    </div>
  </section>

  <section class="sec sec--claro">
    <div class="wrap">
      <div class="sec-head reveal"><h2 class="display">Where you stay</h2>
        <p class="sec-lead">Walkable, residential and close to the clinics. We book the hotel; you pay the hotel directly.</p></div>
      {lista(d['bairros'])}
      {lista(d['hoteis'])}
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="sec-head reveal"><h2 class="display">What you can do, by effort</h2>
        <p class="sec-lead">Grouped by what it asks of your body, not by category, because that is the question that actually matters while you are recovering.</p></div>
      {''.join(blocos_esforco)}
      <p class="fine-note reveal" style="margin-top:34px">Every option here is a concierge suggestion and not a medical recommendation. Your physician decides what you are cleared for, and RefreshU never infers clearance from silence or from time having passed.</p>
    </div>
  </section>

  <section class="sec sec--claro">
    <div class="wrap">
      <div class="sec-head reveal"><h2 class="display">Where you eat</h2>
        <p class="sec-lead">Your concierge handles the reservation, including the ones that normally need weeks. Meals come to the room on the days you should be resting.</p></div>
      {lista(d['mesa'])}
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="sec-head reveal"><h2 class="display">Shopping, services and the weather</h2></div>
      {lista(d['compras'])}
      {lista(d['clima'])}
    </div>
  </section>

  <section class="eval">
    <div class="wrap">
      <div class="dnext reveal">
        <div>
          <h2 class="display">Book your call</h2>
          <p>Three steps, nothing clinical, and a time with your RefreshU concierge to talk through the trip.</p>
          <a class="btn btn--lg" href="assessment.html">Book your call</a>
        </div>
        <a class="dnext__o" href="destination-{outro}.html">
          <span>Considering the other city?</span>
          <b>{outro_nome}</b>
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </section>

</main>

{rodape}

<script src="assets/js/site.js" defer></script>
<script src="assets/js/foot.js" defer></script>
</body>
</html>
'''


def main():
    idx = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
    cabeca = pedaco(idx, '<header class="chrome"', '</header>')
    rodape = pedaco(idx, '<footer class="foot"', '</footer>')

    # A ancora #destination so existe na home: a partir daqui ela precisa
    # do caminho completo, senao o link nao sai do lugar.
    cabeca = cabeca.replace('href="#', 'href="index.html#')
    rodape = rodape.replace('href="#', 'href="index.html#')

    for chave, d in DESTINOS.items():
        alvo = os.path.join(RAIZ, d['arquivo'])
        open(alvo, 'w', encoding='utf-8').write(pagina(chave, d, cabeca, rodape))
        print(f"  {d['arquivo']} gerado")


if __name__ == '__main__':
    main()
