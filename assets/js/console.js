/* ==========================================================================
   RefreshU · shell das aplicacoes internas

   Um arquivo para console.html (operacao) e sales.html (comercial). As duas
   sao aplicacoes separadas, com login proprio, sobre a mesma base de codigo,
   como pede o Anexo A.1. O que muda entre elas e a navegacao e as telas, nao
   o comportamento, entao o shell e um so.

   Tres coisas: troca de tela, gaveta e menu no celular.
   ========================================================================== */

(function () {
  'use strict';

  var nav = document.querySelector('.cnav');
  if (!nav) return;

  var views = document.querySelectorAll('.cview');
  var title = document.getElementById('viewTitle');
  var sub = document.getElementById('viewSub');
  var side = document.getElementById('cside');
  var burger = document.getElementById('cburger');
  var drawer = document.getElementById('drawer');

  // Telas de detalhe: nao tem item de menu proprio, entao carregam o titulo
  // consigo e acendem o item da listagem de onde vieram.
  var DETAIL = {
    record: { title: 'Michael Carter', sub: 'Record #RU-2419 · arrival in Brazil · day 2 of 8', parent: 'clients' },
    prospect: { title: 'James Whitfield', sub: 'Prospect #PR-1188 · medical review · call overdue', parent: 'prospects' }
  };

  /* ------------------------------------------------------------- telas --- */

  function show(name) {
    var target = document.getElementById('v-' + name);
    if (!target) return;

    var link = nav.querySelector('[data-view="' + name + '"]');
    var detail = DETAIL[name];

    views.forEach(function (v) { v.hidden = v !== target; });

    nav.querySelectorAll('a').forEach(function (a) {
      a.classList.remove('is-on');
      a.removeAttribute('aria-current');
    });

    if (link) {
      link.classList.add('is-on');
      link.setAttribute('aria-current', 'page');
      title.textContent = link.querySelector('.cnav__lbl').textContent;
      sub.textContent = link.dataset.sub || '';
    } else if (detail) {
      title.textContent = detail.title;
      sub.textContent = detail.sub;
      var parent = nav.querySelector('[data-view="' + detail.parent + '"]');
      if (parent) parent.classList.add('is-on');
    }

    if (history.replaceState) history.replaceState(null, '', '#' + name);
    window.scrollTo(0, 0);
    closeSide();
  }

  nav.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-view]');
    if (!a) return;
    e.preventDefault();
    show(a.dataset.view);
  });

  // Atalhos dentro das telas: linha de tabela, card do funil, botao de acao.
  document.addEventListener('click', function (e) {
    var go = e.target.closest('[data-goto]');
    if (go) { e.preventDefault(); show(go.dataset.goto); return; }

    var open = e.target.closest('[data-open]');
    if (open && !e.target.closest('[data-drawer]')) { e.preventDefault(); show(open.dataset.open); }
  });

  /* ------------------------------------------------------------ gaveta --- */

  function openDrawer() {
    if (!drawer) return;
    drawer.hidden = false;
    requestAnimationFrame(function () { drawer.setAttribute('data-open', ''); });
    document.body.style.overflow = 'hidden';
    var first = drawer.querySelector('select, input, textarea, button');
    if (first) first.focus();
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.removeAttribute('data-open');
    document.body.style.overflow = '';
    setTimeout(function () { drawer.hidden = true; }, 300);
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-drawer]')) { e.preventDefault(); openDrawer(); return; }
    if (e.target.closest('[data-close]')) { e.preventDefault(); closeDrawer(); }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (drawer && !drawer.hidden) { closeDrawer(); } else { closeSide(); }
  });

  /* ------------------------------------------------------------- menu ---- */

  function closeSide() {
    if (!side) return;
    side.removeAttribute('data-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
  }

  if (burger) {
    burger.addEventListener('click', function () {
      if (side.hasAttribute('data-open')) { closeSide(); return; }
      side.setAttribute('data-open', '');
      burger.setAttribute('aria-expanded', 'true');
    });
  }

  document.addEventListener('click', function (e) {
    if (window.innerWidth > 900) return;
    if (!side || !side.hasAttribute('data-open')) return;
    if (e.target.closest('.cside') || e.target.closest('#cburger')) return;
    closeSide();
  });

  /* -------------------------------------------------------- decorativo --- */

  document.querySelectorAll('.segs').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      g.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    });
  });

  /* -------------------------------------------------------------- boot --- */

  var start = (location.hash || '').slice(1);
  var first = nav.querySelector('a[data-view]');
  show(document.getElementById('v-' + start) ? start : (first ? first.dataset.view : ''));

})();
