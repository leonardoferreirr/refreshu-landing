/* ==========================================================================
   RefreshU · Operations Console

   Tres coisas: troca de tela, troca de papel e a gaveta.

   A troca de papel e o unico ponto que merece atencao. O Anexo A.4 define a
   Plataforma de Vendas como a mesma aplicacao sob papel restrito, e o A.4.2
   lista o que esse papel nao alcanca. Aqui isso e demonstracao de interface;
   em producao a decisao e do servidor, e a rota tem que recusar mesmo que
   alguem force o caminho pelo endereco.
   ========================================================================== */

(function () {
  'use strict';

  var nav = document.querySelector('.cnav');
  var views = document.querySelectorAll('.cview');
  var title = document.getElementById('viewTitle');
  var sub = document.getElementById('viewSub');
  var side = document.getElementById('cside');
  var burger = document.getElementById('cburger');
  var drawer = document.getElementById('drawer');

  /* ------------------------------------------------------------- telas --- */

  function show(name) {
    var link = nav.querySelector('[data-view="' + name + '"]');

    // Pedido para uma tela que o papel atual nao alcanca cai no Overview.
    // E o que o servidor faria: nega e devolve para onde a pessoa pode estar.
    if (link && link.classList.contains('is-locked')) { name = 'overview'; link = nav.querySelector('[data-view="overview"]'); }

    var target = document.getElementById('v-' + name);
    if (!target) return;

    views.forEach(function (v) { v.hidden = v !== target; });

    nav.querySelectorAll('a').forEach(function (a) {
      a.classList.toggle('is-on', a === link);
      if (a === link) { a.setAttribute('aria-current', 'page'); } else { a.removeAttribute('aria-current'); }
    });

    if (link) {
      title.textContent = link.querySelector('.cnav__lbl').textContent;
      sub.textContent = (isSales() && link.dataset.subSales) || link.dataset.sub || '';
    } else if (name === 'record') {
      // O registro nao tem item de menu proprio: e o detalhe de Clients.
      title.textContent = 'Michael Carter';
      sub.textContent = 'Record #RU-2419 · arrival in Brazil · day 2 of 8';
      var cl = nav.querySelector('[data-view="clients"]');
      if (cl) cl.classList.add('is-on');
    }

    if (history.replaceState) history.replaceState(null, '', '#' + name);
    document.querySelector('.cmain').scrollTo({ top: 0, behavior: 'instant' });
    window.scrollTo({ top: 0, behavior: 'instant' });
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

  /* ------------------------------------------------------------- papel --- */

  var ROLES = {
    admin: { name: 'Beatriz Lima', initials: 'BL', label: 'Administrator · São Paulo' },
    sales: { name: 'Tomás Cardoso', initials: 'TC', label: 'Sales · São Paulo' }
  };

  // Colunas da lista de clientes que o papel de Vendas nao alcanca: o medico
  // designado e o financeiro do registro (Anexo A.4.2). Escondidas por indice
  // porque a tabela e uma so; no servidor a consulta e que nao traz o campo.
  var HIDDEN_COLS = [3, 6];

  function isSales() {
    var b = document.querySelector('.roleswap__b[data-role="sales"]');
    return b && b.getAttribute('aria-pressed') === 'true';
  }

  function setRole(role) {
    var sales = role === 'sales';

    document.querySelectorAll('.roleswap__b').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.role === role));
    });

    // O que o papel de Vendas nao alcanca fica listado e cadeado. Some seria
    // mais limpo, mas some tambem esconde o desenho: a separacao E o produto.
    nav.querySelectorAll('a[data-lock-sales]').forEach(function (a) {
      a.classList.toggle('is-locked', sales);
      a.setAttribute('aria-disabled', String(sales));
      if (sales) { a.setAttribute('tabindex', '-1'); } else { a.removeAttribute('tabindex'); }
    });

    document.querySelectorAll('[data-sales-only]').forEach(function (el) { el.hidden = !sales; });

    // Contagens e legendas que mudam com o alcance do papel.
    nav.querySelectorAll('[data-sub-sales]').forEach(function (a) {
      var n = a.querySelector('[data-n-sales]');
      if (n) {
        if (!n.dataset.nAdmin) n.dataset.nAdmin = n.textContent;
        n.textContent = sales ? n.dataset.nSales : n.dataset.nAdmin;
      }
    });

    // A lista de clientes perde as colunas fora do alcance.
    var tbl = document.querySelector('#v-clients .ctbl');
    if (tbl) {
      tbl.querySelectorAll('tr').forEach(function (tr) {
        HIDDEN_COLS.forEach(function (i) {
          var cell = tr.children[i];
          if (cell) cell.hidden = sales;
        });
      });
    }

    var cta = document.querySelector('.ctop .cbtn');
    if (cta) cta.lastChild.textContent = sales ? ' New prospect' : ' New record';

    var who = ROLES[role];
    document.getElementById('meName').textContent = who.name;
    document.getElementById('meAv').textContent = who.initials;
    document.getElementById('meRole').textContent = who.label;

    // Se a tela aberta acabou de sair do alcance, sai dela. O painel do
    // vendedor e o proprio funil, entao Vendas cai no Pipeline.
    var current = document.querySelector('.cview:not([hidden])');
    if (current) {
      var link = nav.querySelector('[data-view="' + current.id.replace('v-', '') + '"]');
      var isRecord = current.id === 'v-record';
      if ((link && link.classList.contains('is-locked')) || (sales && isRecord)) {
        show(sales ? 'pipeline' : 'overview');
      }
    }
  }

  document.querySelectorAll('.roleswap__b').forEach(function (b) {
    b.addEventListener('click', function () { setRole(b.dataset.role); });
  });

  /* ------------------------------------------------------------ gaveta --- */

  function openDrawer() {
    drawer.hidden = false;
    requestAnimationFrame(function () { drawer.setAttribute('data-open', ''); });
    document.body.style.overflow = 'hidden';
    var first = drawer.querySelector('select, input, textarea, button');
    if (first) first.focus();
  }

  function closeDrawer() {
    drawer.removeAttribute('data-open');
    document.body.style.overflow = '';
    setTimeout(function () { drawer.hidden = true; }, 300);
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-drawer]')) { e.preventDefault(); openDrawer(); return; }
    if (e.target.closest('[data-close]')) { e.preventDefault(); closeDrawer(); }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (!drawer.hidden) closeDrawer();
      else closeSide();
    }
  });

  /* ------------------------------------------------------------- menu ---- */

  function closeSide() {
    side.removeAttribute('data-open');
    burger.setAttribute('aria-expanded', 'false');
  }

  burger.addEventListener('click', function () {
    var open = side.hasAttribute('data-open');
    if (open) { closeSide(); } else {
      side.setAttribute('data-open', '');
      burger.setAttribute('aria-expanded', 'true');
    }
  });

  document.addEventListener('click', function (e) {
    if (window.innerWidth > 900) return;
    if (!side.hasAttribute('data-open')) return;
    if (e.target.closest('.cside') || e.target.closest('#cburger')) return;
    closeSide();
  });

  /* -------------------------------------------------------- decorativo --- */

  // Os grupos de filtro sao segmentos de uma escolha so.
  document.querySelectorAll('.segs').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      g.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    });
  });

  /* -------------------------------------------------------------- boot --- */

  setRole('admin');
  var start = (location.hash || '#overview').slice(1);
  show(document.getElementById('v-' + start) ? start : 'overview');

})();
