#!/usr/bin/env python3
"""
Gera a versao pt-BR do site em /pt/ a partir dos arquivos em ingles.

O ingles e a fonte da verdade. Mexeu no texto de index/signin/portal? Roda
este script de novo e /pt/ acompanha. Nunca editar /pt/ na mao.

    python3 traduzir.py

A substituicao e por trecho literal do HTML, incluindo as tags de destaque,
porque em portugues a ordem das palavras muda e traduzir no del texto solto
quebraria frases com <em> e <b> no meio.
"""
import os, re, sys, shutil

RAIZ = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(RAIZ, 'pt')
PAGINAS = ['index.html', 'signin.html', 'portal.html']

# ---------------------------------------------------------------------------
# dicionario: trecho em ingles -> trecho em pt-BR
# regra de copy do projeto: sem travessao, virgula ou dois pontos no lugar
# ---------------------------------------------------------------------------
D = {

# --- portal: perfil da medica, instrucoes, itinerario, legal, suporte ---
'Dr. Juliana Buttros': 'Dra. Juliana Buttros',
'Plastic Surgeon · Hair Transplantation': 'Cirurgiã plástica · Transplante capilar',
'Independent Medical Provider': 'Profissional médica independente',
'About Dr. Juliana': 'Sobre a Dra. Juliana',
'Dr. Juliana Buttros is a plastic surgeon and master&rsquo;s degree holder trained at the Federal University of São Paulo (UNIFESP-EPM). Her professional practice is focused on hair transplantation using the FUE technique, with an emphasis on individualized planning and natural-looking hair restoration.': 'A Dra. Juliana Buttros é cirurgiã plástica e mestre pela Universidade Federal de São Paulo (UNIFESP-EPM). A prática dela é focada em transplante capilar pela técnica FUE, com ênfase em planejamento individualizado e resultado de aparência natural.',
'Her approach, in her own words, is published here once she has approved the final wording.': 'A abordagem dela, nas palavras dela, é publicada aqui assim que o texto final for aprovado.',
'Education and medical training': 'Formação e treinamento médico',
'Professional memberships': 'Filiações profissionais',
'Membership status is confirmed with the physician before any society badge or logo is displayed.': 'A filiação é confirmada com a médica antes de qualquer selo ou logotipo de sociedade ser exibido.',
'Before and after': 'Antes e depois',
'Dr. Juliana Buttros decides': 'A Dra. Juliana Buttros decide',
'RefreshU coordinates': 'A RefreshU coordena',
'View my requirements': 'Ver meus requisitos',
'View physician instructions': 'Ver as orientações da médica',
'Ask my physician': 'Falar com a minha médica',
'Contact RefreshU concierge': 'Falar com o concierge RefreshU',
'This page carries professional profile information only. Consultation scheduling and every message stay inside the approved RefreshU and provider workflow.': 'Esta página traz apenas informação de perfil profissional. O agendamento da consulta e as mensagens ficam dentro do fluxo aprovado da RefreshU e da profissional.',

'Physician instructions': 'Orientações da médica',
'Released by': 'Liberado por',
'Action required': 'Precisa de ação',
'Category': 'Categoria',
'Released': 'Liberado em',
'Priority': 'Prioridade',
'Version': 'Versão',
'Important': 'Importante',
'I have read these instructions': 'Li estas orientações',
'View previous version': 'Ver a versão anterior',
'Everything else on your list': 'O resto da sua lista',
'Reading confirmation records that you opened the instruction. It does not change it, and it is not medical consent. If your physician releases a revised version, you are asked to read it again.': 'Confirmar a leitura registra apenas que você abriu a orientação. Não altera nada e não é consentimento médico. Se a sua médica liberar uma versão revisada, você é convidado a ler de novo.',

'Your Brazil journey': 'Sua jornada no Brasil',
'Print current version': 'Imprimir a versão atual',
'Download current PDF': 'Baixar o PDF atual',
'Important itinerary disclosure': 'Aviso importante sobre o roteiro',
'Independent medical provider': 'Profissional médica independente',
'Third parties, changes and no guarantee': 'Terceiros, mudanças e ausência de garantia',
'Travel documents, insurance and accuracy': 'Documentos de viagem, seguro e conferência',
'Optional activities and printed copies': 'Atividades opcionais e cópias impressas',

'My Legal Documents': 'Meus documentos legais',
'Your privacy requests': 'Seus pedidos de privacidade',
'A copy of your information': 'Uma cópia das suas informações',
'A correction': 'Uma correção',
'Deletion': 'Exclusão',
'Close your account': 'Encerrar sua conta',
'Request a copy': 'Pedir uma cópia',
'Request a correction': 'Pedir uma correção',
'Request deletion': 'Pedir exclusão',
'Request closure': 'Pedir encerramento',

'Ask RefreshU': 'Falar com a RefreshU',
'Medical': 'Médico',
'Travel and concierge': 'Viagem e concierge',
'Write to my physician': 'Escrever para a minha médica',
'Message Beatriz': 'Escrever para a Beatriz',
'Urgent, outside hours': 'Urgente, fora do horário',
'Account and payments': 'Conta e pagamentos',
'A concern about the service': 'Uma reclamação sobre o serviço',
'Report a concern': 'Registrar uma reclamação',

'Travel readiness': 'Prontidão de viagem',
'Service messages': 'Mensagens de serviço',
'Marketing': 'Marketing',
'Michelin and fine dining': 'Alta gastronomia',
'Everyday dining': 'Restaurantes do dia a dia',
'Parks and neighbourhoods': 'Parques e bairros',
'Art and museums': 'Arte e museus',
'Theatre and culture': 'Teatro e cultura',
'Luxury shopping': 'Compras de luxo',
'Wellness and spa': 'Bem-estar e spa',
'Wine and gastronomy': 'Vinho e gastronomia',
'Day trips': 'Bate e volta',
'Exclusive experiences': 'Experiências exclusivas',
'Family and companion': 'Família e acompanhante',
'Nightlife': 'Vida noturna',
'Released for today': 'Liberado para hoje',
'Opens Saturday': 'Abre no sábado',
'Pending physician release': 'Aguardando liberação médica',

# --- blocos novos de setembro/2026: pacotes, confianca, destinos, papel ---
'RefreshU is a medical concierge, referral and travel-coordination platform. Medical care is provided by independent physicians and clinics, who decide eligibility, treatment and every clinical requirement.': 'A RefreshU é uma plataforma de concierge médico, encaminhamento e coordenação de viagem. O cuidado médico é prestado por médicos e clínicas independentes, que decidem elegibilidade, tratamento e todo requisito clínico.',

'Hair and face procedures with independent physicians whose credentials are verified before their profile is published.': 'Procedimentos de cabelo e face com médicos independentes cujas credenciais são verificadas antes de o perfil ser publicado.',
'<p><b>Exceptional care.</b> Independent physicians whose registration, qualification and society memberships are verified before publication, and a journey coordinated from the first referral to the last follow up.</p>': '<p><b>Cuidado excepcional.</b> Médicos independentes com registro, qualificação e filiações verificados antes da publicação, e uma jornada coordenada do primeiro encaminhamento ao último acompanhamento.</p>',

'Choose your RefreshU experience': 'Escolha a sua experiência RefreshU',
'Five levels of concierge support. Medical procedures and medical services are never part of a RefreshU package: they are provided and charged separately by independent physicians and clinics.': 'Cinco níveis de suporte de concierge. Procedimentos e serviços médicos nunca fazem parte de um pacote RefreshU, são prestados e cobrados à parte por médicos e clínicas independentes.',
'Included': 'Incluído',
'Coordination included': 'Coordenação incluída',
'You pay the third party': 'Você paga o fornecedor',
'Independent medical service': 'Serviço médico independente',
'Most complete': 'Mais completo',

'RefreshU Essential': 'RefreshU Essential',
'For independent travellers who want the important details organised while keeping their flexibility.': 'Para quem viaja por conta própria e quer os detalhes importantes organizados sem abrir mão da flexibilidade.',
'RefreshU Signature': 'RefreshU Signature',
'The full experience, coordinated from arrival to departure. Everything in Essential, plus:': 'A experiência completa, coordenada da chegada à partida. Tudo do Essential, mais:',
'RefreshU White Glove': 'RefreshU White Glove',
'Our highest level of personalised support. Everything in Signature, plus:': 'Nosso nível mais alto de suporte personalizado. Tudo do Signature, mais:',
'RefreshU Companion &amp; Family': 'RefreshU Companion &amp; Family',
'For couples, friends or family travelling together, whether one person or several are seeing participating providers.': 'Para casais, amigos ou família viajando juntos, seja uma pessoa ou várias sendo atendidas por profissionais participantes.',
'RefreshU Bespoke': 'RefreshU Bespoke',
'A fully customised experience when travel, hospitality, companion or lifestyle requirements go beyond the standard packages.': 'Uma experiência totalmente sob medida quando as necessidades de viagem, hospedagem, acompanhante ou estilo de vida vão além dos pacotes padrão.',

'A RefreshU dedicated concierge is a non-clinical hospitality and logistics professional, and is not a private nurse or healthcare professional.': 'O concierge dedicado da RefreshU é um profissional de hospitalidade e logística, não é enfermeiro particular nem profissional de saúde.',
'Each person receiving medical services completes their own physician review, provider documentation, medical consents, provider agreement and medical payment. One person&rsquo;s physician decision does not apply to another traveller.': 'Cada pessoa que recebe serviços médicos faz a própria análise médica, a própria documentação, os próprios consentimentos, o próprio contrato com o profissional e o próprio pagamento médico. A decisão do médico sobre uma pessoa não vale para outro viajante.',
'Bespoke services are quoted individually and shown in your Service Summary before purchase.': 'Serviços sob medida são orçados individualmente e aparecem no seu Resumo de Serviços antes da compra.',

'What is never part of a RefreshU package': 'O que nunca faz parte de um pacote RefreshU',
'Physician consultation, medical evaluation and determination of candidacy, surgery or procedure, anesthesia or sedation, hospital and facility services, laboratory or diagnostic testing, interpretation of results, prescriptions and medication selection, clinical nursing, medical clearance, clinical informed consent, medical aftercare and management of complications, and emergency medical services. These are provided and charged separately by independent healthcare professionals.': 'Consulta médica, avaliação médica e definição de elegibilidade, cirurgia ou procedimento, anestesia ou sedação, serviços hospitalares, exames laboratoriais e de diagnóstico, interpretação de resultados, prescrição e escolha de medicamentos, enfermagem clínica, liberação médica, consentimento informado clínico, cuidado pós-operatório e manejo de complicações, e atendimento de emergência. Tudo isso é prestado e cobrado à parte por profissionais de saúde independentes.',
'Read the concierge terms': 'Ler os termos do concierge',

'São Paulo and Rio de Janeiro': 'São Paulo e Rio de Janeiro',
'RefreshU currently operates concierge experiences in two Brazilian cities. You choose the one you want your stay built around, and the concierge experience is the same in both.': 'A RefreshU opera experiências de concierge em duas cidades brasileiras. Você escolhe em qual quer montar a sua estadia, e a experiência de concierge é a mesma nas duas.',
'Jardins, Itaim Bibi, Vila Nova Conceição and Alto de Pinheiros. Michelin dining, Ibirapuera, MASP, Oscar Freire and the São Roque wine route an hour away.': 'Jardins, Itaim Bibi, Vila Nova Conceição e Alto de Pinheiros. Alta gastronomia, Ibirapuera, MASP, Oscar Freire e a rota do vinho de São Roque a uma hora dali.',
'Ipanema, Leblon, Copacabana and Jardim Botânico. Sugarloaf, Christ the Redeemer, the Botanical Garden, Parque Lage and the beach when your physician releases it.': 'Ipanema, Leblon, Copacabana e Jardim Botânico. Pão de Açúcar, Cristo Redentor, Jardim Botânico, Parque Lage e a praia quando o seu médico liberar.',
'Neighbourhoods, venues and routes are concierge-selected. No area is described as completely safe, and private door-to-door transport is recommended at night.': 'Bairros, lugares e trajetos são selecionados pelo concierge. Nenhuma área é descrita como totalmente segura, e transporte privativo porta a porta é recomendado à noite.',

'Why you can trust this': 'Por que você pode confiar nisso',
'Only claims we can actually support appear here. Certifications we are working towards are not displayed until they are earned.': 'Só aparece aqui o que conseguimos sustentar. Certificações em andamento não são exibidas antes de serem conquistadas.',
'RefreshU does not describe itself as HIPAA certified, approved or verified, and does not display an accreditation that belongs to a provider as if it belonged to RefreshU.': 'A RefreshU não se descreve como certificada, aprovada ou verificada pela HIPAA, e não exibe como sua uma acreditação que pertence a um profissional.',

'Request a physician review': 'Solicitar análise médica',
'General educational information. Only a physician can determine whether a procedure is appropriate for you.': 'Informação educativa geral. Só um médico pode determinar se um procedimento é adequado para você.',
'The same money can buy a great deal more than the procedure alone. Do the treatment you have been considering, and live Brazil, with one concierge coordinating the whole journey. Any comparison against United States pricing is published only with its source and its methodology.': 'O mesmo dinheiro pode comprar muito mais do que só o procedimento. Faça o tratamento que você vem considerando e viva o Brasil, com um concierge coordenando a jornada inteira. Qualquer comparação com preços dos Estados Unidos é publicada apenas com a fonte e a metodologia.',

'Not for medical emergencies.': 'Não é para emergências médicas.',
'If you believe you are experiencing a medical emergency, contact your local emergency service immediately. For procedure-related medical questions, contact your treating physician or clinic.': 'Se você acha que está tendo uma emergência médica, procure o serviço de emergência local imediatamente. Para dúvidas médicas sobre o procedimento, fale com o seu médico ou a clínica.',
'Legal': 'Jurídico',
'Terms of Use': 'Termos de uso',
'Privacy Policy': 'Política de privacidade',
'Medical Disclaimer': 'Aviso médico',
'Independent Providers': 'Profissionais independentes',
'Concierge Terms': 'Termos do concierge',
'Cancellation &amp; Refunds': 'Cancelamento e reembolso',
'Travel &amp; Insurance': 'Viagem e seguro',
'Payment &amp; Fees': 'Pagamentos e taxas',
'Privacy Choices': 'Escolhas de privacidade',
'Accessibility': 'Acessibilidade',
'Contact &amp; Complaints': 'Contato e reclamações',
'Packages': 'Pacotes',
# --- clausula 12.6, fronteira clinica (correcao 2026-09)
'Your questionnaire and photos go straight to the physician, in their own system. They never pass through RefreshU.': 'Seu questionário e suas fotos vão direto para o médico, no sistema dele. Nada disso passa pela RefreshU.',
'>Send your travel insurance<': '>Envie seu seguro-viagem<',
'It is the last document we need from you, and it is due today.': 'É o último documento que precisamos de você, e o prazo é hoje.',
'>Take your results to the consultation<': '>Leve seus exames para a consulta<',
'The laboratory sends them straight to Dr. Camila Rocha, so there is nothing to send us. We will mark the item complete as soon as she confirms she has them.': 'O laboratório envia direto para a Dra. Camila Rocha, então não há nada para nos mandar. Marcamos o item como concluído assim que ela confirmar que recebeu.',
'>See where each item stands<': '>Ver como está cada item<',
'your travel insurance document is due today. It is the last item we are waiting on from you.': 'seu documento de seguro-viagem vence hoje. É o último item que estamos esperando de você.',
'<b>Medical questionnaire</b><span>Dr. Camila Rocha confirmed she received it</span>': '<b>Questionário médico</b><span>A Dra. Camila Rocha confirmou que recebeu</span>',
'<b>Travel insurance documentation</b><span>Due today, upload it here</span>': '<b>Documentação do seguro-viagem</b><span>Vence hoje, envie por aqui</span>',
'<b>Blood work required by your physician</b><span>Collection today at 10:00. The laboratory sends it to her directly</span>': '<b>Exames de sangue pedidos pela sua médica</b><span>Coleta hoje às 10:00. O laboratório envia direto para ela</span>',
'Clinical items carry a status here and nothing more. Questionnaires, exams and photographs go straight between you and your physician, and this checklist only records when she confirms an item. Files you upload here are travel and administrative documents.': 'Os itens clínicos aqui carregam apenas um status. Questionários, exames e fotografias vão direto entre você e sua médica, e esta lista só registra quando ela confirma um item. Os arquivos que você envia aqui são documentos de viagem e administrativos.',
'>Your travel and administrative documents, in one place.<': '>Seus documentos de viagem e administrativos, em um só lugar.<',
'<th scope="row">Transport schedule</th>': '<th scope="row">Programação de transporte</th>',
'<th scope="row">Your itinerary, printable</th>': '<th scope="row">Seu itinerário, para imprimir</th>',
'<th scope="row">Consent forms</th>': '<th scope="row">Termos de consentimento</th>',
'<th scope="row">Invoices and receipts</th>': '<th scope="row">Faturas e recibos</th>',
'>Signature pending<': '>Assinatura pendente<',
'>Upload pending<': '>Envio pendente<',
'>Issued<': '>Emitido<',
'Your medical records stay with your physician. The questionnaire, any photographs, laboratory results and clinical reports live in her own system, which is where you send them and where you ask for them. RefreshU neither stores nor displays them.': 'Seus registros médicos ficam com sua médica. O questionário, as fotografias, os resultados de exames e os laudos vivem no sistema dela, que é para onde você envia e onde você os pede. A RefreshU não guarda nem exibe esses documentos.',
'>Public site<': '>Site público<',
'>Operations<': '>Operação<',
'>Sales<': '>Comercial<',
'>Client portal<': '>Portal do cliente<',
'Every name, date, clinic, hotel and document on these screens is sample data.': 'Todo nome, data, clínica, hotel e documento nestas telas é dado de exemplo.',
# --- cabecalho e navegacao
'RefreshU · Medical Concierge, Savings and a Trip Through Brazil': 'RefreshU · Concierge médico, economia e uma viagem pelo Brasil',
'Exceptional aesthetic care in Brazil, meaningful savings, and a journey coordinated end to end by a single concierge. Hair and Face and Neck procedures with carefully selected physicians.': 'Cuidado estético excepcional no Brasil, economia relevante e uma jornada coordenada de ponta a ponta por um único concierge. Procedimentos de cabelo, rosto e pescoço com médicos criteriosamente selecionados.',
'RefreshU · Refresh Yourself. Experience Brazil.': 'RefreshU · Renove você. Viva o Brasil.',
'The procedure is the reason for the trip. RefreshU makes the entire trip worth it.': 'O procedimento é o motivo da viagem. A RefreshU faz a viagem inteira valer a pena.',
'>Skip to content<': '>Ir para o conteúdo<',
'aria-label="RefreshU, home"': 'aria-label="RefreshU, início"',
'aria-label="Main"': 'aria-label="Principal"',
'>Treatments<': '>Tratamentos<',
'>Doctors<': '>Médicos<',
'>Destinations<': '>Destinos<',
'>Savings<': '>Economia<',
'>Experience<': '>Experiência<',
'>How It Works<': '>Como funciona<',
'>Sign In<': '>Entrar<',
'>Start My Evaluation<': '>Iniciar minha avaliação<',
'aria-label="Open menu"': 'aria-label="Abrir menu"',
'aria-label="Language"': 'aria-label="Idioma"',

# --- hero
'alt="Coastline of Rio de Janeiro at golden hour"': 'alt="Litoral do Rio de Janeiro na luz do fim da tarde"',
'Refresh yourself.<br>Experience Brazil.': 'Renove você.<br>Viva o Brasil.',
'Exceptional aesthetic care in Brazil, savings that can be meaningful, and a trip built around you: the physician, the procedure, the hotel, the transport, the meals, the recovery, and everything you will actually want to see.': 'Cuidado estético excepcional no Brasil, uma economia que pode ser relevante e uma viagem montada em torno de você: o médico, o procedimento, o hotel, o transporte, as refeições, a recuperação e tudo o que você de fato vai querer conhecer.',

# --- pilares
'<b>Exceptional value.</b> Access high quality aesthetic procedures in Brazil, with savings that can be significant against the prices practiced in the United States.': '<b>Valor excepcional.</b> Acesso a procedimentos estéticos de alta qualidade no Brasil, com economia que pode ser significativa em relação aos preços praticados nos Estados Unidos.',
'<b>Exceptional care.</b> Carefully selected physicians and a medical journey that is coordinated from the first questionnaire to the last follow up.': '<b>Cuidado excepcional.</b> Médicos criteriosamente selecionados e uma jornada médica coordenada do primeiro questionário até o último retorno.',
'<b>An unforgettable trip.</b> The trip you have to take becomes a trip worth taking: good hotels, restaurants, neighborhoods, culture, beaches and time that fits your recovery.': '<b>Uma viagem inesquecível.</b> A viagem que você precisa fazer vira uma viagem que vale a pena fazer: bons hotéis, restaurantes, bairros, cultura, praias e um tempo que cabe na sua recuperação.',
'<h2>Save</h2>': '<h2>Economize</h2>',
'<h2>Refresh</h2>': '<h2>Renove</h2>',
'<h2>Experience Brazil</h2>': '<h2>Viva o Brasil</h2>',

# --- ideia central
'The procedure is the reason for the trip.<br><em>RefreshU makes the entire trip worth it.</em>': 'O procedimento é o motivo da viagem.<br><em>A RefreshU faz a viagem inteira valer a pena.</em>',

# --- economia
'<h2 class="display">What could you save?</h2>': '<h2 class="display">Quanto você pode economizar?</h2>',
'You are already considering spending this money on a procedure. The real question is what that same money buys you through RefreshU.': 'Você já está considerando gastar esse dinheiro em um procedimento. A pergunta de verdade é o que esse mesmo dinheiro compra através da RefreshU.',
'>Select a procedure<': '>Selecione um procedimento<',
'<option>FUE hair transplant</option>': '<option>Transplante capilar FUE</option>',
'<option>Hair restoration</option>': '<option>Restauração capilar</option>',
'<option>Facelift</option>': '<option>Lifting facial</option>',
'<option>Neck lift</option>': '<option>Lifting de pescoço</option>',
'<option>Rhinoplasty</option>': '<option>Rinoplastia</option>',
'<option>Blepharoplasty</option>': '<option>Blefaroplastia</option>',
'<span>Typical range in the United States</span>': '<span>Faixa típica nos Estados Unidos</span>',
'<span>Procedure range in Brazil</span>': '<span>Faixa do procedimento no Brasil</span>',
'<span>The RefreshU experience</span>': '<span>A experiência RefreshU</span>',
'<span>Potential savings</span>': '<span>Economia potencial</span>',
'>Pending verification<': '>A confirmar<',
'Then imagine what else you could live with the difference.': 'Agora imagine o que mais você poderia viver com a diferença.',
'Every figure and the comparison methodology require a defensible source and legal approval before this section is published.': 'Todos os valores e a metodologia de comparação exigem fonte defensável e aprovação jurídica antes desta seção ir ao ar.',
'Do not spend the money on the procedure alone. Have the procedure <em>and</em> the experience.': 'Não gaste o dinheiro só no procedimento. Tenha o procedimento <em>e</em> a experiência.',

# --- tratamentos
'<h2 class="display">Treatments</h2>': '<h2 class="display">Tratamentos</h2>',
'We are launching with two verticals, each one built around physicians who perform these procedures every week.': 'Começamos com duas verticais, cada uma construída em torno de médicos que realizam esses procedimentos toda semana.',
'alt="Man in his fifties outdoors, natural light"': 'alt="Homem na casa dos cinquenta ao ar livre, luz natural"',
'alt="Portrait in soft daylight, eyes closed"': 'alt="Retrato em luz suave, olhos fechados"',
'<h3>Hair</h3>': '<h3>Cabelo</h3>',
'<h3>Face and Neck</h3>': '<h3>Rosto e pescoço</h3>',
'<li>FUE hair transplant</li>': '<li>Transplante capilar FUE</li>',
'<li>Hair restoration</li>': '<li>Restauração capilar</li>',
'<li>Related treatments performed by a physician</li>': '<li>Tratamentos correlatos realizados por médico</li>',
'<li>Facelift</li>': '<li>Lifting facial</li>',
'<li>Neck lift</li>': '<li>Lifting de pescoço</li>',
'<li>Rhinoplasty</li>': '<li>Rinoplastia</li>',
'<li>Blepharoplasty</li>': '<li>Blefaroplastia</li>',
'<li>Botox and fillers</li>': '<li>Botox e preenchimentos</li>',
'<li>Other facial procedures</li>': '<li>Outros procedimentos faciais</li>',
'See If I&rsquo;m a Candidate': 'Ver se eu sou candidato',
'Body, dentistry, dermatology, wellness and further aesthetic verticals are planned, and the platform is built to receive them.': 'Corpo, odontologia, dermatologia, bem-estar e outras verticais estéticas estão previstas, e a plataforma já foi construída para recebê-las.',

# --- como funciona
'<h2 class="display">How RefreshU works</h2>': '<h2 class="display">Como a RefreshU funciona</h2>',
'Nine steps, one coordinator, and a clear line between what we handle and what the physician decides.': 'Nove passos, um coordenador e uma linha clara entre o que cuidamos e o que o médico decide.',
'<h3>Choose Your Refresh</h3>': '<h3>Escolha o seu Refresh</h3>',
'<p>Explore procedures and tell us what matters to you.</p>': '<p>Conheça os procedimentos e conte o que importa para você.</p>',
'<h3>Submit Your Information</h3>': '<h3>Envie suas informações</h3>',
'<p>Complete a private questionnaire and send the requested photos.</p>': '<p>Preencha um questionário privado e envie as fotos solicitadas.</p>',
'<h3>Physician Review</h3>': '<h3>Análise médica</h3>',
'<p>A participating physician reviews your information. RefreshU does not make the medical decision.</p>': '<p>Um médico participante analisa suas informações. A RefreshU não toma a decisão médica.</p>',
'<h3>Meet Your RefreshU Concierge</h3>': '<h3>Conheça seu concierge RefreshU</h3>',
'<p>Talk through the experience, the destination, concierge services, general pricing, potential savings, travel expectations, packages and next steps.</p>': '<p>Converse sobre a experiência, o destino, os serviços de concierge, os preços gerais, a economia potencial, as expectativas da viagem, os pacotes e os próximos passos.</p>',
'<h3>Meet Your Doctor</h3>': '<h3>Conheça seu médico</h3>',
'<p>The physician handles eligibility, the treatment plan, risks, exams, guidance and every clinical question.</p>': '<p>O médico cuida da elegibilidade, do plano de tratamento, dos riscos, dos exames, das orientações e de toda dúvida clínica.</p>',
'<h3>Build Your Brazil Experience</h3>': '<h3>Monte sua experiência no Brasil</h3>',
'<p>Travel, hotel, transport, appointments, concierge services, restaurants, shopping, attractions, wellness and activities compatible with recovery.</p>': '<p>Viagem, hotel, transporte, consultas, serviços de concierge, restaurantes, compras, atrações, bem-estar e atividades compatíveis com a recuperação.</p>',
'<h3>Arrive in Brazil</h3>': '<h3>Chegue ao Brasil</h3>',
'<p>The concierge experience begins the moment you land.</p>': '<p>A experiência de concierge começa no momento em que você pousa.</p>',
'<h3>Experience, Procedure, Recovery</h3>': '<h3>Experiência, procedimento, recuperação</h3>',
'<p>Enjoy Brazil before and after the procedure, as your physician allows.</p>': '<p>Aproveite o Brasil antes e depois do procedimento, conforme a liberação do seu médico.</p>',
'<h3>Return Home Refreshed</h3>': '<h3>Volte para casa renovado</h3>',
'<p>RefreshU coordinates the departure and any follow up logistics that apply.</p>': '<p>A RefreshU coordena a partida e a logística de acompanhamento que for aplicável.</p>',

# --- Brasil
'<h2 class="display">Brazil is part of the product</h2>': '<h2 class="display">O Brasil faz parte do produto</h2>',
'If you are already flying somewhere to have the procedure, why would the trip not be extraordinary?': 'Se você já vai pegar um avião para fazer o procedimento, por que a viagem não seria extraordinária?',
'alt="Plated dish at a restaurant table"': 'alt="Prato montado em uma mesa de restaurante"',
'alt="Wood panelled hotel suite"': 'alt="Suíte de hotel revestida em madeira"',
'alt="Brazilian coastline seen from above"': 'alt="Litoral brasileiro visto de cima"',
'alt="Modernist Brazilian architecture"': 'alt="Arquitetura modernista brasileira"',
'alt="City park with a lake"': 'alt="Parque urbano com um lago"',
'alt="Person resting in calm water at the horizon"': 'alt="Pessoa descansando em água calma no horizonte"',
'alt="Warm restaurant interior in the evening"': 'alt="Interior aconchegante de restaurante à noite"',
'<figcaption>Food and restaurants</figcaption>': '<figcaption>Gastronomia e restaurantes</figcaption>',
'<figcaption>Hotels</figcaption>': '<figcaption>Hotéis</figcaption>',
'<figcaption>Beaches</figcaption>': '<figcaption>Praias</figcaption>',
'<figcaption>Architecture</figcaption>': '<figcaption>Arquitetura</figcaption>',
'<figcaption>Nature and parks</figcaption>': '<figcaption>Natureza e parques</figcaption>',
'<figcaption>Wellness</figcaption>': '<figcaption>Bem-estar</figcaption>',
'<figcaption>Culture, shopping and nightlife when appropriate</figcaption>': '<figcaption>Cultura, compras e vida noturna quando apropriado</figcaption>',
'Food, architecture, shopping, beaches, nature, culture, hotels, wellness, nightlife when it is appropriate, and the Brazilian hospitality that holds all of it together.': 'Gastronomia, arquitetura, compras, praias, natureza, cultura, hotéis, bem-estar, vida noturna quando apropriado, e a hospitalidade brasileira que segura tudo isso junto.',
'The procedure creates the reason to travel. <em>RefreshU turns the trip into an experience.</em>': 'O procedimento cria o motivo para viajar. <em>A RefreshU transforma a viagem em experiência.</em>',

# --- cronograma
'<h2 class="display">The medical schedule runs the trip</h2>': '<h2 class="display">O cronograma médico comanda a viagem</h2>',
'The travel experience always adapts to what the physician requires, never the other way around.': 'A experiência de viagem sempre se adapta ao que o médico exige, nunca o contrário.',
'Medical schedule <i>+</i> travel schedule <i>+</i> your preferences <i>=</i> your RefreshU itinerary': 'Cronograma médico <i>+</i> cronograma de viagem <i>+</i> suas preferências <i>=</i> seu roteiro RefreshU',
'<b>Monday</b><span>Arrival, airport transfer, hotel check in, welcome kit, dinner reservation</span>': '<b>Segunda</b><span>Chegada, transfer do aeroporto, check-in no hotel, kit de boas-vindas, reserva para o jantar</span>',
'<b>Tuesday</b><span>Breakfast, pre operative blood work, lunch, shopping or a walk through the neighborhood, dinner</span>': '<b>Terça</b><span>Café da manhã, exames de sangue pré-operatórios, almoço, compras ou um passeio pelo bairro, jantar</span>',
'<b>Wednesday</b><span>Medical consultation, recovery preparation, a quiet afternoon</span>': '<b>Quarta</b><span>Consulta médica, preparo para a recuperação, uma tarde tranquila</span>',
'<b>Thursday</b><span>Driver, procedure, return to the hotel, recovery support</span>': '<b>Quinta</b><span>Motorista, procedimento, retorno ao hotel, suporte de recuperação</span>',
'<b>Friday</b><span>Follow up with the physician, recovery at the hotel, meal delivery and concierge</span>': '<b>Sexta</b><span>Retorno com o médico, recuperação no hotel, entrega de refeições e concierge</span>',
'<b>Saturday</b><span>Activities cleared by the physician, a restaurant booking, a calm day in São Paulo</span>': '<b>Sábado</b><span>Atividades liberadas pelo médico, uma reserva em restaurante, um dia calmo em São Paulo</span>',
'This is an illustration. Your itinerary follows your physician&rsquo;s guidance and moves with it.': 'Isto é uma ilustração. Seu roteiro segue as orientações do seu médico e se move junto com elas.',

# --- medicos
'<h2 class="display">You know the physician before anything is decided</h2>': '<h2 class="display">Você conhece o médico antes de qualquer decisão</h2>',
'RefreshU is not a directory. Every participating physician is reviewed and presented in full, so the person operating on you is never an unknown name on a schedule.': 'A RefreshU não é um diretório. Cada médico participante é avaliado e apresentado por inteiro, para que a pessoa que vai operar você nunca seja um nome desconhecido em uma agenda.',
'<li>Name and specialty</li>': '<li>Nome e especialidade</li>',
'<li>Credentials</li>': '<li>Credenciais</li>',
'<li>Clinic or hospital</li>': '<li>Clínica ou hospital</li>',
'<li>Years of experience</li>': '<li>Anos de experiência</li>',
'<li>Location</li>': '<li>Localização</li>',
'<li>Languages spoken</li>': '<li>Idiomas</li>',
'<li>Procedures performed</li>': '<li>Procedimentos realizados</li>',
'<li>Biography and approach</li>': '<li>Biografia e abordagem</li>',
'<li>Before and after gallery</li>': '<li>Galeria de antes e depois</li>',
'<li>Video</li>': '<li>Vídeo</li>',
'<li>Images of the clinic</li>': '<li>Imagens da clínica</li>',
'<li>Experience with international patients</li>': '<li>Experiência com pacientes internacionais</li>',

# --- destino
'<h2 class="display">Your São Paulo Refresh</h2>': '<h2 class="display">Seu Refresh em São Paulo</h2>',
'We are launching in São Paulo, the city with the deepest medical infrastructure in the country and enough life around it to make the week feel like a trip rather than an appointment.': 'Começamos por São Paulo, a cidade com a infraestrutura médica mais profunda do país e vida suficiente em volta para a semana parecer uma viagem, não uma consulta.',
'alt="Avenida Paulista seen from above"': 'alt="Avenida Paulista vista de cima"',
'<h3>Where you will stay</h3>': '<h3>Onde você vai ficar</h3>',
'<p>Premium hotels chosen for comfort during recovery, proximity to your clinic and a neighborhood worth walking.</p>': '<p>Hotéis premium escolhidos pelo conforto durante a recuperação, pela proximidade da sua clínica e por um bairro que vale caminhar.</p>',
'<h3>Where you will eat</h3>': '<h3>Onde você vai comer</h3>',
'<p>Restaurants and Brazilian food, from the everyday to the reservation you will tell people about, with meal delivery when you should be resting.</p>': '<p>Restaurantes e comida brasileira, do dia a dia à reserva que você vai contar para os outros, com entrega de refeições nos dias em que você deve descansar.</p>',
'<h3>What you can experience</h3>': '<h3>O que você pode viver</h3>',
'<p>Neighborhoods, museums, parks, shopping and wellness, filtered by what your recovery allows on each specific day.</p>': '<p>Bairros, museus, parques, compras e bem-estar, filtrados pelo que a sua recuperação permite em cada dia.</p>',
'<h3>Your medical journey</h3>': '<h3>Sua jornada médica</h3>',
'<p>Clinics, consultations, pre operative exams and the procedure itself, held together in one schedule.</p>': '<p>Clínicas, consultas, exames pré-operatórios e o próprio procedimento, reunidos em uma agenda só.</p>',
'<h3>Your RefreshU concierge</h3>': '<h3>Seu concierge RefreshU</h3>',
'<p>Transport, bookings and the one contact who knows your whole week.</p>': '<p>Transporte, reservas e o contato único que conhece a sua semana inteira.</p>',
'Florianópolis, Porto Alegre and further destinations follow.': 'Florianópolis, Porto Alegre e outros destinos vêm na sequência.',

# --- concierge
'<h2 class="display">One person coordinates all of it</h2>': '<h2 class="display">Uma pessoa coordena tudo isso</h2>',
'You should not need five apps, twenty emails and a spreadsheet. Your concierge is a single point of contact for the entire experience.': 'Você não deveria precisar de cinco aplicativos, vinte e-mails e uma planilha. Seu concierge é um ponto de contato único para a experiência inteira.',
'<h3>Transport</h3>': '<h3>Transporte</h3>',
'<p>Airport transfer, hotel, clinic and a private driver.</p>': '<p>Transfer do aeroporto, hotel, clínica e motorista particular.</p>',
'<h3>Dining</h3>': '<h3>Alimentação</h3>',
'<p>Recommendations, reservations and meal delivery.</p>': '<p>Recomendações, reservas e entrega de refeições.</p>',
'<h3>Experiences</h3>': '<h3>Experiências</h3>',
'<p>Restaurants, shopping, museums, tours, local attractions and activities compatible with recovery.</p>': '<p>Restaurantes, compras, museus, passeios, atrações locais e atividades compatíveis com a recuperação.</p>',
'<h3>Personal care</h3>': '<h3>Cuidado pessoal</h3>',
'<p>Barber, hairdresser, nails, lashes and approved wellness professionals.</p>': '<p>Barbeiro, cabeleireiro, unhas, cílios e profissionais de bem-estar aprovados.</p>',
'<h3>Convenience</h3>': '<h3>Conveniência</h3>',
'<p>Laundry, shopping, clothing and pharmacy support for items prescribed by the physician.</p>': '<p>Lavanderia, compras, roupas e apoio na farmácia para itens prescritos pelo médico.</p>',
'<h3>Recovery support</h3>': '<h3>Suporte de recuperação</h3>',
'<p>Qualified recovery professionals where appropriate, services approved by the physician, and transport for the return.</p>': '<p>Profissionais de recuperação qualificados quando apropriado, serviços aprovados pelo médico e transporte para o retorno.</p>',
'alt="Rear seat of a private car"': 'alt="Banco traseiro de um carro particular"',
'<h3>Medical services at the hotel</h3>': '<h3>Serviços médicos no hotel</h3>',
'<p>Where it is legally permitted and requested by your physician, qualified professionals can attend you at the hotel: blood collection, laboratory services, basic exams ordered by the physician, an electrocardiogram when properly provided, a nursing visit and physician approved recovery support.</p>': '<p>Onde for legalmente permitido e solicitado pelo seu médico, profissionais qualificados podem atender você no hotel: coleta de sangue, serviços laboratoriais, exames básicos solicitados pelo médico, eletrocardiograma quando prestado de forma adequada, visita de enfermagem e suporte de recuperação aprovado pelo médico.</p>',
'RefreshU handles the logistics. The physician and the clinic control every clinical requirement.': 'A RefreshU cuida da logística. O médico e a clínica controlam todas as exigências clínicas.',

# --- kit
'alt="Folded linen button front shirt with reading glasses"': 'alt="Camisa de linho dobrada com botões na frente e óculos de leitura"',
'<h2 class="display">The welcome kit</h2>': '<h2 class="display">O kit de boas-vindas</h2>',
'Waiting for you at check in, put together for the days when getting dressed is not supposed to be an effort.': 'Esperando por você no check-in, montado para os dias em que se vestir não deveria dar trabalho.',
'<li>RefreshU recovery shirt, buttoned at the front</li>': '<li>Camisa de recuperação RefreshU, com botões na frente</li>',
'<li>Travel or neck pillow</li>': '<li>Almofada de viagem ou de pescoço</li>',
'<li>Eye mask</li>': '<li>Máscara para os olhos</li>',
'<li>Lip balm or lip mask</li>': '<li>Protetor labial ou máscara labial</li>',
'<li>Branded bag</li>': '<li>Bolsa da marca</li>',
'<li>Water bottle</li>': '<li>Garrafa de água</li>',
'<li>Recovery friendly snacks</li>': '<li>Lanches compatíveis com a recuperação</li>',
'<li>Power adapter</li>': '<li>Adaptador de tomada</li>',
'<li>QR code to your dashboard</li>': '<li>QR code para o seu painel</li>',
'<li>Your personalized Brazil itinerary</li>': '<li>Seu roteiro personalizado do Brasil</li>',
'<li>Your concierge contact</li>': '<li>O contato do seu concierge</li>',

# --- pacotes
'<h2 class="display">Packages</h2>': '<h2 class="display">Pacotes</h2>',
'One procedure, many ways to travel. Every package can add a partner or a family member.': 'Um procedimento, várias formas de viajar. Todo pacote pode incluir um acompanhante ou um familiar.',
'<h3>Solo Refresh</h3>': '<h3>Solo Refresh</h3>',
'<p>One patient, with procedure, concierge and trip.</p>': '<p>Um paciente, com procedimento, concierge e viagem.</p>',
'<h3>Couples Refresh</h3>': '<h3>Couples Refresh</h3>',
'<p>Two travelers, with one or more services.</p>': '<p>Dois viajantes, com um ou mais serviços.</p>',
'<h3>Family and Companion</h3>': '<h3>Família e acompanhante</h3>',
'<p>Patient with a companion.</p>': '<p>Paciente com acompanhante.</p>',
'<h3>Premium Refresh</h3>': '<h3>Premium Refresh</h3>',
'<p>Elevated hotel, transport, hospitality and concierge.</p>': '<p>Hotel, transporte, hospitalidade e concierge aprimorados.</p>',
'<h3>Luxury Refresh</h3>': '<h3>Luxury Refresh</h3>',
'<p>High end accommodation, private transport, premium dining and selected experiences.</p>': '<p>Hospedagem de alto padrão, transporte privativo, gastronomia premium e experiências selecionadas.</p>',
'<h3>Add a partner or family member</h3>': '<h3>Adicionar acompanhante ou familiar</h3>',
'<p>And, if they want, invite them to look into a treatment of their own.</p>': '<p>E, se a pessoa quiser, convidá-la a conhecer um tratamento também.</p>',

# --- tres produtos
'<h2 class="display">Three products, one experience</h2>': '<h2 class="display">Três produtos, uma experiência</h2>',
'Most people buy a procedure in one place and a trip in another, and spend the week holding the two together. Here they arrive as one thing.': 'A maioria compra o procedimento em um lugar e a viagem em outro, e passa a semana segurando os dois. Aqui os dois chegam como uma coisa só.',
'<h3>Medical</h3>': '<h3>Médico</h3>',
'<p>Controlled by the physician and the clinic, from eligibility to discharge.</p>': '<p>Controlado pelo médico e pela clínica, da elegibilidade à alta.</p>',
'<h3>Travel</h3>': '<h3>Viagem</h3>',
'<p>Brazil, flights, hotels, restaurants, destinations and experiences.</p>': '<p>Brasil, voos, hotéis, restaurantes, destinos e experiências.</p>',
'<h3>Concierge</h3>': '<h3>Concierge</h3>',
'<p>RefreshU coordinates everything around the journey, so you carry none of it.</p>': '<p>A RefreshU coordena tudo em volta da jornada, para você não carregar nada disso.</p>',
'You can save a significant amount and, at the same time, receive a great deal more than just the procedure. Do the treatment you have been considering, save meaningfully, and live Brazil, with one concierge coordinating the whole journey.': 'Você pode economizar um valor significativo e, ao mesmo tempo, receber muito mais do que apenas o procedimento. Faça o tratamento que você vem considerando, economize de forma relevante e viva o Brasil, com um único concierge coordenando a jornada inteira.',
'Physician, travel, concierge and value, inside a <em>single coordinated journey</em>.': 'Médico, viagem, concierge e valor, dentro de uma <em>única jornada coordenada</em>.',

# --- historia
'You were already considering the procedure.<br><em>What if the same budget, or even less, could give you more?</em>': 'Você já estava considerando o procedimento.<br><em>E se o mesmo orçamento, ou até menos, pudesse te dar mais?</em>',
'<li class="reveal">Exceptional care.</li>': '<li class="reveal">Cuidado excepcional.</li>',
'<li class="reveal">A personal concierge.</li>': '<li class="reveal">Um concierge pessoal.</li>',
'<li class="reveal">A trip through Brazil.</li>': '<li class="reveal">Uma viagem pelo Brasil.</li>',
'<li class="reveal">Good food.</li>': '<li class="reveal">Boa comida.</li>',
'<li class="reveal">Beautiful places.</li>': '<li class="reveal">Lugares bonitos.</li>',
'<li class="reveal">A memorable experience.</li>': '<li class="reveal">Uma experiência memorável.</li>',
'<li class="reveal">And savings that can genuinely matter.</li>': '<li class="reveal">E uma economia que pode realmente fazer diferença.</li>',
'The procedure and the trip should feel like <em>one experience</em>, not two separate purchases.': 'O procedimento e a viagem devem parecer <em>uma experiência só</em>, não duas compras separadas.',

# --- avaliacao
'<h2 class="display">Start My Evaluation</h2>': '<h2 class="display">Iniciar minha avaliação</h2>',
'<p>Six steps: your interest, the procedure, about you, a medical questionnaire approved by the physician, your photos, and submission for medical review.</p>': '<p>Seis etapas: seu interesse, o procedimento, sobre você, uma anamnese aprovada pelo médico, suas fotos e o envio para análise médica.</p>',
'Your information is submitted for physician review. RefreshU does not make clinical decisions and does not promise a clinical outcome.': 'Suas informações são enviadas para análise médica. A RefreshU não toma decisões clínicas e não promete resultado clínico.',

# --- FAQ
'<h2 class="display sec-head reveal">Questions people ask first</h2>': '<h2 class="display sec-head reveal">As perguntas que aparecem primeiro</h2>',
'<summary>Who decides whether I am a candidate?</summary>': '<summary>Quem decide se eu sou candidato?</summary>',
'<p>A participating physician does, after reviewing your questionnaire and photos. RefreshU coordinates the journey and never makes the medical decision.</p>': '<p>Um médico participante, depois de analisar seu questionário e suas fotos. A RefreshU coordena a jornada e nunca toma a decisão médica.</p>',
'<summary>Is this medical tourism?</summary>': '<summary>Isso é turismo médico?</summary>',
'<p>Not in the way that phrase is normally used. RefreshU is a concierge service built around a physician led journey, where the trip is designed rather than improvised.</p>': '<p>Não no sentido em que essa expressão costuma ser usada. A RefreshU é um serviço de concierge construído em torno de uma jornada conduzida por médico, em que a viagem é desenhada e não improvisada.</p>',
'<summary>How much will I save?</summary>': '<summary>Quanto eu vou economizar?</summary>',
'<p>It depends on the procedure and on what you compare it to. We publish comparisons only where the figures and the methodology can be verified and approved.</p>': '<p>Depende do procedimento e daquilo com que você compara. Só publicamos comparações quando os valores e a metodologia podem ser verificados e aprovados.</p>',
'<summary>Can someone travel with me?</summary>': '<summary>Alguém pode viajar comigo?</summary>',
'<p>Yes. Packages support a partner, a friend or family, and your companion can look into a treatment of their own if they want to.</p>': '<p>Pode. Os pacotes comportam companheiro, amigo ou família, e o acompanhante pode conhecer um tratamento próprio se quiser.</p>',
'<summary>What happens to my medical information?</summary>': '<summary>O que acontece com as minhas informações médicas?</summary>',
'<p>It is collected through a private questionnaire and sent for review by the physician handling your case.</p>': '<p>Elas são coletadas em um questionário privado e enviadas para análise do médico responsável pelo seu caso.</p>',
'<summary>What about travel insurance?</summary>': '<summary>E o seguro-viagem?</summary>',
'<p>Delays and cancellations can affect the medical schedule, and real coverage depends on each individual policy. RefreshU does not promise reimbursement.</p>': '<p>Atrasos e cancelamentos podem afetar o cronograma médico, e a cobertura real depende da apólice de cada pessoa. A RefreshU não promete reembolso.</p>',

# --- rodape
'aria-label="Footer"': 'aria-label="Rodapé"',
'<h3>Explore</h3>': '<h3>Explorar</h3>',
'<h3>RefreshU</h3>': '<h3>RefreshU</h3>',
'<h3>Account</h3>': '<h3>Conta</h3>',
'>The RefreshU Experience<': '>A experiência RefreshU<',
'>About<': '>Sobre<',
'RefreshU coordinates travel, hospitality and logistics around a medical journey. Participating physicians and clinics control eligibility, treatment plans and every clinical requirement. RefreshU does not practice medicine, does not make medical decisions and does not promise a clinical result.': 'A RefreshU coordena viagem, hospitalidade e logística em torno de uma jornada médica. Os médicos participantes e as clínicas controlam a elegibilidade, os planos de tratamento e todas as exigências clínicas. A RefreshU não pratica medicina, não toma decisões médicas e não promete resultado clínico.',
'Medical, legal, privacy, pricing, payment, insurance and marketing claims on this site are pending professional review and approval before launch.': 'Afirmações médicas, jurídicas, de privacidade, preço, pagamento, seguro e marketing deste site estão pendentes de revisão e aprovação profissional antes do lançamento.',
'<span>Photography used for design purposes, licensed for commercial use.</span>': '<span>Fotografia usada para fins de design, licenciada para uso comercial.</span>',

}

# --- entrada no portal ------------------------------------------------------
D.update({
'<title>Sign In · RefreshU</title>': '<title>Entrar · RefreshU</title>',
'Sign in to your RefreshU client portal: your journey, your trip, your schedule, your physician and your concierge in one place.': 'Entre no portal do cliente RefreshU: sua jornada, sua viagem, sua agenda, seu médico e seu concierge em um lugar só.',
'Everything about your journey, in one place.': 'Tudo sobre a sua jornada, em um lugar só.',
'<li>My Journey</li>': '<li>Minha jornada</li>',
'<li>My Trip</li>': '<li>Minha viagem</li>',
'<li>My Schedule</li>': '<li>Minha agenda</li>',
'<li>My Doctor</li>': '<li>Meu médico</li>',
'<li>My Requirements</li>': '<li>Minhas pendências</li>',
'<li>My Concierge</li>': '<li>Meu concierge</li>',
'<li>Explore Brazil</li>': '<li>Explorar o Brasil</li>',
'<li>Documents</li>': '<li>Documentos</li>',
'<li>Payments</li>': '<li>Pagamentos</li>',
'<li>Support</li>': '<li>Suporte</li>',
'>Back to refreshu.com<': '>Voltar para refreshu.com<',
'<h1 class="display auth__t">Welcome back</h1>': '<h1 class="display auth__t">Bem-vindo de volta</h1>',
'Pick your journey up where you left it.': 'Retome sua jornada de onde você parou.',
'<label for="email">Email</label>': '<label for="email">E-mail</label>',
'<label for="password">Password</label>': '<label for="password">Senha</label>',
'>Forgot your password?<': '>Esqueceu a senha?<',
'Enter the email you used in your evaluation.': 'Informe o e-mail que você usou na avaliação.',
'Enter your password.': 'Informe sua senha.',
'aria-label="Show password"': 'aria-label="Mostrar senha"',
'<span>Keep me signed in on this device</span>': '<span>Continuar conectado neste dispositivo</span>',
'id="signinBtn">Sign In<': 'id="signinBtn">Entrar<',
})

# --- portal -----------------------------------------------------------------
D.update({
'<title>My Journey · RefreshU</title>': '<title>Minha jornada · RefreshU</title>',
'<b>Demonstration.</b> Every name, date, clinic, hotel and document on these screens is sample data, created to show how the platform works.': '<b>Demonstração.</b> Todo nome, data, clínica, hotel e documento destas telas é dado de exemplo, criado para mostrar como a plataforma funciona.',
'aria-label="Portal">': 'aria-label="Portal">',
# rotulos do menu do portal
'<span class="pnav__lbl">My Journey</span>': '<span class="pnav__lbl">Minha jornada</span>',
'<span class="pnav__lbl">My Trip</span>': '<span class="pnav__lbl">Minha viagem</span>',
'<span class="pnav__lbl">My Schedule</span>': '<span class="pnav__lbl">Minha agenda</span>',
'<span class="pnav__lbl">My Doctor</span>': '<span class="pnav__lbl">Meu médico</span>',
'<span class="pnav__lbl">My Requirements</span>': '<span class="pnav__lbl">Minhas pendências</span>',
'<span class="pnav__lbl">My Concierge</span>': '<span class="pnav__lbl">Meu concierge</span>',
'<span class="pnav__lbl">Explore Brazil</span>': '<span class="pnav__lbl">Explorar o Brasil</span>',
'<span class="pnav__lbl">Documents</span>': '<span class="pnav__lbl">Documentos</span>',
'<span class="pnav__lbl">Payments</span>': '<span class="pnav__lbl">Pagamentos</span>',
'<span class="pnav__lbl">Support</span>': '<span class="pnav__lbl">Suporte</span>',
# subtitulos de cada tela
'data-sub="Tuesday, day 2 of 8 in São Paulo"': 'data-sub="Terça, dia 2 de 8 em São Paulo"',
'data-sub="São Paulo, March 9 to March 16"': 'data-sub="São Paulo, 9 a 16 de março"',
'data-sub="Your week, your travel, your physician and your concierge"': 'data-sub="Sua semana, sua viagem, seu médico e seu concierge"',
'data-sub="Consultation on Wednesday, March 11"': 'data-sub="Consulta na quarta, 11 de março"',
'data-sub="Two items need you"': 'data-sub="Dois itens dependem de você"',
'data-sub="Beatriz L., São Paulo"': 'data-sub="Beatriz L., São Paulo"',
'data-sub="Filtered by what your physician has cleared"': 'data-sub="Filtrado pelo que o seu médico liberou"',
'data-sub="Everything sent and everything issued"': 'data-sub="Tudo o que foi enviado e tudo o que foi emitido"',
'data-sub="Where each item of your journey stands"': 'data-sub="Em que pé está cada item da sua jornada"',
'data-sub="Who to talk to, and about what"': 'data-sub="Com quem falar, e sobre o quê"',
'<i>Solo Refresh, São Paulo</i>': '<i>Solo Refresh, São Paulo</i>',
'>Sign out<': '>Sair<',
'id="viewTitle">My Journey<': 'id="viewTitle">Minha jornada<',
'id="viewSub">Tuesday, day 2 of 8 in São Paulo<': 'id="viewSub">Terça, dia 2 de 8 em São Paulo<',
'>Contact My Concierge<': '>Falar com meu concierge<',
# trilho da jornada
'<span></span>Evaluation': '<span></span>Avaliação',
'<span></span>Medical review': '<span></span>Análise médica',
'<span></span>Concierge call': '<span></span>Contato do concierge',
'<span></span>Doctor consult': '<span></span>Consulta médica',
'<span></span>Confirmed': '<span></span>Confirmado',
'<span></span>Preparation': '<span></span>Preparação',
'<span></span>In Brazil': '<span></span>No Brasil',
'<span></span>Procedure': '<span></span>Procedimento',
'<span></span>Recovery': '<span></span>Recuperação',
'<span></span>Experience': '<span></span>Experiência',
'<span></span>Home': '<span></span>Volta para casa',
# cartoes do painel
'<h2>Where am I</h2>': '<h2>Em que etapa estou</h2>',
'<p class="q__big">In Brazil</p>': '<p class="q__big">No Brasil</p>',
'<p>You arrived yesterday. Your pre operative process runs today and tomorrow.</p>': '<p>Você chegou ontem. Seu processo pré-operatório acontece hoje e amanhã.</p>',
'<h2>What is next</h2>': '<h2>Qual é a próxima</h2>',
'<p class="q__big">Pre operative blood work</p>': '<p class="q__big">Exames de sangue pré-operatórios</p>',
'<p>Today at 10:00, at the hotel. Your driver is confirmed for 09:00.</p>': '<p>Hoje às 10h, no hotel. Seu motorista está confirmado para as 9h.</p>',
'<h2>What you need to do</h2>': '<h2>O que você precisa fazer</h2>',
'<p class="q__big">Send your lab results</p>': '<p class="q__big">Enviar os resultados dos exames</p>',
'<p>Dr. Camila Rocha asked for the results before tomorrow&rsquo;s consultation.</p>': '<p>A Dra. Camila Rocha pediu os resultados antes da consulta de amanhã.</p>',
'>Go to my requirements<': '>Ir para minhas pendências<',
'<h2>Who you talk to</h2>': '<h2>Com quem você fala</h2>',
'<p>Your concierge in São Paulo, available from 07:00 to 22:00 local time.</p>': '<p>Sua concierge em São Paulo, disponível das 7h às 22h no horário local.</p>',
'>Message Beatriz<': '>Falar com a Beatriz<',
'<h2 class="card__t">Today in Brazil</h2>': '<h2 class="card__t">Hoje no Brasil</h2>',
'<b>09:00</b><span>Driver at the hotel lobby</span>': '<b>09:00</b><span>Motorista no lobby do hotel</span>',
'<b>10:00</b><span>Pre operative blood work</span>': '<b>10:00</b><span>Exames de sangue pré-operatórios</span>',
'<b>12:30</b><span>Lunch reservation, Jardins</span>': '<b>12:30</b><span>Reserva para o almoço, Jardins</span>',
'<b>15:00</b><span>Walk through Jardins, cleared by your physician</span>': '<b>15:00</b><span>Passeio pelos Jardins, liberado pelo seu médico</span>',
'<b>19:30</b><span>Dinner reservation</span>': '<b>19:30</b><span>Reserva para o jantar</span>',
'<h2 class="card__t">Next medical action</h2>': '<h2 class="card__t">Próxima ação médica</h2>',
'<p class="card__big">Send your laboratory results</p>': '<p class="card__big">Enviar os resultados laboratoriais</p>',
'<p class="card__p">Upload the results as soon as the laboratory releases them. Your physician reviews them before the consultation.</p>': '<p class="card__p">Suba os resultados assim que o laboratório liberar. Seu médico analisa antes da consulta.</p>',
'>Upload results<': '>Enviar resultados<',
'<h2 class="card__t">Need anything</h2>': '<h2 class="card__t">Precisa de alguma coisa</h2>',
'<p class="card__p">A restaurant, a pharmacy item your physician prescribed, laundry, a driver, or just a question about tomorrow.</p>': '<p class="card__p">Um restaurante, um item de farmácia que seu médico prescreveu, lavanderia, um motorista, ou só uma dúvida sobre amanhã.</p>',
'>Talk to your RefreshU concierge<': '>Falar com seu concierge RefreshU<',
# minha viagem
'Your medical and travel information in one itinerary, so you do not need five apps, twenty emails and a spreadsheet.': 'Suas informações médicas e de viagem em um roteiro só, para você não precisar de cinco aplicativos, vinte e-mails e uma planilha.',
'<h2 class="card__t">Arrival flight</h2>': '<h2 class="card__t">Voo de chegada</h2>',
'<p class="card__big">Mon, March 9</p>': '<p class="card__big">Seg, 9 de março</p>',
'<p class="card__p">Landing at GRU, 06:40 local time. Confirmation on file.</p>': '<p class="card__p">Pouso em GRU, 6h40 no horário local. Confirmação registrada.</p>',
'<h2 class="card__t">Hotel</h2>': '<h2 class="card__t">Hotel</h2>',
'<p class="card__p">Check in Mon, March 9. Check out Mon, March 16. Recovery friendly room, high floor, quiet side.</p>': '<p class="card__p">Check-in seg, 9 de março. Check-out seg, 16 de março. Quarto adequado à recuperação, andar alto, lado silencioso.</p>',
'<h2 class="card__t">Transport</h2>': '<h2 class="card__t">Transporte</h2>',
'<p class="card__big">Private driver</p>': '<p class="card__big">Motorista particular</p>',
'<p class="card__p">Airport transfer, hotel, clinic and every appointment on your schedule.</p>': '<p class="card__p">Transfer do aeroporto, hotel, clínica e todo compromisso da sua agenda.</p>',
'<h2 class="card__t">Consultations</h2>': '<h2 class="card__t">Consultas</h2>',
'<p class="card__big">Wed, March 11, 14:00</p>': '<p class="card__big">Qua, 11 de março, 14h</p>',
'<p class="card__p">Clínica Vértice, Itaim Bibi. With Dr. Camila Rocha.</p>': '<p class="card__p">Clínica Vértice, Itaim Bibi. Com a Dra. Camila Rocha.</p>',
'<h2 class="card__t">Procedure</h2>': '<h2 class="card__t">Procedimento</h2>',
'<p class="card__big">Thu, March 12</p>': '<p class="card__big">Qui, 12 de março</p>',
'<p class="card__p">FUE hair transplant. Arrival 07:00. Driver confirmed. Return to the hotel the same day.</p>': '<p class="card__p">Transplante capilar FUE. Chegada às 7h. Motorista confirmado. Retorno ao hotel no mesmo dia.</p>',
'<h2 class="card__t">Recovery days</h2>': '<h2 class="card__t">Dias de recuperação</h2>',
'<p class="card__big">Fri 13 and Sat 14</p>': '<p class="card__big">Sex 13 e sáb 14</p>',
'<p class="card__p">Rest at the hotel with meal delivery, then activities as your physician clears them.</p>': '<p class="card__p">Descanso no hotel com entrega de refeições, depois atividades conforme a liberação do seu médico.</p>',
'<h2 class="card__t">Restaurants</h2>': '<h2 class="card__t">Restaurantes</h2>',
'<p class="card__big">3 reservations</p>': '<p class="card__big">3 reservas</p>',
'<p class="card__p">Tue dinner, Sat lunch and Sun dinner, all chosen around what you can eat on each day.</p>': '<p class="card__p">Jantar de terça, almoço de sábado e jantar de domingo, todos escolhidos pelo que você pode comer em cada dia.</p>',
'<h2 class="card__t">Experiences</h2>': '<h2 class="card__t">Experiências</h2>',
'<p class="card__big">2 booked</p>': '<p class="card__big">2 reservadas</p>',
'<p class="card__p">A walk through Jardins today and a museum visit on Sunday, both recovery compatible.</p>': '<p class="card__p">Um passeio pelos Jardins hoje e uma visita a museu no domingo, os dois compatíveis com a recuperação.</p>',
'<h2 class="card__t">Return flight</h2>': '<h2 class="card__t">Voo de volta</h2>',
'<p class="card__big">Mon, March 16</p>': '<p class="card__big">Seg, 16 de março</p>',
'<p class="card__p">Departure 22:10 from GRU. Driver confirmed for 18:30.</p>': '<p class="card__p">Partida às 22h10 de GRU. Motorista confirmado para as 18h30.</p>',
# agenda
'One timeline holding four schedules together: yours, your travel, your physician and clinical team, and your concierge. Gaps are left on purpose, for delays and for whatever your physician requires.': 'Uma linha do tempo reunindo quatro agendas: a sua, a da viagem, a do médico e da equipe clínica, e a do concierge. As folgas ficam de propósito, para atrasos e para o que o seu médico exigir.',
'<i class="k k--you"></i>You': '<i class="k k--you"></i>Você',
'<i class="k k--trav"></i>Travel': '<i class="k k--trav"></i>Viagem',
'<i class="k k--med"></i>Physician and clinic': '<i class="k k--med"></i>Médico e clínica',
'<i class="k k--conc"></i>Concierge': '<i class="k k--conc"></i>Concierge',
'<b>Monday</b><i>March 9</i>': '<b>Segunda</b><i>9 de março</i>',
'<b>Tuesday</b><i>March 10</i>': '<b>Terça</b><i>10 de março</i>',
'<b>Wednesday</b><i>March 11</i>': '<b>Quarta</b><i>11 de março</i>',
'<b>Thursday</b><i>March 12</i>': '<b>Quinta</b><i>12 de março</i>',
'<b>Friday</b><i>March 13</i>': '<b>Sexta</b><i>13 de março</i>',
'<b>Saturday</b><i>March 14</i>': '<b>Sábado</b><i>14 de março</i>',
'<b>Sunday</b><i>March 15</i>': '<b>Domingo</b><i>15 de março</i>',
'<b>Monday</b><i>March 16</i>': '<b>Segunda</b><i>16 de março</i>',
'>06:40 Arrival at GRU<': '>06h40 Chegada em GRU<',
'>08:00 Airport transfer<': '>08h00 Transfer do aeroporto<',
'>10:00 Hotel check in and welcome kit<': '>10h00 Check-in no hotel e kit de boas-vindas<',
'>20:00 Dinner reservation<': '>20h00 Reserva para o jantar<',
'>09:00 Driver<': '>09h00 Motorista<',
'>10:00 Pre operative blood work<': '>10h00 Exames de sangue pré-operatórios<',
'>12:30 Lunch<': '>12h30 Almoço<',
'>15:00 Jardins<': '>15h00 Jardins<',
'>19:30 Dinner<': '>19h30 Jantar<',
'>14:00 Consultation with Dr. Camila Rocha<': '>14h00 Consulta com a Dra. Camila Rocha<',
'>15:30 Recovery preparation and guidance<': '>15h30 Preparo para a recuperação e orientações<',
'>Free afternoon, kept quiet on purpose<': '>Tarde livre, mantida tranquila de propósito<',
'>06:15 Driver<': '>06h15 Motorista<',
'>07:00 Procedure, Clínica Vértice<': '>07h00 Procedimento, Clínica Vértice<',
'>Return to the hotel<': '>Retorno ao hotel<',
'>Recovery support and meal delivery<': '>Suporte de recuperação e entrega de refeições<',
'>11:00 Follow up with your physician<': '>11h00 Retorno com o seu médico<',
'>Recovery at the hotel, meals delivered<': '>Recuperação no hotel, refeições entregues<',
'>Activities released by your physician<': '>Atividades liberadas pelo seu médico<',
'>13:00 Lunch reservation<': '>13h00 Reserva para o almoço<',
'>A calm day in São Paulo<': '>Um dia calmo em São Paulo<',
'>11:00 Museum visit<': '>11h00 Visita a museu<',
'>19:30 Dinner reservation<': '>19h30 Reserva para o jantar<',
'>09:00 Final check with your physician<': '>09h00 Checagem final com o seu médico<',
'>18:30 Driver to the airport<': '>18h30 Motorista para o aeroporto<',
'>22:10 Return flight<': '>22h10 Voo de volta<',
# medico
'<p class="doc__s">Hair restoration and FUE transplant</p>': '<p class="doc__s">Restauração capilar e transplante FUE</p>',
'<p class="doc__c">Clínica Vértice, Itaim Bibi, São Paulo</p>': '<p class="doc__c">Clínica Vértice, Itaim Bibi, São Paulo</p>',
'<dt>Credentials</dt><dd>Sample credential record</dd>': '<dt>Credenciais</dt><dd>Registro de credencial de exemplo</dd>',
'<dt>Years of experience</dt><dd>18</dd>': '<dt>Anos de experiência</dt><dd>18</dd>',
'<dt>Languages spoken</dt><dd>Portuguese, English, Spanish</dd>': '<dt>Idiomas</dt><dd>Português, inglês, espanhol</dd>',
'<dt>Procedures performed</dt><dd>FUE transplant, hair restoration</dd>': '<dt>Procedimentos realizados</dt><dd>Transplante FUE, restauração capilar</dd>',
'<dt>International patients</dt><dd>Attends patients from the United States weekly</dd>': '<dt>Pacientes internacionais</dt><dd>Atende pacientes dos Estados Unidos toda semana</dd>',
'<dt>Your consultation</dt><dd>Wednesday, March 11, 14:00</dd>': '<dt>Sua consulta</dt><dd>Quarta, 11 de março, 14h</dd>',
'<h3>Approach</h3>': '<h3>Abordagem</h3>',
'Sample biography. In the live platform this is the physician&rsquo;s own text, describing how they work, what they will and will not recommend, and what they expect from a patient travelling from abroad.': 'Biografia de exemplo. Na plataforma real este é o texto do próprio médico, descrevendo como trabalha, o que recomenda e o que não recomenda, e o que espera de um paciente que vem de fora.',
'<h3>Before and after</h3>': '<h3>Antes e depois</h3>',
'The gallery appears here once the physician contract authorises the use of professional and patient content.': 'A galeria aparece aqui assim que o contrato com o médico autorizar o uso de conteúdo do profissional e dos pacientes.',
'The physician decides eligibility, the treatment plan, the risks, the exams and every clinical instruction. RefreshU coordinates the logistics around those decisions and does not take part in them.': 'O médico decide a elegibilidade, o plano de tratamento, os riscos, os exames e toda orientação clínica. A RefreshU coordena a logística em torno dessas decisões e não participa delas.',
# pendencias
'<b>Action needed:</b> your physician requires your laboratory results before the consultation on Wednesday, March 11.': '<b>Ação necessária:</b> seu médico precisa dos resultados laboratoriais antes da consulta de quarta, 11 de março.',
'RefreshU handles the logistics. Your physician and the clinic control every clinical requirement on this list.': 'A RefreshU cuida da logística. Seu médico e a clínica controlam todas as exigências clínicas desta lista.',
'<b>Medical questionnaire</b><span>Submitted and reviewed</span>': '<b>Questionário médico</b><span>Enviado e analisado</span>',
'<b>Flight itinerary</b><span>Confirmed both ways</span>': '<b>Itinerário de voo</b><span>Confirmado nos dois trechos</span>',
'<b>Travel insurance documentation</b><span>Received</span>': '<b>Documentação de seguro-viagem</b><span>Recebida</span>',
'<b>Hotel</b><span>Confirmed, March 9 to March 16</span>': '<b>Hotel</b><span>Confirmado, 9 a 16 de março</span>',
'<b>Transport</b><span>Private driver for every appointment</span>': '<b>Transporte</b><span>Motorista particular para todo compromisso</span>',
'<b>Blood work required by your physician</b><span>Collection today at 10:00, results pending</span>': '<b>Exames de sangue exigidos pelo seu médico</b><span>Coleta hoje às 10h, resultados pendentes</span>',
'<b>Payments</b><span>One item due before the procedure</span>': '<b>Pagamentos</b><span>Um item a vencer antes do procedimento</span>',
'<b>Cardiac exams</b><span>Not required for your case</span>': '<b>Exames cardíacos</b><span>Não exigidos no seu caso</span>',
'<b>Medical consultation</b><span>Wednesday, March 11, 14:00</span>': '<b>Consulta médica</b><span>Quarta, 11 de março, 14h</span>',
'<b>Physician instructions</b><span>Released after the consultation</span>': '<b>Orientações do médico</b><span>Liberadas depois da consulta</span>',
'<b>Medical documents</b><span>Issued by the clinic after the procedure</span>': '<b>Documentos médicos</b><span>Emitidos pela clínica depois do procedimento</span>',
# concierge do portal
'<p class="card__p">Your concierge in São Paulo. Available 07:00 to 22:00 local time, and reachable at any hour for anything urgent.</p>': '<p class="card__p">Sua concierge em São Paulo. Disponível das 7h às 22h no horário local, e acessível a qualquer hora para o que for urgente.</p>',
'>Send a message<': '>Enviar mensagem<',
'>Request a call<': '>Pedir uma ligação<',
'<p class="card__p">Airport transfer, hotel, clinic and a private driver for anything on your schedule.</p>': '<p class="card__p">Transfer do aeroporto, hotel, clínica e motorista particular para qualquer item da sua agenda.</p>',
'<p class="card__p">Recommendations, reservations and meal delivery on the days you should be resting.</p>': '<p class="card__p">Recomendações, reservas e entrega de refeições nos dias em que você deve descansar.</p>',
'<p class="card__p">Restaurants, shopping, museums, tours and local attractions, filtered by what your recovery allows.</p>': '<p class="card__p">Restaurantes, compras, museus, passeios e atrações locais, filtrados pelo que a sua recuperação permite.</p>',
'<p class="card__p">Barber, hairdresser, nails, lashes and approved wellness professionals.</p>': '<p class="card__p">Barbeiro, cabeleireiro, unhas, cílios e profissionais de bem-estar aprovados.</p>',
'<p class="card__p">Laundry, shopping, clothing and pharmacy support for items your physician prescribed.</p>': '<p class="card__p">Lavanderia, compras, roupas e apoio na farmácia para itens prescritos pelo seu médico.</p>',
'<p class="card__p">Qualified professionals where appropriate, services approved by your physician, and transport for the return.</p>': '<p class="card__p">Profissionais qualificados quando apropriado, serviços aprovados pelo seu médico e transporte para o retorno.</p>',
'<h2 class="card__t">Personal care</h2>': '<h2 class="card__t">Cuidado pessoal</h2>',
'<h2 class="card__t">Convenience</h2>': '<h2 class="card__t">Conveniência</h2>',
'<h2 class="card__t">Recovery support</h2>': '<h2 class="card__t">Suporte de recuperação</h2>',
'<h2 class="card__t">Dining</h2>': '<h2 class="card__t">Alimentação</h2>',
'<h2 class="card__t">Medical services at the hotel</h2>': '<h2 class="card__t">Serviços médicos no hotel</h2>',
'<p class="card__p">Where it is legally permitted and requested by your physician, qualified professionals attend you at the hotel: blood collection, laboratory services, basic exams, an electrocardiogram when properly provided, a nursing visit and physician approved recovery support.</p>': '<p class="card__p">Onde for legalmente permitido e solicitado pelo seu médico, profissionais qualificados atendem você no hotel: coleta de sangue, serviços laboratoriais, exames básicos, eletrocardiograma quando prestado de forma adequada, visita de enfermagem e suporte de recuperação aprovado pelo médico.</p>',
'<p class="card__p"><b>Your pre operative testing</b> is scheduled at the hotel today at 10:00.</p>': '<p class="card__p"><b>Seus exames pré-operatórios</b> estão agendados no hotel hoje às 10h.</p>',
# explorar o brasil
'Everything here is filtered by what your physician has cleared for the day you are on. Options open up as your recovery advances.': 'Tudo aqui é filtrado pelo que o seu médico liberou para o dia em que você está. As opções vão abrindo conforme a recuperação avança.',
'<h3>Restaurants</h3>': '<h3>Restaurantes</h3>',
'<p>From the everyday to the reservation you will tell people about.</p>': '<p>Do dia a dia à reserva que você vai contar para os outros.</p>',
'<h3>Parks and neighborhoods</h3>': '<h3>Parques e bairros</h3>',
'<p>Jardins, Ibirapuera and a slow walk that fits your week.</p>': '<p>Jardins, Ibirapuera e uma caminhada tranquila que cabe na sua semana.</p>',
'<h3>Museums and culture</h3>': '<h3>Museus e cultura</h3>',
'<p>Architecture, art and the parts of the city worth the detour.</p>': '<p>Arquitetura, arte e as partes da cidade que valem o desvio.</p>',
'<h3>Shopping</h3>': '<h3>Compras</h3>',
'<p>Districts and stores, with a driver waiting.</p>': '<p>Bairros e lojas, com um motorista esperando.</p>',
'<h3>Wellness</h3>': '<h3>Bem-estar</h3>',
'<p>Approved professionals, once your physician releases it.</p>': '<p>Profissionais aprovados, assim que o seu médico liberar.</p>',
'<h3>Day trips</h3>': '<h3>Bate-voltas</h3>',
'<p>The coast, for the end of the stay if you are cleared to travel.</p>': '<p>O litoral, para o fim da estadia se você estiver liberado para viajar.</p>',
'>Cleared today<': '>Liberado hoje<',
'>Opens Saturday<': '>Abre no sábado<',
'>Pending physician release<': '>Aguardando liberação médica<',
# documentos
'Everything you sent and everything issued to you, in one place.': 'Tudo o que você enviou e tudo o que foi emitido para você, em um lugar só.',
'<caption class="sr">Your documents</caption>': '<caption class="sr">Seus documentos</caption>',
'<th scope="col">Document</th><th scope="col">Added</th><th scope="col">Status</th>': '<th scope="col">Documento</th><th scope="col">Adicionado</th><th scope="col">Situação</th>',
'<th scope="row">Medical questionnaire</th>': '<th scope="row">Questionário médico</th>',
'<th scope="row">Photographs for evaluation</th>': '<th scope="row">Fotos para avaliação</th>',
'<th scope="row">Flight itinerary</th>': '<th scope="row">Itinerário de voo</th>',
'<th scope="row">Travel insurance</th>': '<th scope="row">Seguro-viagem</th>',
'<th scope="row">Hotel confirmation</th>': '<th scope="row">Confirmação do hotel</th>',
'<th scope="row">Laboratory results</th>': '<th scope="row">Resultados laboratoriais</th>',
'<th scope="row">Physician instructions</th>': '<th scope="row">Orientações do médico</th>',
'<th scope="row">Medical report</th>': '<th scope="row">Relatório médico</th>',
'<td>February 12</td>': '<td>12 de fevereiro</td>',
'<td>February 24</td>': '<td>24 de fevereiro</td>',
'<td>February 27</td>': '<td>27 de fevereiro</td>',
'<td>February 20</td>': '<td>20 de fevereiro</td>',
'<td>March 1</td>': '<td>1 de março</td>',
'<td>March 9</td>': '<td>9 de março</td>',
'<td>March 11</td>': '<td>11 de março</td>',
'<td>Waiting</td>': '<td>Aguardando</td>',
'<td>On request</td>': '<td>Sob demanda</td>',
'>Reviewed<': '>Analisado<',
'>Confirmed<': '>Confirmado<',
'>Received<': '>Recebido<',
'>Upload pending<': '>Envio pendente<',
'>After consultation<': '>Depois da consulta<',
'>After procedure<': '>Depois do procedimento<',
# pagamentos
'Every item of your journey and where it stands. Amounts appear here once pricing is approved for publication.': 'Cada item da sua jornada e em que pé está. Os valores aparecem aqui assim que o preço for aprovado para publicação.',
'<caption class="sr">Your payments</caption>': '<caption class="sr">Seus pagamentos</caption>',
'<th scope="col">Item</th><th scope="col">Due</th><th scope="col">Status</th>': '<th scope="col">Item</th><th scope="col">Vencimento</th><th scope="col">Situação</th>',
'<th scope="row">Reservation deposit</th>': '<th scope="row">Depósito de reserva</th>',
'<th scope="row">Concierge and travel coordination</th>': '<th scope="row">Concierge e coordenação de viagem</th>',
'<th scope="row">Hotel</th>': '<th scope="row">Hotel</th>',
'<th scope="row">Procedure balance</th>': '<th scope="row">Saldo do procedimento</th>',
'<th scope="row">Additional experiences</th>': '<th scope="row">Experiências adicionais</th>',
'>Paid<': '>Pago<',
'>Due before the procedure<': '>A vencer antes do procedimento<',
'>Nothing pending<': '>Nada pendente<',
'Payment handling, receipts and the security measures around them are part of the platform build and are not represented on this demonstration screen.': 'O processamento de pagamento, os recibos e as medidas de segurança em volta fazem parte da construção da plataforma e não estão representados nesta tela de demonstração.',
# suporte
'<h2 class="card__t">Your concierge, first</h2>': '<h2 class="card__t">Seu concierge, primeiro</h2>',
'<p class="card__p">For anything about your trip, your schedule, transport, food, bookings or day to day needs. 07:00 to 22:00 local time.</p>': '<p class="card__p">Para qualquer coisa sobre a viagem, a agenda, transporte, comida, reservas ou necessidades do dia a dia. Das 7h às 22h no horário local.</p>',
'<h2 class="card__t">Clinical questions</h2>': '<h2 class="card__t">Dúvidas clínicas</h2>',
'<p class="card__p">Anything clinical goes to Dr. Camila Rocha and the clinical team. Your concierge routes it and never answers it.</p>': '<p class="card__p">Toda questão clínica vai para a Dra. Camila Rocha e a equipe clínica. Seu concierge encaminha e nunca responde.</p>',
'<h2 class="card__t">Urgent, outside hours</h2>': '<h2 class="card__t">Urgente, fora do horário</h2>',
'<p class="card__p">A line that reaches a person at any hour, for anything that cannot wait until morning.</p>': '<p class="card__p">Uma linha que alcança uma pessoa a qualquer hora, para o que não pode esperar até de manhã.</p>',
'<h2 class="card__t">Account and payments</h2>': '<h2 class="card__t">Conta e pagamentos</h2>',
'<p class="card__p">Billing, documents and access to this portal.</p>': '<p class="card__p">Cobrança, documentos e acesso a este portal.</p>',
'aria-label="Open menu" aria-expanded="false" aria-controls="pside"': 'aria-label="Abrir menu" aria-expanded="false" aria-controls="pside"',
})

# ---------------------------------------------------------------------------
def traduzir(html, arquivo):
    faltando = []
    # do trecho mais longo para o mais curto: evita que uma chave curta
    # estrague uma frase longa que ainda nao foi traduzida
    for en in sorted(D, key=len, reverse=True):
        if en in html:
            html = html.replace(en, D[en])
        else:
            faltando.append(en)

    # caminhos: /pt/ esta um nivel abaixo da raiz
    html = html.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    html = html.replace('srcset="assets/', 'srcset="../assets/')

    # Paginas que existem so na raiz. A Plataforma e apenas em ingles pelo
    # Anexo A.2, e um segundo idioma esta no Anexo D, fora do escopo. Entao
    # o /pt/ aponta para a versao em ingles em vez de gerar um 404.
    for so_raiz in ('assessment.html', 'console.html', 'sales.html',
                    'signin-team.html', 'signin-sales.html',
                    'signup.html', 'recover.html'):
        html = html.replace('href="%s"' % so_raiz, 'href="../%s"' % so_raiz)

    # idioma do documento e alternativas
    html = html.replace('<html lang="en">', '<html lang="pt-BR">')
    # troca do idioma ativo nas bandeiras, valendo para qualquer pagina
    # index.html vira "../" e "./" para nao passar por redirecionamento do host
    def en_link(m):
        alvo = '../' if m.group(1) == 'index.html' else '../' + m.group(1)
        return f'<a class="lang__b" href="{alvo}" hreflang="en"'
    html = re.sub(r'<a class="lang__b is-on" href="([\w.-]+)" hreflang="en" aria-current="page"', en_link, html)

    def pt_link(m):
        alvo = m.group(1) or './'
        return f'<a class="lang__b is-on" href="{alvo}" hreflang="pt-BR" aria-current="page"'
    html = re.sub(r'<a class="lang__b" href="pt/([\w.-]*)" hreflang="pt-BR"', pt_link, html)
    return html, faltando


def main():
    if os.path.isdir(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)

    total_faltando = set(D)
    for nome in PAGINAS:
        origem = os.path.join(RAIZ, nome)
        if not os.path.exists(origem):
            print('  falta o arquivo', nome); continue
        html = open(origem, encoding='utf-8').read()
        saida, faltando = traduzir(html, nome)
        open(os.path.join(DEST, nome), 'w', encoding='utf-8').write(saida)
        total_faltando &= set(faltando)
        print(f'  pt/{nome} gerado')

    if total_faltando:
        print('\n  chaves que nao casaram em nenhum arquivo (dicionario desatualizado?):')
        for k in sorted(total_faltando):
            print('   ·', k[:88])
    else:
        print('\n  todas as chaves do dicionario foram aplicadas')

if __name__ == '__main__':
    main()
