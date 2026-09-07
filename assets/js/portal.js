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
