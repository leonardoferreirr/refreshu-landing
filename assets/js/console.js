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
  var traduz = window.t || function (s) { return s; };

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
    record: { title: 'Michael Carter', sub: traduz('Record #RU-2419 · arrival in Brazil · day 2 of 8'), parent: 'clients' },
    prospect: { title: 'James Whitfield', sub: traduz('Prospect #PR-1188 · medical review · call overdue'), parent: 'prospects' }
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

  // Um drawer com varios paineis. Quem abre diz qual painel quer; o painel
  // traz o proprio titulo. Os que nao estao em uso saem do DOM visivel, para
  // que o foco nunca caia num campo de painel escondido.
  var dTitle = document.getElementById('drawerTitle');
  var lastFocus = null;

  function openDrawer(name) {
    if (!drawer) return;

    var panels = drawer.querySelectorAll('.dpanel');
    var target = drawer.querySelector('.dpanel[data-panel="' + name + '"]') || panels[0];
    if (!target) return;

    panels.forEach(function (p) { p.hidden = p !== target; });
    if (dTitle && target.dataset.title) dTitle.textContent = target.dataset.title;

    lastFocus = document.activeElement;
    drawer.hidden = false;
    requestAnimationFrame(function () { drawer.setAttribute('data-open', ''); });
    document.body.style.overflow = 'hidden';

    var first = target.querySelector('input:not([readonly]):not([disabled]), select, textarea, button');
    if (first) first.focus();
  }

  function closeDrawer() {
    if (!drawer || drawer.hidden) return;
    drawer.removeAttribute('data-open');
    document.body.style.overflow = '';
    setTimeout(function () { drawer.hidden = true; }, 300);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
    lastFocus = null;
  }

  document.addEventListener('click', function (e) {
    var open = e.target.closest('[data-drawer]');
    if (open) { e.preventDefault(); openDrawer(open.dataset.drawer); return; }
    if (e.target.closest('[data-close]')) { e.preventDefault(); closeDrawer(); }
  });

  // Prende o foco dentro do drawer enquanto ele estiver aberto.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab' || !drawer || drawer.hidden) return;
    var can = drawer.querySelectorAll('.dpanel:not([hidden]) input:not([disabled]), .dpanel:not([hidden]) select, .dpanel:not([hidden]) textarea, .dpanel:not([hidden]) button, .drawer__h button');
    if (!can.length) return;
    var first = can[0], last = can[can.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ----------------------------------------------- visibilidade (A.3.8) -- */

  // Alterna direto na linha, sem abrir nada: o controle documento a documento
  // que o item pede so serve se for de um clique.
  document.addEventListener('click', function (e) {
    var t = e.target.closest('.vis');
    if (!t) return;
    var on = t.getAttribute('aria-pressed') === 'true';
    t.setAttribute('aria-pressed', String(!on));
    t.classList.toggle('vis--on', !on);
    var lbl = t.getAttribute('aria-label') || '';
    if (/client/i.test(lbl)) t.setAttribute('aria-label', on ? traduz('Hidden from the client') : traduz('Visible to the client'));
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


  /* ------------------------------------------------- fornecedores ------- */
  // Uma tabela por cidade. Sao Paulo abre por padrao.
  document.querySelectorAll('[data-sup]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-sup]').forEach(function (x) {
        x.setAttribute('aria-pressed', String(x === b));
      });
      document.querySelectorAll('#supTbl tbody').forEach(function (t) {
        t.hidden = t.dataset.city !== b.dataset.sup;
      });
    });
  });

  /* ----------------------------------------- publicar o itinerario ------ */
  // Publicar cria uma versao nova e carimba data e hora. Nunca altera a
  // versao anterior, que continua auditavel.
  var pub = document.getElementById('itinPublish');
  var pubState = document.getElementById('pubState');
  if (pub && pubState) {
    pub.addEventListener('click', function () {
      var now = new Date();
      var hh = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
      pubState.textContent = traduz('Published version 4 at {h}').replace('{h}', hh);
      pubState.classList.add('is-clean');
      pub.disabled = true;
      pub.textContent = traduz('Published');
    });
  }
  var prev = document.getElementById('itinPreview');
  if (prev) prev.addEventListener('click', function () { window.open('portal.html#trip', '_blank', 'noopener'); });

  /* ------------------------------------- credenciais publicas ----------- */
  // Le a mesma lista que o site usa, para que console e site nunca
  // divirjam sobre o que ja foi conquistado.
  var credBody = document.querySelector('#credTbl tbody');
  if (credBody) {
    var CREDS = window.RU_CREDENTIALS || [];
    if (!CREDS.length) {
      credBody.innerHTML = '<tr><td colspan="4">Credential list not loaded.</td></tr>';
    } else {
      credBody.innerHTML = CREDS.map(function (c) {
        var live = c.status === 'active';
        var tag = live ? '<span class="tag tag--ok">Active</span>'
          : (c.status === 'expired' ? '<span class="tag tag--bad">Expired</span>'
                                    : '<span class="tag tag--wait">Not earned yet</span>');
        return '<tr' + (live ? '' : ' class="is-off"') + '>' +
          '<th scope="row">' + c.name + '</th>' +
          '<td>' + (c.issuer || 'RefreshU') + '</td>' +
          '<td>' + tag + '</td>' +
          '<td>' + (live ? traduz('Shown') : traduz('Hidden')) + '</td>' +
          '</tr>';
      }).join('');
    }
  }

})();

/* --- Criacao da conta da cliente (tela de vendas) -------------------------
   A unica porta de entrada do portal. O site publico nao tem cadastro: uma
   conta existe porque alguem de vendas ou do admin criou contra um negocio
   fechado, e o convite sai para o e-mail da ficha.

   Sem backend ligado, o botao registra a intencao e diz o que vai acontecer
   quando o convite existir de verdade. Dizer isso e melhor que fingir que o
   e-mail saiu. */
(function () {
  'use strict';
  var go = document.getElementById('acctGo');
  if (!go) return;

  var ok = document.getElementById('acctConfirm');
  var mail = document.getElementById('acctMail');
  var deal = document.getElementById('acctDeal');
  var msg = document.getElementById('acctMsg');
  var tag = document.getElementById('acctTag');

  function valida() {
    var temMail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test((mail.value || '').trim());
    go.disabled = !(temMail && deal.value && ok.checked);
  }

  [ok, mail, deal].forEach(function (el) {
    el.addEventListener('input', valida);
    el.addEventListener('change', valida);
  });
  valida();

  go.addEventListener('click', function () {
    go.disabled = true;
    tag.textContent = traduz('Invitation queued');
    tag.className = 'tag tag--warn';
    msg.textContent = 'Queued for ' + mail.value.trim() +
      '. The email goes out when the backend is connected; the account itself is created on that same call.';
    ok.disabled = mail.disabled = deal.disabled = true;
  });
})();
