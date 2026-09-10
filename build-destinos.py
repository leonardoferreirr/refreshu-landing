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
        'bairros': [{'nome': 'Jardins',
  'meta': 'Where most guests stay',
  'texto': 'The city&rsquo;s classic high-end address, and the most walkable neighbourhood on this '
           'list. Rua Oscar Freire was rebuilt with five-metre pavements at the corners, 40 '
           'accessibility ramps and buried cabling, which matters when you are walking slowly. '
           'Sírio-Libanês and Oswaldo Cruz are minutes away by car.'},
 {'nome': 'Itaim Bibi',
  'meta': 'Closest to the clinics',
  'texto': 'The corporate quarter, and the neighbourhood with the shortest distance between bed '
           'and clinic: Sírio-Libanês has a unit on Rua Joaquim Floriano with its own surgical '
           'centre, on the same street as the hair clinics. Consultation, procedure and follow-up '
           'happen within a five-minute drive. The trade is noise near Jerônimo da Veiga at '
           'night.'},
 {'nome': 'Vila Nova Conceição',
  'meta': 'The quiet one',
  'texto': 'Almost entirely residential, wrapped around Ibirapuera park, and the most expensive '
           'square metre in São Paulo. Einstein Ibirapuera is effectively on the corner. Hotels '
           'here are scarce, so in practice we place you on its edge, towards Jardim Paulista.'},
 {'nome': 'Bela Vista and Paraíso',
  'meta': 'The hospital quarter',
  'texto': 'Not the prettiest address, but the one with the shortest distance to a reference '
           'emergency room: Sírio-Libanês, Oswaldo Cruz, Nove de Julho and Santa Catarina sit '
           'within a short radius, beside Avenida Paulista.'}],       # preenchido pela pesquisa
        'hoteis': [{'nome': 'Rosewood São Paulo',
  'meta': 'Bela Vista',
  'texto': 'Preserved early-1900s buildings plus Jean Nouvel&rsquo;s vertical-garden tower, with '
           'three hectares of Atlantic forest inside the grounds and Avenida Paulista 200 metres '
           'away. You can spend five days here without leaving, with a short shaded walk of your '
           'own, in the neighbourhood where the reference hospitals are.'},
 {'nome': 'Palácio Tangará',
  'meta': 'Panamby, inside Burle Marx park',
  'texto': 'The quietest private green space available in a São Paulo hotel, and Tangará '
           'Jean-Georges holds a Michelin star downstairs: a starred dinner reached by lift, with '
           'no traffic and no exposure.'},
 {'nome': 'Hotel Fasano',
  'meta': 'Jardins',
  'texto': 'A 1930s modernist building in exposed brick, about 250 metres from Rua Oscar Freire. '
           'Short walks and the luxury shopping street on the same block.'},
 {'nome': 'Fasano Itaim',
  'meta': 'Itaim Bibi',
  'texto': 'Residential-format apartments from 30 to 190 m², which changes an eight to fourteen '
           'day stay, in the same neighbourhood as the Itaim hospital unit and the clinics.'}],
        'passeios': {'leve': [{'nome': 'Farol Santander, 26th-floor lookout',
           'meta': 'Centro · 45 min',
           'texto': 'The best view in the city for the least effort. Ten lifts, a single floor at '
                    'the top, a closed café beside it to sit down. Timed tickets every 30 minutes, '
                    'so no queue in the sun.'},
          {'nome': 'MASP',
           'meta': 'Avenida Paulista · 1h',
           'texto': 'Two buildings joined by a 40-metre underground tunnel, lifts throughout, '
                    'wheelchairs lent at the door, fully climate controlled. Book a time online. '
                    'Avoid Tuesdays, when entry is free and it fills up.'},
          {'nome': 'Japan House',
           'meta': 'Avenida Paulista · 45 min',
           'texto': 'Small, free, indoors, 40 to 60 minutes, on the flat stretch of Paulista. The '
                    'lowest-commitment outing on the list.'},
          {'nome': 'Sala São Paulo',
           'meta': 'Campos Elíseos · 1–2h',
           'texto': 'The seated option: an Osesp concert, or a guided visit of about an hour. '
                    'Ramps, panoramic lifts and a lift platform. Arrive by car through the hotel '
                    'entrance on Rua Mauá.'},
          {'nome': 'Instituto Moreira Salles',
           'meta': 'Avenida Paulista · 1h',
           'texto': 'Photography and visual arts, free, lifts to every exhibition floor. Metro '
                    'works on the block mean the driver should agree the drop-off point in '
                    'advance.'}],
 'medio': [{'nome': 'Ibirapuera, the Niemeyer canopy',
            'meta': 'Vila Mariana · 500–800 m',
            'texto': 'The intelligent cut is the covered walkway linking MAM, Oca and the Bienal: '
                     'continuous shade, flat, and a fraction of the three-kilometre lake loop. '
                     'Enter by gate 3 before 9am or after 4pm.'},
           {'nome': 'Pinacoteca',
            'meta': 'Luz · 1.5h',
            'texto': 'Inside it is easy: three buildings on an accessible route, free wheelchairs, '
                     'one ticket covers all three the same day. What raises the effort is the '
                     'surroundings, so arrive and leave by car at the door, without exception.'},
           {'nome': 'Museu do Ipiranga',
            'meta': 'Ipiranga · 2–3h',
            'texto': 'Fully restored, with three lifts, escalators and a lift platform to the '
                     'viewpoint. Two things to know: the entrance is reached across a French '
                     'garden with no shade at all, and the full visit is two to three hours on '
                     'your feet.'},
           {'nome': 'Jardim Botânico',
            'meta': 'Água Funda · 1h',
            'texto': 'An accessible trail and a 360-metre raised walkway with rest points. Some '
                     'historic glasshouses are not accessible.'},
           {'nome': 'Mercado Municipal',
            'meta': 'Centro · 1h',
            'texto': 'Covered but not air conditioned: the stained glass makes it warm and close. '
                     'Tuesday to Thursday between 10 and 11. Saturday morning belongs in the next '
                     'group.'}],
 'liberado': [{'nome': 'Mercadão on a Saturday morning',
               'meta': 'Heat and crowd',
               'texto': 'The same building, a different experience: shoulder to shoulder, warm, '
                        'and slow to get out of.'},
              {'nome': 'Beco do Batman on foot',
               'meta': 'Twenty minutes uphill',
               'texto': 'The alley is short. Vila Madalena around it is a hill, on uneven paving, '
                        'twenty minutes up from the metro. Go by car, before 9am, and it drops a '
                        'category.'}]},
        'mesa': [{'nome': 'Evvai',
  'meta': 'Pinheiros · three Michelin stars',
  'texto': 'One of the first two three-star restaurants in Latin America, awarded in April 2026. '
           'Contemporary Italian, tasting menu around R$ 1,150. Weeks of notice, which your '
           'concierge handles.'},
 {'nome': 'Tuju',
  'meta': 'Jardim Paulistano · three Michelin stars',
  'texto': 'The other one. Ten courses through Brazilian biomes, around R$ 1,500, in a restored '
           'house with a five-metre glass cellar. Reservation only, booked well ahead.'},
 {'nome': 'D.O.M.',
  'meta': 'Jardins · two Michelin stars',
  'texto': 'Alex Atala&rsquo;s single tasting menu, with a vegetarian version. The restaurant that '
           'put Brazilian cooking on the international map.'},
 {'nome': 'A Figueira Rubaiyat',
  'meta': 'Jardins · walk in',
  'texto': 'A dining room built around a century-old fig tree, beef from the restaurant&rsquo;s '
           'own farm. The format an American reads without translation, and no reservation drama.'},
 {'nome': 'Tordesilhas',
  'meta': 'Jardins · walk in',
  'texto': 'Thirty years of regional Brazilian cooking, a Michelin Bib Gourmand, feijoada on '
           'Saturdays. Where you eat the real thing without a ten-course commitment.'},
 {'nome': 'A Casa do Porco',
  'meta': 'Centro · plan far ahead',
  'texto': '25th in Latin America&rsquo;s 50 Best and the restaurant you will hear about. Honest '
           'warning: booking runs up to 120 days out for weekends, the queue stands outside, and '
           'it is downtown. Not a first-week outing.'}],
        'compras': [{'nome': 'Rua Oscar Freire',
  'meta': 'Jardins',
  'texto': 'Over 300 shops along 2.6 kilometres, and the best pavement in the city since the '
           'rebuild, which is the part that matters when you are walking slowly.'},
 {'nome': 'Iguatemi São Paulo',
  'meta': 'Faria Lima',
  'texto': 'The services are the point: personal shopper by appointment, a concierge desk that '
           'books restaurants and wraps gifts, daily valet.'},
 {'nome': 'Shopping Cidade Jardim',
  'meta': 'Morumbi',
  'texto': 'Open air, in the manner of Miami and Los Angeles. The architecture helps if cold air '
           'conditioning is not for you.'},
 {'nome': 'Lymphatic drainage',
  'meta': 'At the hotel or in a spa',
  'texto': 'The most requested service after a facial procedure. Arranged as part of your '
           'itinerary rather than as an extra to hunt for.'}],
        'clima': [{'nome': 'June to August',
  'meta': 'The best window',
  'texto': 'Cool and dry, lows between 12 and 19°C, August the driest month of the year. No heat, '
           'no sweat, weak sun, and the city&rsquo;s indoor cultural programme at its most '
           'comfortable.'},
 {'nome': 'April, May, September to November',
  'meta': 'Workable',
  'texto': 'Mild shoulder seasons. Watch the midday sun towards November.'},
 {'nome': 'December to March',
  'meta': 'The one to avoid',
  'texto': 'Hot and wet, February the warmest, January the wettest, and a UV index that reaches '
           '11, the extreme band. Sweat is what dislodges grafts in the first week, and direct sun '
           'on a healing scalp is off the table for about 30 days. São Paulo&rsquo;s advantage is '
           'that the afternoon rain pushes you indoors, and the indoor programme is deep.'}],
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
        'bairros': [{'nome': 'Copacabana',
  'meta': 'The strongest medical case',
  'texto': 'Rua Figueiredo de Magalhães starts at the beachfront and holds two reference private '
           'hospitals within a few blocks, Copa Star and Copa D&rsquo;Or. You leave a hotel facing '
           'the sea and reach the hospital on flat ground without leaving the neighbourhood. '
           'Busier and more touristic than Ipanema, with the widest choice of hotels.'},
 {'nome': 'Ipanema',
  'meta': 'The balanced one',
  'texto': 'A small grid, two metro stations, the densest run of restaurants in the Zona Sul, and '
           'Brazil&rsquo;s fine jewellery street. Almost everything is solved within two or three '
           'flat blocks. Ipanema and Leblon recorded no homicides in the first quarter of 2026, '
           'and 61 municipal guards have patrolled both around the clock since May.'},
 {'nome': 'Leblon',
  'meta': 'The quiet one',
  'texto': 'The most expensive and calmest address in the Zona Sul, with Dias Ferreira as its '
           'restaurant spine. It empties after dinner, which is usually the criticism and is '
           'exactly the point when you are recovering. Three of Rio&rsquo;s eight Michelin stars '
           'are here.'},
 {'nome': 'Jardim Botânico',
  'meta': 'The green one',
  'texto': 'Leafy, noticeably cooler because forest surrounds it, with Parque Lage, the botanical '
           'garden and the lagoon around it. Hotels are scarce, so it works better as a daily '
           'destination than as a base.'}],
        'hoteis': [{'nome': 'Copacabana Palace',
  'meta': 'Copacabana',
  'texto': 'The most recognisable hotel in Brazil, a century old, facing the beach, with MEE and '
           'its Michelin star inside. One thing to check before you fix dates: the 1948 annexe is '
           'under renovation into a new tower, due to finish in the second half of 2026. The main '
           'building and the restaurants stay open throughout.'},
 {'nome': 'Hotel Fasano Rio',
  'meta': 'Ipanema, Avenida Vieira Souto',
  'texto': 'Philippe Starck, facing Ipanema beach, rooftop pool and bar. The most discreet of the '
           'large hotels, on the most orderly stretch of the seafront.'},
 {'nome': 'Emiliano Rio',
  'meta': 'Copacabana',
  'texto': 'Between Copacabana and Ipanema, rooftop pool, 24-hour gym. The most efficient '
           'combination in Rio for this stay: high service, a few flat blocks from the hospitals.'},
 {'nome': 'Fairmont Rio',
  'meta': 'Arpoador',
  'texto': 'A flag an American recognises without research, and the Willow Stream spa inside '
           'handles lymphatic drainage without you leaving the building.'}],
        'passeios': {'leve': [{'nome': 'Guanabara Bay by catamaran',
           'meta': 'Marina da Glória · 2h, seated',
           'texto': 'Probably the best outing for the first days: seated the whole time, main deck '
                    'enclosed and air conditioned, upper deck optional. Passes Ilha Fiscal, the '
                    'Museum of Tomorrow, Sugarloaf and Christ seen from the water. We book the '
                    'enclosed catamaran, never an open boat, because of spray and direct sun.'},
          {'nome': 'Museum of Tomorrow',
           'meta': 'Praça Mauá · 1–1.5h',
           'texto': 'Calatrava&rsquo;s building, cooled by sea water, fully accessible, timed '
                    'tickets. It runs cold inside, so bring a light layer, and arrive by car: the '
                    'promenade around it is 3.5 kilometres without shade.'},
          {'nome': 'Museu de Arte do Rio',
           'meta': 'Praça Mauá · 1h',
           'texto': 'Under 200 metres from the Museum of Tomorrow, all flat, two buildings joined '
                    'internally. Combines into the same trip with no extra travel.'},
          {'nome': 'Sugarloaf cable car',
           'meta': 'Urca · 2h',
           'texto': 'Two enclosed glass cabins in sequence, with eight lift platforms across the '
                    'three stations. Fast Access exists and is worth it here: queues can run past '
                    'two hours. The Morro da Urca trail is a different thing entirely and belongs '
                    'in the last group.'},
          {'nome': 'H.Stern workshop tour',
           'meta': 'Ipanema · 15 min',
           'texto': 'Free, guided in more than 19 languages, indoors and air conditioned, showing '
                    'cutting and setting. Premium, short, and it asks nothing of your body. Book '
                    'ahead.'},
          {'nome': 'Vista Chinesa by car',
           'meta': 'Tijuca forest · 1h',
           'texto': 'Fifteen minutes uphill by car from the botanical garden, parking at the top, '
                    'a short walk to the viewpoint, through closed shaded forest. On foot it is '
                    '4.5 kilometres of climbing, which is another category.'}],
 'medio': [{'nome': 'Rio Botanical Garden',
            'meta': 'Jardim Botânico · 1h',
            'texto': 'The best natural shade among Rio&rsquo;s outdoor options: wide flat paths, '
                     'no stairs on the main routes. The short version, the imperial palm avenue '
                     'and the lake, takes 40 to 60 minutes.'},
           {'nome': 'Lagoa Rodrigo de Freitas',
            'meta': 'Lagoa · 40 min',
            'texto': 'Flat asphalt, no stairs. Our advice is not to do the loop: pick a kiosk, go '
                     'late afternoon, and walk no more than 500 metres. Much of the path has '
                     'little shade.'},
           {'nome': 'Santa Teresa by car',
            'meta': 'Santa Teresa · 2h',
            'texto': 'Drive straight to a restaurant or to the Chácara do Céu museum, stay seated, '
                     'skip the tram, and the whole afternoon drops a category.'}],
 'liberado': [{'nome': 'Christ the Redeemer',
               'meta': 'Read this before you plan it',
               'texto': 'The escalators were switched off in August 2026 for replacement and '
                        'return around May 2027. The lifts still run, but about 80 stone steps '
                        'between the second level and the platform are unavoidable on foot. '
                        'Climbing chairs and stair-climbing carriers are available at the visitor '
                        'centre, though they do not operate in rain or on wet ground. The platform '
                        'itself has no shade at all: sun, wind and uneven stone. If it goes in the '
                        'plan, put it at the end of the stay, first slot of the morning, and book '
                        'far ahead — capacity has been cut in half.'},
              {'nome': 'Santa Teresa tram',
               'meta': 'Queue, open sides, no air conditioning',
               'texto': 'Tickets sold only at the Carioca booth, with reports of one to two hours '
                        'standing, on an open tram, into a neighbourhood of steep cobbles and '
                        'rails underfoot.'},
              {'nome': 'Selarón steps, climbing them',
               'meta': '215 steps',
               'texto': 'The photograph everyone wants is taken from the bottom, in ten minutes, '
                        'standing still. Climbing all 215 is a different proposition, and '
                        'roadworks around the steps run into late 2026.'},
              {'nome': 'Morro da Urca on foot',
               'meta': 'Steep, 30–40 min',
               'texto': 'Just over a kilometre of continuous climb on steps cut into earth, '
                        'slippery after rain.'}]},
        'mesa': [{'nome': 'Lasai',
  'meta': 'Botafogo · two Michelin stars',
  'texto': 'Farm to table by Rafa Costa e Silva, tasting menu around R$ 1,380. Weeks of notice.'},
 {'nome': 'Oro',
  'meta': 'Leblon · two Michelin stars',
  'texto': 'Felipe Bronze&rsquo;s Brazilian vanguard, two menus around R$ 980 and R$ 1,100.'},
 {'nome': 'MEE',
  'meta': 'Copacabana · one Michelin star',
  'texto': 'Omakase inside the Copacabana Palace, around R$ 950. If you are staying there, it is a '
           'starred dinner without stepping outside.'},
 {'nome': 'Madame Olympe',
  'meta': 'Leblon · one Michelin star',
  'texto': 'Claude Troisgros, starred in 2026 and the most reachable of Rio&rsquo;s stars at R$ '
           '440 to R$ 540.'},
 {'nome': 'Talho Capixaba',
  'meta': 'Leblon · walk in',
  'texto': 'Delicatessen and sourdough bakery, open every day from 7am to 10pm. Breakfast and '
           'lunch with no production at all, for the day you would rather not be seen.'},
 {'nome': 'Pici, Koral and Didier',
  'meta': 'Ipanema · walk in',
  'texto': 'Three Bib Gourmand addresses within a few blocks of each other: Italian, contemporary '
           'and a classic French bistro. Simple booking, or none.'}],
        'compras': [{'nome': 'Rua Garcia D&rsquo;Ávila',
  'meta': 'Ipanema',
  'texto': 'Brazil&rsquo;s fine jewellery street, with H.Stern, Amsterdam Sauer and Antonio '
           'Bernardo. The highest-value, lowest-effort shopping in the city: all indoors, all '
           'within two blocks.'},
 {'nome': 'Shopping Leblon and Rio Design',
  'meta': 'Leblon',
  'texto': 'On opposite corners, the most complete pair in the Zona Sul, with cinema and art '
           'installations.'},
 {'nome': 'Lymphatic drainage',
  'meta': 'Hotel spa or in the room',
  'texto': 'Available in hotel spas, the Fairmont&rsquo;s among them, and arranged as part of your '
           'itinerary.'},
 {'nome': 'On the street',
  'meta': 'Copacabana and Ipanema',
  'texto': 'The Segurança Presente programme patrols the seafront on foot, bicycle and motorcycle, '
           'and 61 municipal guards have covered both neighbourhoods around the clock since May '
           '2026. Private door-to-door transport is still what we recommend at night.'}],
        'clima': [{'nome': 'March to June',
  'meta': 'The best window',
  'texto': '20 to 28°C with falling humidity. Warm enough to walk without sweating, which is the '
           'whole question in the first two weeks.'},
 {'nome': 'July and August',
  'meta': 'Second best',
  'texto': 'Sunny and dry, 18 to 25°C, rarely genuinely cold. Strong sun, manageable heat.'},
 {'nome': 'December to March',
  'meta': 'The one to avoid, by a wide margin',
  'texto': 'The hottest and most humid, with peaks reaching 40°C and a UV index recorded at 13 to '
           '14, where 11 already counts as extreme risk. A healing scalp needs about 30 days out '
           'of direct sun, and caps are not allowed early on. In a Rio summer that means no hat, '
           'no beach and no shade on most outdoor plans. We would rather tell you than sell you '
           'the wrong month.'}],
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
