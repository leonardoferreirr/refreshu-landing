/* ==========================================================================
   RefreshU · login das aplicacoes internas

   Duas etapas, como pede o Anexo A.3.1: credencial e depois o codigo de seis
   digitos. Aqui e demonstracao, entao qualquer credencial valida passa e
   qualquer codigo de seis digitos entra. Em producao a primeira etapa devolve
   um token de desafio e a segunda e que abre a sessao, e nenhuma das duas
   decide nada no navegador.
   ========================================================================== */

(function () {
  'use strict';

  var form = document.getElementById('teamForm');
  if (!form) return;

  var mfa = document.getElementById('mfa');
  var btn = document.getElementById('teamBtn');
  var email = document.getElementById('email');
  var pass = document.getElementById('password');
  var peek = document.getElementById('peek');
  var digits = mfa ? Array.prototype.slice.call(mfa.querySelectorAll('input')) : [];

  var app = form.dataset.app === 'sales' ? 'sales.html' : 'console.html';
  var step = 1;

  /* ------------------------------------------------------------ campos --- */

  function fail(field, on) {
    field.setAttribute('aria-invalid', String(on));
    var err = form.querySelector('[data-err-for="' + field.id + '"]');
    if (err) err.classList.toggle('is-on', on);
    return !on;
  }

  [email, pass].forEach(function (f) {
    f.addEventListener('input', function () { if (f.getAttribute('aria-invalid') === 'true') fail(f, false); });
  });

  if (peek) {
    peek.addEventListener('click', function () {
      var shown = pass.type === 'text';
      pass.type = shown ? 'password' : 'text';
      peek.setAttribute('aria-pressed', String(!shown));
      peek.setAttribute('aria-label', shown ? 'Show password' : 'Hide password');
      pass.focus();
    });
  }

  /* ----------------------------------------------------- seis digitos ---- */

  digits.forEach(function (d, i) {
    d.addEventListener('input', function () {
      d.value = d.value.replace(/\D/g, '').slice(0, 1);
      d.toggleAttribute('data-filled', !!d.value);
      if (d.value && i < digits.length - 1) digits[i + 1].focus();
    });

    d.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' && !d.value && i > 0) { digits[i - 1].focus(); return; }
      if (e.key === 'ArrowLeft' && i > 0) { e.preventDefault(); digits[i - 1].focus(); }
      if (e.key === 'ArrowRight' && i < digits.length - 1) { e.preventDefault(); digits[i + 1].focus(); }
    });

    // Colar o codigo inteiro em qualquer campo distribui os digitos.
    d.addEventListener('paste', function (e) {
      var txt = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '');
      if (!txt) return;
      e.preventDefault();
      txt.slice(0, digits.length - i).split('').forEach(function (c, k) {
        digits[i + k].value = c;
        digits[i + k].toggleAttribute('data-filled', true);
      });
      digits[Math.min(i + txt.length, digits.length - 1)].focus();
    });
  });

  function code() { return digits.map(function (d) { return d.value; }).join(''); }

  /* ------------------------------------------------------------- envio --- */

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (step === 1) {
      var okMail = fail(email, !email.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value));
      var okPass = fail(pass, !pass.value);
      if (!okMail || !okPass) return;

      step = 2;
      mfa.hidden = false;
      btn.textContent = 'Sign in';
      email.readOnly = true;
      pass.readOnly = true;
      digits[0].focus();
      return;
    }

    if (code().length < digits.length) { digits[code().length].focus(); return; }

    btn.disabled = true;
    btn.textContent = 'Signing in…';
    setTimeout(function () { location.href = app; }, 420);
  });

})();
