/* ============================================================
   Legal Center
   Indice que acompanha a leitura, e o formulario de reclamacao,
   que precisa devolver um numero de caso porque o guia de
   compliance exige numero e trilha de auditoria por reclamacao.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- indice acompanha a leitura ---------- */
  var links = [].slice.call(document.querySelectorAll('.lgnav a'));
  var docs = links.map(function (a) {
    return document.querySelector(a.getAttribute('href'));
  }).filter(Boolean);

  if (docs.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-on', a.getAttribute('href') === '#' + e.target.id);
        });
      });
    }, { rootMargin: '-96px 0px -70% 0px', threshold: 0 });
    docs.forEach(function (d) { io.observe(d); });
  }

  /* ---------- reclamacao ---------- */
  var form = document.getElementById('concernForm');
  if (!form) return;
  var out = document.getElementById('concernOut');

  function fail(field, on) {
    var err = form.querySelector('[data-err-for="' + field.id + '"]');
    field.setAttribute('aria-invalid', on ? 'true' : 'false');
    if (err) err.classList.toggle('is-on', on);
    return !on;
  }

  // Numero de caso legivel: RU-C-AAAAMMDD-XXXX. O sufixo vem do
  // servidor quando o backend existir; aqui e so a forma.
  function caseNumber() {
    var d = new Date();
    var ymd = d.getFullYear() +
      String(d.getMonth() + 1).padStart(2, '0') +
      String(d.getDate()).padStart(2, '0');
    var n = String(Math.floor(Math.random() * 9000) + 1000);
    return 'RU-C-' + ymd + '-' + n;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    ['cnName', 'cnMail', 'cnCat', 'cnDesc'].forEach(function (id) {
      var f = document.getElementById(id);
      if (!f) return;
      var empty = !String(f.value || '').trim();
      var badMail = id === 'cnMail' && !empty && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.value);
      if (!fail(f, empty || badMail)) ok = false;
    });
    if (!ok) {
      var first = form.querySelector('[aria-invalid="true"]');
      if (first) first.focus();
      return;
    }
    var id = caseNumber();
    out.textContent = 'Received. Your case number is ' + id +
      '. We reply within two business days, and the case stays open until you tell us it is resolved.';
    out.classList.add('is-ok');
    form.querySelector('button[type="submit"]').disabled = true;
  });
})();
