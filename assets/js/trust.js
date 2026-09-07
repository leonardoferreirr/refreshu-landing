/* ============================================================
   Sinais de confianca
   Regra do roadmap: um selo so aparece depois de conquistado, e
   um vencido some sozinho. Por isso a lista e dados com status e
   validade, e nao HTML escrito a mao. O admin edita esta lista
   pela tela de conteudo do console; nada aqui e decorativo.

   status: 'active'  aparece
           'pending' nao aparece no site, aparece no console
           'expired' nao aparece, e sai sozinho pela data
   ============================================================ */
(function () {
  'use strict';

  var CREDENTIALS = [
    {
      name: 'Independent physician model',
      status: 'active',
      body: 'Medical decisions stay with licensed independent providers. RefreshU coordinates the journey and does not practise medicine.',
      href: 'legal.html#providers'
    },
    {
      name: 'Encrypted connection',
      status: 'active',
      body: 'The whole site and the client portal are served over HTTPS, with secure cookies and no mixed content.',
      href: 'legal.html#cookies'
    },
    {
      name: 'Secure client portal',
      status: 'active',
      body: 'Role-based access, session expiry, optional two-step sign in for clients and required two-step sign in for the RefreshU team.',
      href: 'legal.html#privacy'
    },
    {
      name: 'Published legal terms',
      status: 'active',
      body: 'Terms, privacy, medical disclaimer, provider disclosure, concierge agreement, cancellation, travel and insurance, each versioned and dated.',
      href: 'legal.html'
    },
    {
      name: 'Documented complaint route',
      status: 'active',
      body: 'Every concern receives a case number and an audit trail, and honest reviews are never penalised.',
      href: 'legal.html#concern'
    },
    {
      name: 'Verified provider process',
      status: 'active',
      body: 'Credentials, registration numbers and society memberships are checked with the physician before a profile is published.',
      href: 'legal.html#providers'
    },

    /* ---- ainda nao conquistados: ficam fora do site de proposito ---- */
    {
      name: 'GHA Medical Travel Facilitator Certification',
      status: 'pending',
      issuer: 'Global Healthcare Accreditation',
      verify: 'https://www.globalhealthcareaccreditation.com/medical-travel-facilitator-certification',
      body: 'Highest-priority industry certification. Fifteen programme elements, a verification interview and staff training. Not displayed until it is earned.'
    },
    {
      name: 'Trustpilot',
      status: 'pending',
      issuer: 'Trustpilot',
      verify: 'https://business.trustpilot.com/',
      body: 'Live rating only, through the approved integration. Never a typed number, never bought or gated reviews.'
    },
    {
      name: 'Google Business Profile',
      status: 'pending',
      issuer: 'Google',
      body: 'Built alongside Trustpilot, with genuine reviews and no review gating.'
    },
    {
      name: 'DMCA Protection',
      status: 'pending',
      issuer: 'DMCA.com',
      verify: 'https://www.dmca.com/Badges.aspx',
      body: 'Content-ownership signal for original RefreshU copy and guides. Not a healthcare or security certification.'
    },
    {
      name: 'Professional and cyber coverage',
      status: 'pending',
      body: 'Displayed only with wording approved by the insurance broker and counsel.'
    }
  ];

  // O console lê esta mesma lista, para que site e console nunca divirjam
  // sobre o que já foi conquistado.
  window.RU_CREDENTIALS = CREDENTIALS;

  var grid = document.getElementById('trustGrid');
  if (!grid) return;

  var today = new Date();

  function live(c) {
    if (c.status !== 'active') return false;
    if (c.expires && new Date(c.expires) < today) return false;   // vencido sai sozinho
    return true;
  }

  var shown = CREDENTIALS.filter(live);
  if (!shown.length) { grid.closest('section').hidden = true; return; }

  grid.innerHTML = shown.map(function (c) {
    var inner =
      '<span class="tr__i" aria-hidden="true">' +
        '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3.2 5 6v5.3c0 4.1 2.9 7.9 7 9.2 4.1-1.3 7-5.1 7-9.2V6l-7-2.8Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="m9 12 2.2 2.2L15.4 10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      '</span>' +
      '<b>' + c.name + '</b>' +
      '<span>' + c.body + '</span>';
    return '<li class="tr">' +
      (c.href ? '<a href="' + c.href + '">' + inner + '</a>' : inner) +
      '</li>';
  }).join('');
})();
