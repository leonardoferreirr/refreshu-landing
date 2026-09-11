# RefreshU

Site público, tela de entrada e portal demonstrativo do cliente. Concierge médico, economia e experiência de viagem no Brasil, para público americano.

Construído a partir de `RefreshU-Briefing-de-Design-PT-BR.pdf`, 31 seções.

## Rodar

```bash
npx -y serve -l 8821 .
```

Site estático, sem build. A única etapa gerada são os outros idiomas:

```bash
python3 i18n_traduzir.py
```

## Páginas

| Arquivo | O que é |
|---|---|
| `index.html` | home pública |
| `destination-sao-paulo.html`, `destination-rio.html` | guias de destino |
| `legal.html` | Centro Legal, quinze documentos |
| `assessment.html` | avaliação em três etapas e agendamento |
| `signin.html`, `recover.html` | entrada e recuperação de senha da cliente |
| `portal.html` | portal da cliente, demonstrativo, onze áreas |
| `signin-sales.html`, `sales.html` | aplicação comercial |
| `signin-team.html`, `console.html` | console de operação |
| `es/` | as doze acima em espanhol, **geradas**, nunca editar na mão |
| `pt/` | a home em pt-BR, **gerada**, nunca editar na mão |

## Idiomas

O inglês é a fonte da verdade. Mexeu no texto? Roda `i18n_traduzir.py` de novo.

| Script | Para quê |
|---|---|
| `i18n_core.py` | o motor: acha cada trecho traduzível **com a posição dele** no arquivo, e troca por posição, não por busca |
| `i18n_extrair.py` | lista de trabalho por página, em `i18n/unidades/` |
| `i18n_js.py` | o texto de tela que nasce dentro do JavaScript (rodapé legal, selos, catálogo) |
| `i18n_juntar.py` | junta um lote de traduções ao dicionário, sem sobrescrever o que já foi revisado |
| `i18n_traduzir.py` | gera `/es/` e `/pt/`, mais `assets/js/i18n.<idioma>.js` |

O build **cobra o que ficou sem traduzir**, por página e no JavaScript, e escreve a lista em `i18n/pendente-<idioma>.json`. Era o que faltava no script antigo: ele só sabia reclamar de chave do dicionário que sobrou, nunca de texto da página que nunca entrou nele. Foi assim que a seção de pacotes ficou em inglês dentro do `/pt/` sem ninguém perceber.

**Matriz de idiomas.** A Plataforma (portal, vendas, console e os logins) sai em inglês e espanhol. O site público pode ter português também. Veio da Agata em 10/09/2026 e substitui a linha "Idioma: apenas inglês" do Anexo A. Estender o português para todo o site público é trocar uma linha em `IDIOMAS`, dentro de `i18n_traduzir.py`.

**Página que não existe num idioma aponta para a raiz em inglês**, em vez de 404 dentro da própria pasta. O seletor de idioma só oferece o idioma em que aquela página existe.

**O seletor é texto, não bandeira.** Bandeira nomeia país e idioma não é país: quem lê espanhol aqui mora nos Estados Unidos, e a bandeira da Espanha diria a coisa errada para uma cliente mexicana ou colombiana.

## Decisões que valem saber

**O site nasce em inglês, com português no botão.** O público é americano e todo CTA do briefing já está em inglês. As bandeiras ao lado do CTA levam para `/pt/`, que existe para o cliente, parceiros e imprensa no Brasil.

**Paleta tirada da logo**, não do PDF do briefing: navy `#12305a` da palavra "refresh" e o degradê ciano `#25c6e0` para turquesa `#12bfa2` do símbolo. O papel é um marfim quente `#fbf9f5` de propósito: branco puro somado a ciano dá cara de SaaS médico, e o briefing pede hospitalidade.

**Tipografia:** Newsreader nos títulos, DM Sans na interface. Auto-hospedadas, 57 KB somadas.

**Sem travessão e sem tag acima de título**, verificado nos arquivos inteiros.

**Sem médicos inventados na home.** As buscas de foto de médico voltaram só com imagem gerada por IA. A seção de médicos sustenta a credibilidade pela lista de credenciais da seção 13, sem retrato e sem nome.

**O portal é demonstração declarada.** Uma faixa fixa no topo diz, em toda tela, que nome, data, clínica, hotel e documento são exemplo. Hotel Aurora, Clínica Vértice, Dra. Camila Rocha, Beatriz L. e Michael Carter são fictícios, escolhidos assim de propósito para não sugerir parceria que não existe. Trocar tudo antes de qualquer uso real.

**Um CTA só, e ele leva ao login.** "Explore Treatments" e o link "Sign In" saíram do topo. Sobrou "Start My Evaluation", no gradiente ciano da marca, apontando para `signin.html` em todos os pontos da home: topo, hero, seção de médicos, seção de avaliação e rodapé. Consequências que vieram junto:

- O CTA entrou no menu do celular, onde o botão do topo é escondido. O gradiente ciano destaca sobre o navy do painel, então ele mantém a cor do resto do site.
- O rodapé mantém "Sign In", que é a porta de quem já é cliente. É o único lugar do site onde ela aparece agora.

**A página de login é só o formulário.** Título, subtítulo, e-mail, senha, lembrar e o botão. Saíram, a pedido: o aviso de demonstração, a mensagem "Opening your journey." depois do envio, o separador "New to RefreshU" com o botão que devolvia para a home, a frase sobre o portal abrir depois da análise médica e o texto de acesso e privacidade. O `authMsg` saiu do HTML e do `auth.js` junto.

Duas coisas a recolocar antes do lançamento, porque saíram da única tela onde apareciam:

- O texto de privacidade ("suas informações são usadas para coordenar a jornada e compartilhadas com o médico que analisa o caso") é conteúdo do briefing e precisa de um lugar, seja no rodapé, seja na política de privacidade.
- Sem o aviso de demonstração, quem abre o login não tem como saber que qualquer e-mail e senha entram. Enquanto não houver autenticação de verdade, quem for mostrar a demo precisa dizer isso por fora.

## Auditoria contra o briefing

Passei as 31 seções contra o que está no ar. Estado por seção:

**No ar e fiel:** 1, 2, 3, 4, 5, 7, 8, 11, 13 (campos), 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29.

**No ar com ressalva:**

- **Seção 6, economia.** A estrutura está pronta com o seletor de procedimento e as quatro linhas. Os valores aparecem como "A confirmar" porque o próprio briefing exige fonte defensável e aprovação jurídica antes de publicar.
- **Seção 26, navegação.** O briefing lista nove itens no menu. Coloquei seis no cabeçalho e levei "Sobre" e "FAQ" para o rodapé: nove itens num cabeçalho premium viram sopa de links. Se o cliente quiser os nove, é reverter em um minuto.
- **Seção 13, perfis.** Os campos estão listados na home. As páginas de listagem e de perfil entram quando houver médico contratado.

**Fora do escopo desta rodada, previstas no briefing:**

- Seção 9 e 12: páginas de destino e de procedimento (hoje são seções da home)
- Seção 10: montador de roteiro, que o próprio briefing coloca no futuro
- Seção 14: o fluxo de seis etapas da avaliação
- Seção 25: a tela "Today in Brazil" existe no painel, falta a versão de app
- Seção 30, fase 2 inteira

**Correções que a auditoria gerou:** os três pilares ganharam os nomes da seção 5 (cuidado, valor e viagem) sem perder o trio da marca; entrou a frase de fechamento do quadro de economia; entrou a hospitalidade brasileira na lista do Brasil; e entrou a seção 28 inteira, "Três produtos, uma experiência", que estava diluída no site.

## O que está travado esperando terceiros

| Item | Onde | Depende de |
|---|---|---|
| Números da economia | `#savings` | fonte defensável e aprovação jurídica |
| Vetor oficial da logo | `assets/img/refreshu-mark.svg` | símbolo recriado a partir do PNG, trocar pelo arquivo do cliente |
| Autenticação e assinatura | `assets/js/auth.js`, função `enviar()` | back end. Hoje qualquer e-mail válido abre o portal demonstrativo |
| Pagamento seguro | tela Pagamentos do portal | mostra itens e situação, sem valores, até o preço ser aprovado |
| Médicos | `#physicians` | contratos autorizando uso de conteúdo do profissional e de pacientes |
| Fotografia própria | `assets/img/` | as 14 fotos são Unsplash, licença comercial. Para marca premium, o ideal é ensaio próprio |
| Domínio | `hreflang` | as tags `<link rel="alternate">` precisam de URL absoluta, entram no lançamento |

## Medições

Lighthouse com `--throttling-method=devtools`, porque `simulate` infla o LCP:

| Página | Perf | A11y | Práticas | SEO |
|---|---|---|---|---|
| `/` mobile | 98 | 100 | 100 | 100 |
| `/pt/` mobile | 98 | 100 | 100 | 100 |
| `/signin.html` mobile | 97 | 100 | 100 | 63 |
| `/portal.html` mobile | 97 | 100 | 100 | 54 |

SEO baixo em `signin` e `portal` é o `noindex`, proposital. LCP 2,2 s, CLS 0, TBT 0 ms.

Depois do espanhol, medido em desktop, para conferir que o dicionário do JavaScript não cobrou nada:

| Página | Perf | A11y | Práticas | SEO |
|---|---|---|---|---|
| `/` desktop | 100 | 100 | 100 | 100 |
| `/es/` desktop | 100 | 100 | 100 | 100 |

A página em espanhol carrega 9,5 KB a mais, que é o dicionário `i18n.es.js`, e isso não apareceu na nota. Uma coisa apareceu: trocar bandeira por texto no seletor criou divergência entre o rótulo visível (`PT`) e o nome acessível (`Português`), o que quebra o critério 2.5.3 da WCAG para quem usa controle por voz. O nome acessível agora começa pelo texto visível: `PT, Português`.

## Armadilhas já pagas

- **Medir `/pt/index.html` dá 87, medir `/pt/` dá 98.** O `serve` faz 301 de `/pt/index.html` para `/pt/index`, e o redirecionamento sozinho custa um segundo de FCP. Medir sempre na URL que responde 200.
- **Especificidade no mosaico:** as regras `.mosaic > :nth-child(N)` do desktop vencem um reset com `*`. No celular o reset precisa ser `:nth-child(n)`.
- **Posicionamento automático em grade abre buraco:** o item largo que não cabe no resto da linha pula. As duas grades do mosaico são explícitas.
- **`opacity` derruba contraste:** o item já cumprido do "Hoje no Brasil" usava `opacity: .5` e caiu para 2,2:1. Item apagado se faz com cor própria, não com opacidade.
- **Alfa de texto:** `--on-deep-fine` em `.58` e `--on-paper-fine` em `.66` são os mínimos que passam 4.5:1 no pior fundo de cada lado. Não baixar sem recalcular.
- **Título de tela do portal não pode viver no JavaScript.** Estava numa tabela fixa e a versão pt-BR continuava em inglês. Agora sai do rótulo do próprio menu, então a tradução do HTML resolve.
- **Captura de tela mente:** `scroll-behavior: smooth` deixa a página em movimento no print e `loading="lazy"` esvazia seção abaixo da dobra. Forçar `loading="eager"` e desligar o scroll suave antes do screenshot.
- **O painel do menu do celular precisa de altura cheia.** Sem `min-height: 100dvh` ele para onde o conteúdo acaba, o CTA do hero vaza por baixo e aparecem dois "Start My Evaluation" empilhados.
- **`.nav a` vence `.nav__cta`.** Um botão dentro do menu precisa de `.nav a.nav__cta` para sobrescrever cor, padding e a borda de baixo dos links.
- **O login cabe em 660px de altura.** Hoje sobra folga, mas já estourou por 57px quando ganhou um bloco de aviso. Medir `scrollHeight - innerHeight` a 660px antes de acrescentar qualquer coisa ali.
- **Tirar conteúdo do HTML pede rodar o `traduzir.py` na sequência.** Ele lista as chaves que deixaram de casar, e essa lista é a única forma de achar tradução órfã. Foram 4 nesta rodada.

## Próximo

Páginas que o briefing pede e ainda não existem: procedimento (Hair e Face + Neck), listagem e perfil de médico, destino São Paulo completo, o fluxo `Start My Evaluation` de seis etapas, e a versão de app da tela "Today in Brazil".
