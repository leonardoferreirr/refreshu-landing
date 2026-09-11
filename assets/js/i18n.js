/* ============================================================
   Texto que nasce no JavaScript

   Parte da tela nao esta no HTML: o rodape legal, os selos de
   confianca, o catalogo de procedimentos e alguns rotulos que
   mudam por acao da pessoa. Esse texto nao passa pelo extrator
   de paginas, e sem isto sairia em ingles numa pagina em
   espanhol, que foi exatamente o que aconteceu.

   Como funciona: t('texto em ingles') devolve a traducao quando
   existe, e o proprio ingles quando nao existe. O ingles e a
   fonte da verdade aqui tambem, entao uma chave nova nunca
   quebra a tela, no maximo aparece sem traduzir.

   Este arquivo e a versao em ingles, com o dicionario vazio.
   As versoes traduzidas (i18n.es.js, i18n.pt.js) sao geradas
   por i18n_traduzir.py e trocadas no <script> de cada pagina.
   Nunca editar as geradas na mao.
   ============================================================ */
(function () {
  'use strict';
  var D = window.RU_T || {};
  window.RU_T = D;
  window.t = function (s) {
    return Object.prototype.hasOwnProperty.call(D, s) ? D[s] : s;
  };
})();
