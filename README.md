# RefreshU

Site público e tela de entrada do portal. Concierge médico, economia e experiência de viagem no Brasil, para público americano.

Construído a partir de `RefreshU-Briefing-de-Design-PT-BR.pdf` (31 seções).

## Rodar

```bash
npx -y serve -l 8821 .
```

Site estático, sem build. Editar direto e recarregar.

## Decisões que valem saber

**O site é em inglês.** O público é americano. Todo CTA do briefing está em inglês (`Explore Treatments`, `Start My Evaluation`, `See If I'm a Candidate`, `Contact My Concierge`) e a navegação da seção 26 também. A tradução PT-BR do briefing serve para leitura interna, não para virar o site.

**Paleta tirada da logo**, não do PDF do briefing: navy `#12305a` da palavra "refresh" e o degradê ciano `#25c6e0` para turquesa `#12bfa2` do símbolo. O papel é um marfim quente `#fbf9f5` de propósito: branco puro somado a ciano dá cara de SaaS médico, e o briefing pede hospitalidade.

**Tipografia:** Newsreader para títulos (serifa editorial, puxa o lado viagem de alto padrão) e DM Sans para interface (geométrica, conversa com a construção da logo). Auto-hospedadas, 57 KB somadas.

**Sem travessão e sem tag acima de título**, verificado no arquivo inteiro.

**Sem médicos inventados.** As buscas de foto de médico voltaram só com imagem gerada por IA (consultório genérico, pele plástica). Colocar isso num site médico entrega justamente a cara de IA que o cliente não quer, e nomear médicos fictícios num site que pode ir ao ar é pior. A seção de médicos sustenta a credibilidade pela lista de credenciais da seção 13, sem retrato e sem nome. As páginas de listagem e de perfil entram quando houver médicos contratados.

**Sem foto de compras.** As buscas voltaram com vitrines de Celine, Mulberry, Tory Burch e Jo Malone, marcas de terceiros em rua europeia. Compras entrou como texto na legenda do mosaico.

## O que está travado esperando terceiros

| Item | Onde | Depende de |
|---|---|---|
| Números da economia | seção `#savings`, quatro células "Pending verification" | fonte defensável e aprovação jurídica (aviso da própria seção 6 do briefing) |
| Vetor oficial da logo | `assets/img/refreshu-mark.svg` | o símbolo foi recriado a partir do PNG; trocar pelo AI/EPS/SVG do cliente |
| Autenticação e assinatura | `assets/js/auth.js`, função `enviar()` | back end. Hoje o envio devolve a regra real do produto: o portal abre depois da análise médica |
| Médicos | seção `#physicians` | contratos autorizando uso de conteúdo do profissional e de pacientes (seção 13) |
| Fotografia própria | `assets/img/` | as 14 fotos são Unsplash, licença de uso comercial. Para marca premium, o ideal é ensaio próprio no hero e nos tratamentos |

Toda afirmação médica, jurídica, de privacidade, preço, pagamento, seguro e marketing continua pendente de aprovação profissional, como a capa do briefing determina.

## Medições

Lighthouse com `--throttling-method=devtools` (o modo `simulate` infla o LCP):

| Página | Perf | A11y | Práticas | SEO |
|---|---|---|---|---|
| `/` mobile | 98 | 100 | 100 | 100 |
| `/` desktop | 95 | 100 | 100 | 100 |
| `/signin.html` mobile | 97 | 100 | 100 | 63 |

O SEO 63 do Sign In é o `noindex`, proposital numa tela de login.

LCP 2,2 s no mobile, CLS 0, TBT 0 ms.

## Armadilhas já pagas

- **Especificidade no mosaico:** as regras `.mosaic > :nth-child(N)` do desktop vencem um reset com `*`. No celular o reset precisa ser `:nth-child(n)`, senão a grade do desktop atravessa.
- **Posicionamento automático em grade abre buraco:** o item largo que não cabe no resto da linha pula, deixando célula vazia. As duas grades do mosaico são explícitas.
- **Alfa de texto sobre fundo escuro:** `--on-deep-fine` está em `.58` porque é o mínimo que passa 4.5:1 nos dois fundos escuros do site. `--on-paper-fine` em `.66` pelo mesmo motivo do lado claro. Não baixar sem recalcular.
- **Captura de tela mente:** `scroll-behavior: smooth` deixa a página em movimento no print, e `loading="lazy"` faz seção abaixo da dobra sair vazia. Para conferir layout, forçar `loading="eager"` e desligar o scroll suave antes do screenshot.

## Próximo

Páginas que o briefing pede e ainda não existem: procedimento (Hair e Face + Neck), listagem e perfil de médico, destino São Paulo completo, o fluxo `Start My Evaluation` de seis etapas, e o portal do cliente com as dez áreas da seção 27.
