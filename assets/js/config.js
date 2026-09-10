/* ==========================================================================
   RefreshU · configuracao de ambiente

   Um arquivo so, carregado antes dos outros, para o que muda entre ambientes
   ou depende de uma conta externa. Nada aqui e segredo: sao valores publicos
   que o navegador ve de qualquer jeito.
   ========================================================================== */

window.REFRESHU_CONFIG = {

  /* Pagina de agendamento da RefreshU. Hoje e o Cal.com; o campo aceita
     tambem um "appointment schedule" do Google Calendar, e trocar de um para
     o outro e trocar esta linha.

     Por que Cal.com e nao Google: na conta gratuita do Google o agendamento
     existe mas NAO manda lembrete para quem marcou, e a call e com alguem em
     outro fuso, marcada com 12h ou mais de antecedencia. Sem lembrete, o
     no-show sobe. O Cal.com manda no plano gratuito.

     Notas do Google, para o dia em que a RefreshU assinar o Workspace:
     Como gerar, na conta que vai receber as calls:

       Google Calendar > Create > Appointment schedule
       define duracao, disponibilidade e antecedencia minima
       em "Booking form", marca nome, e-mail e telefone como campos pedidos
       Share > Copy link

     O proprio Google manda a confirmacao por e-mail para a cliente e para a
     conta do calendario, cria o evento nos dois calendarios e envia o
     lembrete. Nao ha nada a construir do nosso lado, e por isso esta etapa
     funciona hoje, sem backend.

     Aceita as duas formas de link:
       https://calendar.app.google/XXXXXXXXXXXX
       https://calendar.google.com/calendar/appointments/schedules/XXXX?gv=true

     Enquanto estiver vazio, a tela avisa que o agendamento ainda nao foi
     ligado, em vez de mostrar um quadro em branco. */
  /* O link curto (calendar.app.google/sQi3JYZiqBQpae8A7) redireciona para
     este. Usamos o longo de proposito: e o unico que aceita ?gv=true, o
     parametro que abre a agenda ja embutida, sem o cabecalho do Google. */
  bookingUrl: 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ0XKHslykIGRzyZdcm-Wrr2cBNXVhBkcDYLRHGN8VjSW3NRkT_qhC_8e5Qjus2SoH3XQgUjluki',

  /* Para onde a cliente escreve se o agendamento nao abrir. Sai do Legal
     Center quando a entidade legal e os e-mails oficiais forem definidos. */
  bookingFallbackEmail: 'info@werefreshyou.com',

  /* Os medicos participantes. Cada um tem o proprio site, e e la que vive
     tudo o que e clinico: questionario, fotos, exames e laudos. A plataforma
     da RefreshU nunca recebe esse material, so o retorno de que a etapa
     esta cumprida.

     'site' e para onde o portal manda a cliente quando o assunto e clinico.
     'social' aparece no perfil dela dentro do portal; deixe de fora a rede
     que ela nao usa, em vez de publicar um link vazio.

     Nada aqui vai ao ar sem a autorizacao assinada da medica: e a pendencia
     numero 2 do Anexo C. */
  physicians: {
    'juliana-buttros': {
      name: 'Dr. Juliana Buttros',
      site: '',                       // ex.: 'https://julianabuttros.com.br'
      social: {
        instagram: '',                // ex.: 'https://instagram.com/...'
        tiktok: '',
        youtube: '',
        linkedin: ''
      },
      /* Antes e depois. Cada caso precisa de imagem aprovada pela medica E da
         permissao documentada da paciente. Enquanto a lista estiver vazia, o
         portal mostra o aviso de "nao publicado" no lugar da galeria, que e o
         comportamento correto e nao um placeholder. */
      beforeAfter: []
      // ex.: [{ before:'assets/img/ba/01-antes.webp', after:'assets/img/ba/01-depois.webp',
      //         caption:'FUE, 2.400 grafts, 12 months', consent:'2026-03-04' }]
    }
  }
};
