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

  doHash();
})();
