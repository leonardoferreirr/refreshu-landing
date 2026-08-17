/* RefreshU · entrada no portal.
   O portal ainda nao tem back end. Em vez de simular um login que nao existe,
   o envio devolve a regra real do produto: o portal abre depois que um medico
   analisa a avaliacao (secoes 14, 15 e 27 do briefing). Quando a autenticacao
   e a assinatura entrarem, o unico ponto a trocar e o corpo de enviar(). */
(function () {
  'use strict';

  var form = document.getElementById('signinForm');
  if (!form) return;

  var email = document.getElementById('email');
  var senha = document.getElementById('password');
  var botao = document.getElementById('signinBtn');
  var aviso = document.getElementById('authMsg');
  var olho = document.getElementById('peek');

  /* mostrar/esconder senha */
  if (olho && senha) {
    olho.addEventListener('click', function () {
      var vendo = senha.type === 'text';
      senha.type = vendo ? 'password' : 'text';
      olho.setAttribute('aria-pressed', vendo ? 'false' : 'true');
      olho.setAttribute('aria-label', vendo ? 'Show password' : 'Hide password');
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
    botao.textContent = 'Checking';
    botao.disabled = true;
    setTimeout(function () {
      botao.textContent = 'Sign In';
      botao.disabled = false;
      aviso.hidden = false;
      aviso.textContent = 'The client portal is not open yet. If you have already completed your evaluation, your concierge will send your access as soon as it is released.';
      aviso.focus && aviso.focus();
    }, 700);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    aviso.hidden = true;
    var okEmail = valida(email, temEmail(email.value));
    var okSenha = valida(senha, senha.value.trim().length > 0);
    if (!okEmail) { email.focus(); return; }
    if (!okSenha) { senha.focus(); return; }
    enviar();
  });
})();
