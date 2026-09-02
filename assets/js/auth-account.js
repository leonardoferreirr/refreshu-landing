/* ==========================================================================
   RefreshU · criar conta e recuperar senha, lado do cliente

   Os dois fluxos do Anexo A.5.1 que faltavam. Ambos têm duas etapas com o
   mesmo código de seis dígitos, então dividem este arquivo. Aqui é
   demonstração: qualquer código de seis dígitos passa. Em produção a primeira
   etapa devolve um desafio e a segunda é quem abre a sessão ou grava a senha.
   ========================================================================== */

(function () {
  'use strict';

  var form = document.getElementById('signupForm') || document.getElementById('resetForm');
  if (!form) return;

  var isSignup = form.id === 'signupForm';
  var mfa = document.getElementById('mfa');
  var btn = document.getElementById(isSignup ? 'signupBtn' : 'resetBtn');
  var pass = document.getElementById('password');
  var peek = document.getElementById('peek');
  var newPassWrap = document.getElementById('newPassWrap');
  var digits = mfa ? Array.prototype.slice.call(mfa.querySelectorAll('input')) : [];

  var REQUIRED = isSignup ? ['fname', 'lname', 'email', 'password'] : ['email'];
  var step = 1;

  function f(id) { return document.getElementById(id); }

  function fail(el, bad) {
    if (!el) return true;
    el.setAttribute('aria-invalid', String(bad));
    var err = form.querySelector('[data-err-for="' + el.id + '"]');
    if (err) err.classList.toggle('is-on', bad);
    return !bad;
  }

  function check(id) {
    var el = f(id);
    if (!el) return true;
    var v = (el.value || '').trim();
    var bad = !v;
    if (id === 'email') bad = !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
    if (id === 'password') bad = v.length < 10;
    return fail(el, bad);
  }

  REQUIRED.forEach(function (id) {
    var el = f(id);
    if (!el) return;
    el.addEventListener('input', function () {
      if (el.getAttribute('aria-invalid') === 'true') check(id);
    });
  });

  if (peek && pass) {
    peek.addEventListener('click', function () {
      var shown = pass.type === 'text';
      pass.type = shown ? 'password' : 'text';
      peek.setAttribute('aria-pressed', String(!shown));
      peek.setAttribute('aria-label', shown ? 'Show password' : 'Hide password');
      pass.focus();
    });
  }

  /* ----------------------------------------------------- seis digitos --- */

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

  /* -------------------------------------------------------------- envio -- */

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (step === 1) {
      var bad = REQUIRED.filter(function (id) { return !check(id); });

      var terms = f('terms');
      if (isSignup && terms && !terms.checked) { terms.focus(); return; }
      if (bad.length) { f(bad[0]).focus(); return; }

      step = 2;
      mfa.hidden = false;
      if (newPassWrap) newPassWrap.hidden = false;
      REQUIRED.forEach(function (id) { var el = f(id); if (el) el.readOnly = true; });
      btn.textContent = isSignup ? 'Verify and continue' : 'Save new password';
      digits[0].focus();
      return;
    }

    if (code().length < digits.length) { digits[code().length].focus(); return; }
    // No fluxo de recuperacao a senha nova so existe na segunda etapa.
    if (!isSignup && !check('password')) { pass.focus(); return; }

    btn.disabled = true;
    btn.textContent = isSignup ? 'Creating your account…' : 'Saving…';
    setTimeout(function () { location.href = isSignup ? 'portal.html' : 'signin.html'; }, 420);
  });

})();
