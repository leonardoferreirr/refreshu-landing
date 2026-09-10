/* RefreshU · portal do cliente (demonstracao).
   Troca de tela pelo hash, para que cada area tenha URL propria e o botao de
   voltar do navegador funcione durante a apresentacao ao cliente. */
(function () {
  'use strict';

  /* O titulo e o subtitulo saem do proprio menu, nao de uma tabela no codigo.
     Assim a versao pt-BR gerada por traduzir.py traduz o HTML e as telas
     acompanham, sem precisar de um segundo arquivo de JavaScript. */
  var titulo = document.getElementById('viewTitle');
  var sub = document.getElementById('viewSub');
  var links = document.querySelectorAll('.pnav a');
  var lateral = document.getElementById('pside');
  var burger = document.getElementById('pburger');

  function existe(nome) {
    return !!document.getElementById('v-' + nome);
  }

  function mostrar(nome, rolarTopo) {
    if (!existe(nome)) nome = 'journey';

    var secoes = document.querySelectorAll('.pview');
    for (var i = 0; i < secoes.length; i++) {
      secoes[i].hidden = (secoes[i].id !== 'v-' + nome);
    }
    var atual = null;
    for (var j = 0; j < links.length; j++) {
      var igual = links[j].getAttribute('data-view') === nome;
      links[j].classList.toggle('is-on', igual);
      if (igual) atual = links[j];
    }

    if (atual) {
      var lbl = atual.querySelector('.pnav__lbl');
      titulo.textContent = lbl ? lbl.textContent.trim() : nome;
      sub.textContent = atual.getAttribute('data-sub') || '';
      document.title = titulo.textContent + ' \u00b7 RefreshU';
    }

    fechar();
    if (rolarTopo) window.scrollTo(0, 0);
  }

  function doHash() {
    mostrar((location.hash || '#journey').slice(1), false);
  }

  /* qualquer link com data-view navega, inclusive os de dentro dos cartoes */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-view]');
    if (!a) return;
    e.preventDefault();
    var nome = a.getAttribute('data-view');
    if (location.hash.slice(1) !== nome) location.hash = nome;
    mostrar(nome, true);
  });

  window.addEventListener('hashchange', doHash);

  /* menu lateral no celular */
  function fechar() {
    if (!lateral || !lateral.classList.contains('is-open')) return;
    lateral.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  if (burger && lateral) {
    burger.addEventListener('click', function () {
      var aberto = lateral.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', aberto ? 'true' : 'false');
      document.body.style.overflow = aberto ? 'hidden' : '';
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') fechar(); });
  }

  /* ------------------------------------------------------ agenda (A.5.5) - */

  // Duas visoes sobre a mesma linha do tempo, como o item pede: por dia, que e
  // o padrao, e em lista corrida para quem quer ver a semana inteira de uma vez.
  // Os eventos sao os mesmos; muda o arranjo, nao o conteudo.
  var semana = document.querySelector('.week2');
  document.querySelectorAll('[data-sched]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-sched]').forEach(function (x) {
        x.setAttribute('aria-pressed', String(x === b));
      });
      if (!semana) return;
      if (b.dataset.sched === 'list') { semana.setAttribute('data-view', 'list'); }
      else { semana.removeAttribute('data-view'); }
    });
  });

  /* ------------------------------------------- instrucoes do medico ------

     Confirmar leitura muda o estado da instrucao e nada mais. Nao edita o
     texto, nao completa clinicamente, nao vale como consentimento. Quem
     completa um item clinico e o medico ou a equipe dele.                 */

  var pins = document.getElementById('pins');
  var pinsAck = document.getElementById('pinsAck');
  var pinsBadge = document.getElementById('pinsBadge');

  if (pins && pinsAck && pinsBadge) {
    pinsAck.addEventListener('change', function () {
      var lido = pinsAck.checked;
      pins.dataset.status = lido ? 'read' : 'released';
      pinsBadge.textContent = lido ? 'Read' : 'Action required';
      pinsBadge.className = 'tag pins__badge ' + (lido ? 'tag--ok' : 'tag--act');
      // Registro do aceite por versao: o backend grava author, versao e hora.
      pins.dataset.ackAt = lido ? new Date().toISOString() : '';
      pins.dataset.ackVersion = lido ? (pins.dataset.version || '') : '';
    });
  }

  var pinsHist = document.getElementById('pinsHist');
  var pinsHistBox = document.getElementById('pinsHistBox');
  if (pinsHist && pinsHistBox) {
    pinsHist.addEventListener('click', function () {
      var aberto = !pinsHistBox.hidden;
      pinsHistBox.hidden = aberto;
      pinsHist.textContent = aberto ? 'View previous version' : 'Hide previous version';
    });
  }

  /* --------------------------------------- perguntar ao medico ou a nos --

     Um link com data-ask="physician" abre o Support ja na porta clinica.
     Uma pergunta clinica nunca cai no canal do concierge por acidente.   */

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-ask]');
    if (!a || a.dataset.ask !== 'physician') return;
    setTimeout(function () {
      var alvo = document.getElementById('ask-physician');
      if (!alvo) return;
      alvo.scrollIntoView({ behavior: 'smooth', block: 'center' });
      alvo.classList.add('is-flash');
      setTimeout(function () { alvo.classList.remove('is-flash'); }, 1400);
    }, 60);
  });

  /* ------------------------------------------- pedidos de privacidade ----

     Cada pedido abre um chamado com numero. Exclusao nunca apaga na hora:
     ha registro sujeito a retencao, e isso e dito na propria resposta.   */

  var prqOut = document.getElementById('prqOut');
  var PRQ = {
    copy: 'A copy of your information was requested.',
    correction: 'A correction was requested. We will ask you what should change.',
    deletion: 'A deletion request was opened for review. Records under a retention obligation are identified and explained to you before anything is removed.',
    closure: 'Account closure was requested. If you have an active trip we speak to you first.'
  };
  document.querySelectorAll('[data-prq]').forEach(function (b) {
    b.addEventListener('click', function () {
      var d = new Date();
      var num = 'RU-P-' + d.getFullYear() +
        String(d.getMonth() + 1).padStart(2, '0') +
        String(d.getDate()).padStart(2, '0') + '-' +
        String(Math.floor(Math.random() * 9000) + 1000);
      if (prqOut) {
        prqOut.textContent = PRQ[b.dataset.prq] + ' Case number ' + num + '.';
        prqOut.classList.add('is-ok');
      }
      b.disabled = true;
    });
  });

  /* ------------------------------------------------ imprimir itinerario --
     Sempre a versao publicada corrente, com data, hora e numero de versao
     no proprio documento. Notas internas nao existem nesta tela.          */

  ['itinPrint', 'itinPdf'].forEach(function (id) {
    var b = document.getElementById(id);
    if (b) b.addEventListener('click', function () { window.print(); });
  });

  doHash();
})();

/* --- Perfil da medica: canais e antes/depois ------------------------------
   Tudo vem de config.js. A regra e a mesma nos dois blocos: sem dado
   aprovado, o portal diz "nao publicado" em vez de mostrar moldura vazia.
   Publicar link ou foto de medica sem autorizacao assinada e o risco que
   este arquivo existe para evitar. */
(function () {
  'use strict';
  var CFG = (window.REFRESHU_CONFIG || {}).physicians || {};
  var med = CFG['juliana-buttros'];
  if (!med) return;

  /* o botao que leva ao site dela: sem endereco, nao aparece */
  var bt = document.getElementById('docSite');
  if (bt) {
    if (med.site) { bt.href = med.site; } else { bt.hidden = true; }
  }

  /* canais */
  var REDES = { instagram: 'Instagram', tiktok: 'TikTok', youtube: 'YouTube', linkedin: 'LinkedIn' };
  var ul = document.getElementById('docSocial');
  var off = document.getElementById('docSocialOff');
  var links = Object.keys(REDES).filter(function (k) { return med.social && med.social[k]; });

  if (ul && links.length) {
    links.forEach(function (k) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = med.social[k];
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = REDES[k];
      li.appendChild(a);
      ul.appendChild(li);
    });
    ul.hidden = false;
    if (off) off.hidden = true;
  }

  /* antes e depois */
  var ba = document.getElementById('docBA');
  var baNota = document.getElementById('docBANote');
  var baOff = document.getElementById('docBAOff');
  var casos = (med.beforeAfter || []).filter(function (c) { return c && c.before && c.after && c.consent; });

  if (ba && casos.length) {
    casos.forEach(function (c) {
      var fig = document.createElement('figure');
      fig.className = 'ba__i';
      [['before', 'Before'], ['after', 'After']].map(function (par) {
        var wrap = document.createElement('span');
        wrap.className = 'ba__f';
        var img = document.createElement('img');
        img.src = c[par[0]];
        img.alt = par[1] + (c.caption ? ', ' + c.caption : '');
        img.loading = 'lazy';
        img.decoding = 'async';
        var tag = document.createElement('b');
        tag.textContent = par[1];
        wrap.appendChild(img);
        wrap.appendChild(tag);
        return wrap;
      }).forEach(function (n) { fig.appendChild(n); });

      if (c.caption) {
        var cap = document.createElement('figcaption');
        cap.textContent = c.caption;
        fig.appendChild(cap);
      }
      ba.appendChild(fig);
    });
    ba.hidden = false;
    if (baNota) baNota.hidden = false;
    if (baOff) baOff.hidden = true;
  }
})();
