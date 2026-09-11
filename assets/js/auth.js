/* RefreshU · entrada no portal.
   Ainda nao ha autenticacao: qualquer email valido abre o portal em modo
   demonstracao, que se anuncia como tal na faixa do topo. Quando a
   autenticacao e a assinatura entrarem, o unico ponto a trocar e o corpo de
   enviar(): validar credencial de verdade antes de redirecionar. */
(function () {
  'use strict';
  var traduz = window.t || function (s) { return s; };

  var form = document.getElementById('signinForm');
  if (!form) return;

  var email = document.getElementById('email');
  var senha = document.getElementById('password');
  var botao = document.getElementById('signinBtn');
  var olho = document.getElementById('peek');

  /* mostrar/esconder senha */
  if (olho && senha) {
    olho.addEventListener('click', function () {
      var vendo = senha.type === 'text';
      senha.type = vendo ? 'password' : 'text';
      olho.setAttribute('aria-pressed', vendo ? 'false' : 'true');
      olho.setAttribute('aria-label', vendo ? traduz('Show password') : traduz('Hide password'));
      senha.focus();
    });
  }

  function valida(campo, ok) {
    campo.closest('.fld').classList.toggle('is-bad', !ok);
    return ok;
  }
  function temEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }

  [email, senha].forEach(function (campo) {
    campo.addEventListener('input', function () {
      if (campo.closest('.fld').classList.contains('is-bad')) {
        valida(campo, campo === email ? temEmail(campo.value) : campo.value.trim().length > 0);
      }
    });
  });

  function enviar() {
    botao.textContent = traduz('Signing in');
    botao.disabled = true;
    setTimeout(function () { window.location.href = 'portal.html'; }, 620);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var okEmail = valida(email, temEmail(email.value));
    var okSenha = valida(senha, senha.value.trim().length > 0);
    if (!okEmail) { email.focus(); return; }
    if (!okSenha) { senha.focus(); return; }
    enviar();
  });
})();
