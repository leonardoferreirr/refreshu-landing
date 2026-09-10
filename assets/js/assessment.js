/* ==========================================================================
   RefreshU · Book your call

   Tres telas: quem e voce, o que voce esta considerando, e a hora da call.
   Salvar e retomar guarda o rascunho no proprio navegador; em producao o
   rascunho vive no servidor, atado a conta.

   Nenhum campo clinico existe neste arquivo, e isso e proposital: a Clausula
   12.6 nao e uma validacao que se possa desligar, e a ausencia do campo. A
   parte clinica acontece no sistema do proprio medico, fora daqui.

   O agendamento e o "appointment schedule" do Google Calendar embutido: e ele
   que confirma por e-mail, cria o evento e lembra. Ver assets/js/config.js.
   ========================================================================== */

(function () {
  'use strict';

  var KEY = 'refreshu.assessment.v2';
  var LAST = 3;

  var panels = document.querySelectorAll('[data-panel]');
  var steps = document.querySelectorAll('.as__step');
  var next = document.getElementById('next');
  var back = document.getElementById('back');
  var foot = document.getElementById('foot');
  var saved = document.getElementById('saved');
  var procs = document.getElementById('procs');
  var form = document.getElementById('aboutForm');
  var procsHint = document.getElementById('procsHint');
  var bookSlot = document.getElementById('bookSlot');
  var bookAck = document.getElementById('bookAck');
  var CFG = window.REFRESHU_CONFIG || {};

  var state = load();
  var step = 1;

  /* ------------------------------------------------------- catalogo ----- */

  // Espelha as fichas de procedimento do item A.3.11, editaveis pelo admin.
  // As faixas de economia so aparecem quando a fonte esta aprovada: por isso
  // dental e body vem sem numero, exatamente como no console.
  var CATALOGUE = {
    hair: {
      label: 'Hair',
      doctor: { name: 'Dr. Camila Rocha', initials: 'CR', meta: 'Hair restoration · São Paulo · 14 years' },
      items: [
        { id: 'fue', name: 'FUE hair transplant', desc: 'Follicular unit extraction, the most common route.', save: '55 – 70%' },
        { id: 'dhi', name: 'DHI hair transplant', desc: 'Direct implantation, often for tighter density.', save: '55 – 70%' },
        { id: 'beard', name: 'Beard or eyebrow restoration', desc: 'Same technique, different area.', save: '55 – 70%' },
        { id: 'hair-other', name: 'Not sure yet', desc: 'The physician recommends the technique after seeing you.' }
      ]
    },
    face: {
      label: 'Face',
      doctor: { name: 'Dr. Helena Braga', initials: 'HB', meta: 'Plastic surgery · São Paulo · 19 years' },
      items: [
        { id: 'facelift', name: 'Facelift', desc: 'Full or lower face, depending on what you need.', save: '60 – 72%' },
        { id: 'eyelid', name: 'Eyelid surgery', desc: 'Upper, lower, or both.', save: '60 – 72%' },
        { id: 'rhino', name: 'Rhinoplasty', desc: 'Shape, profile or breathing.' },
        { id: 'face-other', name: 'Not sure yet', desc: 'Bring it to the consultation and decide there.' }
      ]
    },
    body: {
      label: 'Body',
      doctor: { name: 'Dr. Helena Braga', initials: 'HB', meta: 'Plastic surgery · São Paulo · 19 years' },
      items: [
        { id: 'contour', name: 'Body contouring', desc: 'Abdomen, flanks and waist.' },
        { id: 'lift', name: 'Lift procedures', desc: 'Arms, thighs or a lower body lift.' },
        { id: 'breast', name: 'Breast procedures', desc: 'Augmentation, reduction or lift.' },
        { id: 'body-other', name: 'Not sure yet', desc: 'A consultation is the honest first step here.' }
      ]
    },
    dental: {
      label: 'Dental',
      doctor: { name: 'Dr. Paulo Serra', initials: 'PS', meta: 'Dentistry · São Paulo · 11 years' },
      items: [
        { id: 'veneers', name: 'Veneers', desc: 'Porcelain, front teeth.' },
        { id: 'implants', name: 'Implants', desc: 'Single, multiple or full arch.' },
        { id: 'whitening', name: 'Whitening and cleaning', desc: 'Usually combined with another procedure.' },
        { id: 'dental-other', name: 'Not sure yet', desc: 'The dentist plans it after an examination.' }
      ]
    }
  };

  /* --------------------------------------------------------- rascunho --- */

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }

  var savedTimer;
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { return; }
    saved.classList.add('is-on');
    clearTimeout(savedTimer);
    savedTimer = setTimeout(function () { saved.classList.remove('is-on'); }, 1600);
  }

  /* ------------------------------------------------------------ telas --- */

  function go(n) {
    step = Math.max(1, Math.min(LAST, n));

    panels.forEach(function (p) { p.hidden = Number(p.dataset.panel) !== step; });

    steps.forEach(function (s) {
      var i = Number(s.dataset.step);
      s.classList.toggle('is-done', i < step);
      s.classList.toggle('is-now', i === step);
    });

    back.hidden = step === 1;
    // A ultima tela nao tem "continuar": quem conclui e o proprio calendario.
    next.hidden = step === LAST;
    foot.hidden = false;

    if (step === 2) paintProcs();
    if (step === LAST) { montaCalendario(); save(); }

    next.textContent = 'Continue';

    gate();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ------------------------------------------ 1. area de interesse ------ */

  document.querySelectorAll('.pick').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.pick').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (state.area !== b.dataset.area) { state.proc = null; state.procName = null; }
      state.area = b.dataset.area;
      state.areaLabel = b.dataset.label;
      // Area e procedimento moram na mesma etapa: escolher a area revela a
      // lista logo abaixo, em vez de mandar para outra tela.
      paintProcs();
      save();
      gate();
    });
  });

  /* ---------------------------------------------- 2. procedimento ------- */

  function paintProcs() {
    var cat = CATALOGUE[state.area];
    if (!cat) { procs.hidden = true; if (procsHint) procsHint.hidden = true; return; }
    procs.hidden = false;
    if (procsHint) procsHint.hidden = false;

    procs.innerHTML = '';
    cat.items.forEach(function (it) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'proc';
      b.setAttribute('aria-pressed', String(state.proc === it.id));
      b.dataset.proc = it.id;

      b.innerHTML =
        '<span class="proc__t">' +
          '<span class="proc__n"></span>' +
          '<span class="proc__d"></span>' +
        '</span>' +
        '<span class="proc__x">' +
          (it.save ? '<span class="save">Save ' + it.save + '</span>' : '') +
          '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" style="width:18px;height:18px;color:var(--on-paper-fine)"><path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
        '</span>';

      // Texto por nó, nunca por innerHTML: o catalogo e conteudo editavel
      // pelo admin, entao entra como dado, nao como marcacao.
      b.querySelector('.proc__n').textContent = it.name;
      b.querySelector('.proc__d').textContent = it.desc;

      b.addEventListener('click', function () {
        procs.querySelectorAll('.proc').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        state.proc = it.id;
        state.procName = it.name;
        save();
        gate();
      });

      procs.appendChild(b);
    });
  }

  /* ------------------------------------------------- 3. sobre voce ------ */

  var REQUIRED = ['fname', 'lname', 'mail', 'state', 'window'];

  function field(id) { return document.getElementById(id); }

  function valid(id, quiet) {
    var el = field(id);
    var v = (el.value || '').trim();
    var bad = !v || (id === 'mail' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v));

    if (!quiet) {
      el.setAttribute('aria-invalid', String(bad));
      var err = form.querySelector('[data-err-for="' + id + '"]');
      if (err) err.classList.toggle('is-on', bad);
    }
    return !bad;
  }

  REQUIRED.concat(['phone', 'anything']).forEach(function (id) {
    var el = field(id);
    if (!el) return;
    if (state[id]) el.value = state[id];

    el.addEventListener('input', function () {
      state[id] = el.value;
      if (el.getAttribute('aria-invalid') === 'true') valid(id);
      gate();
      save();
    });
    el.addEventListener('change', function () { state[id] = el.value; gate(); save(); });
  });

  document.querySelectorAll('[data-comp]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-comp]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      state.comp = b.dataset.comp;
      state.compLabel = b.textContent.trim();
      save();
    });
  });

  /* ----------------------------------------------- 3. book your call ----
     O agendamento e o "appointment schedule" do Google Calendar embutido.
     Ele confirma por e-mail, cria o evento nos dois calendarios e lembra, o
     que resolve a etapa inteira sem backend. O link vive em config.js.

     Sem link configurado a tela diz isso com todas as letras e oferece o
     e-mail, em vez de mostrar um quadro vazio que parece defeito.          */

  function urlDoCalendario() {
    var u = String(CFG.bookingUrl || '').trim();
    if (!u) return '';
    // O formato longo aceita ?gv=true para abrir ja embutido, sem o cabecalho
    // do Google. O curto (calendar.app.google) redireciona e nao precisa.
    if (u.indexOf('/appointments/schedules/') > -1 && u.indexOf('gv=true') === -1) {
      u += (u.indexOf('?') > -1 ? '&' : '?') + 'gv=true';
    }
    return u;
  }

  function montaCalendario() {
    if (!bookSlot || bookSlot.dataset.pronto) return;
    var url = urlDoCalendario();

    if (!url) {
      /* Sem o link do calendario a tela nao pode agendar, mas ainda pode ser
         apresentavel: diz o que acontece a seguir e da uma saida de verdade,
         em vez de anunciar um defeito para quem esta do outro lado. */
      bookSlot.innerHTML = '';
      var aviso = document.createElement('div');
      aviso.className = 'book__off';
      aviso.innerHTML =
        '<b>One more step, and it is on our side</b>' +
        '<p>Send us your request and a RefreshU advisor comes back within one ' +
        'business day with the times available for your call, in your own time zone.</p>';
      var a = document.createElement('a');
      a.className = 'btn';
      a.href = 'mailto:' + (CFG.bookingFallbackEmail || '') +
               '?subject=' + encodeURIComponent('Book my RefreshU call');
      a.textContent = 'Send my request';
      aviso.appendChild(a);

      var nota = document.createElement('p');
      nota.className = 'book__offnote';
      nota.textContent = 'Live scheduling, with instant confirmation, goes live once the RefreshU calendar is connected.';
      aviso.appendChild(nota);

      bookSlot.appendChild(aviso);
      bookSlot.dataset.pronto = '1';
      return;
    }

    var f = document.createElement('iframe');
    f.src = url;
    f.title = 'Choose a time for your RefreshU call';
    f.width = '100%';
    f.height = '640';
    f.frameBorder = '0';
    f.style.border = '0';
    f.loading = 'lazy';
    bookSlot.innerHTML = '';
    bookSlot.appendChild(f);

    // Quem preferir a aba do Google, ou estiver num navegador que bloqueia o
    // iframe de terceiro, ainda tem por onde ir.
    var fora = document.createElement('a');
    fora.className = 'book__out';
    fora.href = url;
    fora.target = '_blank';
    fora.rel = 'noopener';
    fora.textContent = 'Open the calendar in a new tab';
    bookSlot.appendChild(fora);

    bookSlot.dataset.pronto = '1';
  }

  if (bookAck) {
    bookAck.addEventListener('change', function () {
      state.ack = bookAck.checked;
      state.ackAt = bookAck.checked ? new Date().toISOString() : null;
      state.ackDoc = bookAck.dataset.doc;
      state.ackVersion = bookAck.dataset.version;
      save();
    });
  }

  /* --------------------------------------------------------- avancar ---- */

  // O botao so libera quando a etapa esta completa. Impedir de avancar e
  // melhor que deixar avancar e reclamar depois.
  function gate() {
    var ok = true;
    if (step === 1) ok = REQUIRED.every(function (id) { return valid(id, true); });
    if (step === 2) ok = !!state.proc;
    next.disabled = !ok;
  }

  next.addEventListener('click', function () {
    if (step === 1) {
      var bad = REQUIRED.filter(function (id) { return !valid(id); });
      if (bad.length) { field(bad[0]).focus(); return; }
    }
    if (step === LAST) return;
    save();
    go(step + 1);
  });

  back.addEventListener('click', function () { go(step - 1); });

  /* ---------------------------------------------------------- retomar --- */

  // Volta o rascunho para a tela e retoma na primeira etapa incompleta.
  (function resume() {
    if (state.area) {
      var pick = document.querySelector('.pick[data-area="' + state.area + '"]');
      if (pick) pick.setAttribute('aria-pressed', 'true');
    }
    if (state.comp) {
      var c = document.querySelector('[data-comp="' + state.comp + '"]');
      if (c) c.setAttribute('aria-pressed', 'true');
    }
    if (state.ack && bookAck) bookAck.checked = true;

    var at = 1;
    if (REQUIRED.every(function (id) { return valid(id, true); })) at = 2;
    if (state.proc) at = 3;

    go(at);
  })();

})();
