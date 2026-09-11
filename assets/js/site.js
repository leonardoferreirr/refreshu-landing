/* RefreshU · comportamento do site publico.
   Sem biblioteca: header que solidifica, menu do celular e entrada por scroll.
   Cuidado ja aprendido: nada de clip-path no elemento observado, senao o
   IntersectionObserver nunca dispara. Aqui a entrada e so opacity/transform. */
(function () {
  'use strict';
  var traduz = window.t || function (s) { return s; };

  var chrome = document.getElementById('chrome');
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  /* header ------------------------------------------------------------- */
  var stuck = false;
  function onScroll() {
    var s = window.pageYOffset > 40;
    if (s !== stuck) { stuck = s; chrome.classList.toggle('is-stuck', s); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* menu do celular ---------------------------------------------------- */
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? traduz('Close menu') : traduz('Open menu'));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName !== 'A' || !nav.classList.contains('is-open')) return;
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', traduz('Open menu'));
      document.body.style.overflow = '';
    });
  }

  /* entrada por scroll --------------------------------------------------
     Escalonado por vizinhanca: elementos que entram no mesmo quadro ganham
     um atraso em cascata, senao uma grade inteira acende de uma vez so. */
  var alvos = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    for (var i = 0; i < alvos.length; i++) alvos[i].classList.add('is-in');
    return;
  }

  var io = new IntersectionObserver(function (entradas) {
    var lote = 0;
    for (var j = 0; j < entradas.length; j++) {
      var e = entradas[j];
      if (!e.isIntersecting) continue;
      e.target.style.transitionDelay = (Math.min(lote, 5) * 70) + 'ms';
      e.target.classList.add('is-in');
      io.unobserve(e.target);
      lote++;
    }
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

  for (var k = 0; k < alvos.length; k++) io.observe(alvos[k]);
})();

/* --- Abas do destino ------------------------------------------------------
   Padrao de tablist: clique troca o painel, seta esquerda/direita anda entre
   as abas e leva o foco junto, e so a aba ativa fica na ordem de tabulacao. */
(function () {
  'use strict';
  var abas = [].slice.call(document.querySelectorAll('.dest__tab'));
  if (abas.length < 2) return;

  function mostra(alvo, move) {
    abas.forEach(function (b) {
      var on = b === alvo;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-selected', String(on));
      b.tabIndex = on ? 0 : -1;
      var painel = document.getElementById(b.getAttribute('aria-controls'));
      if (painel) painel.hidden = !on;
    });
    if (move) alvo.focus();
  }

  abas.forEach(function (b, i) {
    b.addEventListener('click', function () { mostra(b, false); });
    b.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      mostra(abas[(i + d + abas.length) % abas.length], true);
    });
  });
})();

/* --- Pilha que sobe: carimba o indice de cada cartao -----------------------
   O CSS precisa saber a posicao do cartao na fila para calcular o quanto ele
   gruda abaixo do anterior. Nao da para fazer isso so com CSS, entao o indice
   entra como variavel. Vale para qualquer .stack da pagina. */
(function () {
  'use strict';
  document.querySelectorAll('.stack').forEach(function (pilha) {
    [].forEach.call(pilha.children, function (c, i) {
      c.style.setProperty('--i', i);
    });
  });
})();
