/* ============================================================
   Rodape legal compartilhado
   O guia de compliance pede o mesmo conjunto de links em toda
   tela. Em vez de repetir o bloco em cinco arquivos, ele e
   montado aqui e injetado em quem tiver <footer id="siteFoot">.
   O site publico escreve o proprio rodape em HTML, por SEO.
   ============================================================ */
(function () {
  'use strict';
  var host = document.getElementById('siteFoot');
  if (!host) return;

  var base = host.dataset.base || '';   // '../' quando a pagina estiver em subpasta

  var LINKS = [
    ['Terms of Use', 'legal.html#terms'],
    ['Privacy Policy', 'legal.html#privacy'],
    ['Medical Disclaimer', 'legal.html#medical'],
    ['Independent Providers', 'legal.html#providers'],
    ['Concierge Terms', 'legal.html#concierge'],
    ['Cancellation &amp; Refunds', 'legal.html#cancellation'],
    ['Travel &amp; Insurance', 'legal.html#travel'],
    ['Payment &amp; Fees', 'legal.html#payments'],
    ['Privacy Choices', 'legal.html#cookies'],
    ['Accessibility', 'legal.html#accessibility'],
    ['Contact &amp; Complaints', 'legal.html#complaints']
  ];

  var year = new Date().getFullYear();

  host.className = 'foot foot--slim';
  host.innerHTML =
    '<div class="wrap">' +
      '<div class="foot__emerg" role="note">' +
        '<p><b>Not for medical emergencies.</b> If you believe you are experiencing a medical emergency, ' +
        'contact your local emergency service immediately. For procedure-related medical questions, ' +
        'contact your treating physician or clinic.</p>' +
      '</div>' +
      '<nav class="foot__legalnav" aria-label="Legal">' +
        LINKS.map(function (l) {
          return '<a href="' + base + l[1] + '">' + l[0] + '</a>';
        }).join('') +
      '</nav>' +
      '<div class="foot__legal">' +
        '<p>RefreshU coordinates travel, hospitality and logistics around a medical journey. ' +
        'Participating physicians and clinics are independent providers and control eligibility, ' +
        'treatment plans and every clinical requirement. RefreshU does not practise medicine, does not ' +
        'make medical decisions and does not promise a clinical result.</p>' +
      '</div>' +
      '<div class="foot__base">' +
        '<span>&copy; ' + year + ' RefreshU</span>' +
        '<span>Legal, privacy, pricing, insurance and marketing content is pending professional review.</span>' +
      '</div>' +
    '</div>';
})();
