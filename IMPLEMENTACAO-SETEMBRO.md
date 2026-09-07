# RefreshU · o que foi implementado dos documentos da Agata

Documento de retomada. Escrito em 7 de setembro de 2026, depois de aplicar os
doze documentos que a Agata mandou (guias de compliance, pacotes, itinerário,
perfil da médica, páginas legais, termos, roadmap de certificações, guias de São
Paulo e Rio, formulário de itinerário, planilha de fornecedores e o print com os
requisitos de avaliações).

---

## 1. O conflito que você precisa resolver antes de qualquer outra coisa

Três documentos assumem uma plataforma que **o contrato assinado proíbe**.

Cláusula 12.6, texto literal do contrato:

> A Plataforma não coleta, recebe, armazena, transmite, trata ou exibe o
> questionário de triagem médica ou suas respostas, fotografias clínicas,
> resultados laboratoriais ou diagnósticos, nem anotações clínicas de médicos.

O que chegou:

| Documento | O que pede | Conflito |
|---|---|---|
| Developer Legal & Compliance Guide, item 1 e item 13 | *"RefreshU may host/retain medical intake, photos and documents for physician review"* e um **Secure Medical Intake** | Direto com a 12.6 |
| Terms of Use, cláusula 5 | *"The Platform may allow you to submit questionnaires, photographs, or documents"* | Direto com a 12.6 |
| Physician Instructions Guide, item 3, e tracker item 15 | Um **Provider Portal** com login do médico, MFA e acesso a pacientes atribuídos | Cláusula 12.8: *"Qualquer integração futura entre a Plataforma e um Sistema de Triagem do Médico está fora do Preço e exige Ordem de Alteração"* |

**O que eu fiz.** Implementei tudo o que a 12.7 permite e nada do que a 12.6
proíbe. A 12.7 autoriza expressamente a Plataforma a *"receber de volta, da
CONTRATANTE ou do médico, o resultado da análise e qualquer instrução
operacional liberada pelo médico"*. É exatamente esse o caminho que está no
código:

- O sistema completo de instruções existe: objeto, categorias, versionamento,
  rascunho e liberação, prioridade, prazo, confirmação de leitura por versão,
  histórico imutável, efeito no roteiro, matriz de permissões e trilha de
  auditoria.
- Quem registra a liberação é a operação, na tela **Physician instructions** do
  console, e não um médico logado na plataforma. É o que a 12.7(c) prevê.
- A arquitetura já está pronta para o Provider Portal. Ligar o login do médico
  vira uma camada de autenticação a mais, não uma reescrita.

**O que falta decidir.** Se a Agata quer mesmo o Provider Portal e o intake
clínico hospedado, isso é Ordem de Alteração com preço fechado por escrito antes
de começar, pela Cláusula 6.3. E muda a classificação regulatória de vocês: no
dia em que a plataforma hospeda foto clínica, entra HIPAA, entra BAA, entra
análise formal de risco de segurança, e a arquitetura inteira muda. O
Compliance Guide dela reconhece isso no item 24, ao listar a classificação HIPAA
como decisão de advogado.

Marquei esse ponto em gold dentro dos próprios Termos e da Política de
Privacidade publicados, para que o advogado veja o conflito ao revisar.

---

## 2. O que ficou pronto

### Legal Center · `legal.html`
Quinze documentos, cada um com versão, data de vigência e data de atualização
próprias: Termos de Uso, Privacidade, Aviso Médico, Divulgação de Profissional
Independente, Contrato de Concierge, Cancelamento e Reembolso, Termos de Viagem,
Seguro Viagem, Pagamentos e Taxas, Comunicações Eletrônicas, Consentimento de
Marketing, Cookies e Escolhas de Privacidade, Acessibilidade, Contato e
Reclamações, e Aviso de Emergência.

- Cancelamento é mostrado **por marco e por quem recebe**, não como uma frase
  vaga. A estrutura está fechada; os valores e prazos ficam com o advogado.
- Cláusulas que dependem de advogado aparecem marcadas em dourado, em vez de
  escritas como se estivessem resolvidas.
- Formulário **Report a Concern** com número de caso, e o texto que o print da
  Agata exige: a RefreshU não penaliza avaliação negativa honesta, não exige
  transferência de propriedade da avaliação e não usa foto clínica em fluxo de
  depoimento.
- Rodapé legal em todas as telas, com o aviso de emergência e os telefones reais
  (192 e 911).

### Consent Center · `signup.html` e `assessment.html`
- Os sete consentimentos obrigatórios separados, mais o de marketing opcional,
  nenhum pré-marcado, o de marketing visualmente e estruturalmente apartado.
- Cada aceite grava documento, versão e carimbo de tempo. Isso responde à
  pergunta que o Compliance Guide manda o advogado fazer: *"Can we prove exactly
  which legal-document version a user accepted and when?"*
- Captura de **localização física** no momento do encaminhamento, país e estado,
  porque o endereço residencial não responde à pergunta que as regras estaduais
  fazem. Geolocalização por rede não é usada.
- O mapa de restrições estaduais existe e **sai vazio de propósito**: quem decide
  o que um médico brasileiro pode revisar com o paciente fisicamente nos EUA é o
  advogado, não o código.
- Reconhecimento afirmativo antes do encaminhamento, com link para a Privacidade
  e o Aviso Médico, e aviso de emergência na mesma tela.

### Portal do cliente · `portal.html`
- **My Doctor** com a Dra. Juliana Buttros: CRM 144522, RQE 75343, formação
  UNIFESP-EPM, foco em FUE, filiações. Sem preço, orçamento, depósito, desconto
  ou financiamento, e sem nenhuma rota que leve a cliente a contatá-la fora do
  fluxo. A galeria de antes e depois está construída e **desligada** até existir
  imagem aprovada e permissão documentada.
- **My Requirements** com o card de instruções: autor, clínica, categoria, hora
  de liberação, prioridade, versão, prazo e o texto exatamente como liberado.
  Confirmar leitura muda o status e nada mais, e a tela diz que isso não é
  consentimento de tratamento.
- **My Legal Documents**, novo: cada documento aceito com versão e data, e os
  pedidos de privacidade (cópia, correção, exclusão, encerramento) com número de
  caso. Exclusão abre chamado revisado, não apaga registro sob retenção.
- **My Trip** virou documento publicado e versionado, com identificador da
  viagem, versão, hora de emissão, aviso de atualização, impressão e PDF a partir
  da versão publicada, e as divulgações completas com rodapé em toda página
  impressa.
- **Support** com as duas portas separadas, *Ask My Physician* e *Ask RefreshU*,
  e o aviso de emergência acima delas.
- **Explore Brazil** reconstruído a partir do guia de São Paulo, com o filtro da
  estadia, e bem-estar, bate e volta e vida noturna fechados até liberação médica.
- **My Profile** com mensagens de serviço separadas de marketing, marketing
  desligado por padrão, e prontidão de viagem em campos separados, dizendo que
  cumpri-los não é liberação médica.

### Site público · `index.html`
- Os cinco pacotes, com cada linha rotulada Incluído, Coordenação incluída, Você
  paga o fornecedor, ou Serviço médico independente. Nenhum total único que
  faria a RefreshU parecer vendedora de serviço médico.
- Bloco do que nunca faz parte de um pacote, com a lista inteira do documento.
- Dois destinos, São Paulo e Rio, com os bairros dos dois guias premium. Nenhuma
  área descrita como totalmente segura.
- Componente de confiança alimentado por dados: só aparece o que já foi
  conquistado, o vencido some sozinho, e os cinco em andamento (GHA, Trustpilot,
  Google, DMCA, seguro) ficam guardados como pendentes e **não são exibidos**.
- Claims revisados: "carefully selected physicians" virou o processo de
  verificação que vocês de fato executam, o CTA virou "Request a physician
  review", e a linha de economia agora diz que comparação só é publicada com
  fonte e metodologia.

### Console de operação · `console.html`
Quatro áreas novas.

- **Physician instructions**: onde a operação registra o que a médica liberou.
  Os campos que permitiriam a RefreshU escrever conteúdo clínico não existem
  nesta tela. A matriz do mínimo necessário está visível, e a tabela de
  linguagem torna a regra operacional ("nunca *RefreshU cleared you*, sempre
  *your physician released this activity*").
- **Suppliers**: as redes de São Paulo e Rio da planilha, com rota de contato,
  pedido de parceria e status de outreach, mais as duas regras fixas (checar CNPJ,
  licença e seguro para passeio e transporte; e nunca deixar um fornecedor
  decidir se a cliente pode participar de uma atividade).
- **Legal & consent**: versões dos documentos com estado de aprovação, log de
  consentimento por cliente, e a tabela de credenciais públicas, que lê a mesma
  lista que o site renderiza para que os dois nunca divirjam.
- **Concerns**: reclamações com número de caso e as regras de tratamento de
  avaliação.
- O itinerário agora publica uma versão numerada e carimbada, mostra quantas
  mudanças estão sem publicar e pré-visualiza a tela da cliente.

### Comercial · `sales.html`
Os cinco pacotes oficiais substituíram os três antigos, com os mesmos rótulos de
quem entrega e quem cobra, e o bloco do que nunca é orçado junto.

### Versão pt-BR
`traduzir.py` foi ampliado e `/pt/` regenerado. O site público e o portal estão
com os blocos novos traduzidos.

---

## 3. Qualidade

| Tela | Acessibilidade |
|---|---|
| index.html | 100 |
| legal.html | 100 |
| portal.html | 100 |
| console.html | 100 |
| sales.html | 100 |
| assessment.html | 100 |
| signup.html | 100 |

Home mobile: performance 94, acessibilidade 100, boas práticas 100, SEO 100.

Contrastes corrigidos no caminho: o marcador de pendência do Legal Center, a
etiqueta de alerta do console e o rótulo de etapa do assessment estavam abaixo
de 4.5:1.

**Pendência conhecida:** dez tabelas antigas do console têm a primeira célula em
`<td>` em vez de `<th scope="row">`. Não derruba a nota, mas um leitor de tela
perde a referência da linha. Fica para uma passada de polimento, porque mexer nas
dez agora arriscaria o visual sem necessidade.

---

## 4. O que ainda depende da Agata

Chegaram quatro dependências vencidas do Anexo C, o que é uma boa notícia:
pacotes (A.3.11), conteúdo de destinos (A.5.9), dados da médica (A.3.4) e as
páginas legais (12.3 e 12.4). Continuam pendentes:

1. **Decisão e pagamento da infraestrutura**, vencida em 22/08. É o que trava o
   backend inteiro, e o próprio Anexo C diz que o desenvolvimento não passa da
   fundação sem banco.
2. **Autorização assinada da Dra. Juliana**, sem a qual o conteúdo dela não pode
   ser publicado, e a galeria de antes e depois não pode ser ligada.
3. **Definição do escopo clínico**, o conflito da seção 1 deste documento.
4. Valores e prazos de cancelamento, mínimo de cobertura do seguro, e a
   confirmação da regra de chegada com sete dias, todos marcados em dourado nas
   páginas legais.
5. Entidade legal, endereço, e-mails e domínio, que aparecem como campos entre
   colchetes no Legal Center.
6. Definições das etapas e ações internas (A.3.5), logotipo vetorial, e nomes e
   papéis da equipe inicial (A.3.1).

Continua valendo o que o documento de 2 de setembro dizia: mandar o e-mail
escrito para `info@werefreshyou.com` listando as dependências vencidas e
invocando a Cláusula 3.3. Sem esse e-mail, o atraso da cliente vira atraso seu.

---

## 5. Depois disso

O front-end das cinco aplicações está fechado contra os documentos. O que resta
é o backend, na ordem dos marcos M1 a M5 do contrato, e as doze medidas de
segurança da Cláusula 11.2. As telas novas já nascem com a forma que o backend
precisa preencher: objeto de instrução com versão e status, log de consentimento
por documento e versão, número de caso para reclamação e para pedido de
privacidade, e versão publicada de itinerário.
