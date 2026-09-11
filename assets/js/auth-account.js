/* ==========================================================================
   RefreshU · redefinicao de senha da clienta

   A pagina recover.html carregava este arquivo, que nao existia. O resultado
   era um 404 silencioso e a tela inteira morta: o botao nao fazia nada, o
   campo de codigo nunca aparecia e o olho da senha nao abria.

   Tres etapas na mesma tela, que e o que o HTML ja desenhava: o e-mail, o
   codigo de seis digitos e a senha nova. Aqui e demonstracao, entao qualquer
   e-mail valido segue e qualquer codigo de seis digitos entra. Em producao a
   primeira etapa dispara o envio do codigo e nao revela se a conta existe,
   a segunda troca o codigo por um token de uso unico, e a terceira e a unica
   que grava. Nenhuma das tres decide nada no navegador.

   Os rotulos passam por traduz() porque esta tela existe em mais de um idioma.
   ========================================================================== */

(function () {
  'use strict';

  var form = document.getElementById('resetForm');
  if (!form) return;

  var traduz = window.t || function (s) { return s; };

  var email = document.getElementById('email');
  var mfa = document.getElementById('mfa');
  var caixaSenha = document.getElementById('newPassWrap');
  var senha = document.getElementById('password');
  var peek = document.getElementById('peek');
  var btn = document.getElementById('resetBtn');
  var digits = mfa ? Array.prototype.slice.call(mfa.querySelectorAll('input')) : [];

  var MIN_SENHA = 10;   // o mesmo numero que a mensagem de erro promete
  var etapa = 1;

  /* ------------------------------------------------------------ campos --- */

  function fail(campo, on) {
    campo.setAttribute('aria-invalid', String(on));
    var err = form.querySelector('[data-err-for="' + campo.id + '"]');
    if (err) err.classList.toggle('is-on', on);
    return !on;
  }

  [email, senha].forEach(function (f) {
    if (!f) return;
    f.addEventListener('input', function () {
      if (f.getAttribute('aria-invalid') === 'true') fail(f, false);
    });
  });

  if (peek && senha) {
    peek.addEventListener('click', function () {
      var vendo = senha.type === 'text';
      senha.type = vendo ? 'password' : 'text';
      peek.setAttribute('aria-pressed', String(!vendo));
      peek.setAttribute('aria-label', vendo ? traduz('Show password') : traduz('Hide password'));
      senha.focus();
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

  function codigo() {
    return digits.map(function (d) { return d.value; }).join('');
  }

  /* -------------------------------------------------------- reenviar ----- */

  var reenviar = form.querySelector('a[href="#resend"]');
  if (reenviar) {
    reenviar.addEventListener('click', function (e) {
      e.preventDefault();
      digits.forEach(function (d) { d.value = ''; d.removeAttribute('data-filled'); });
      if (digits[0]) digits[0].focus();
    });
  }

  /* ------------------------------------------------------------- envio --- */

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (etapa === 1) {
      if (!fail(email, !email.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value))) return;
      etapa = 2;
      mfa.hidden = false;
      email.readOnly = true;
      btn.textContent = traduz('Continue');
      if (digits[0]) digits[0].focus();
      return;
    }

    if (etapa === 2) {
      if (codigo().length < digits.length) { digits[codigo().length].focus(); return; }
      etapa = 3;
      caixaSenha.hidden = false;
      digits.forEach(function (d) { d.readOnly = true; });
      btn.textContent = traduz('Save the new password');
      senha.focus();
      return;
    }

    if (!fail(senha, !senha.value || senha.value.length < MIN_SENHA)) return;

    btn.disabled = true;
    btn.textContent = traduz('Saving…');
    setTimeout(function () { location.href = 'signin.html'; }, 420);
  });

})();
