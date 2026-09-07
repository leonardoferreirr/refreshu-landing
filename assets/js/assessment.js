/* ==========================================================================
   RefreshU · Start My Assessment

   Cinco telas, o Anexo A.5.2. Tres delas coletam, a quarta encaminha e a
   quinta confirma. Salvar e retomar guarda o rascunho no proprio navegador,
   como pede o A.5.2; em producao o rascunho vive no servidor, atado a conta,
   e este armazenamento vira so um espelho para quem ainda nao criou conta.

   Nenhum campo clinico existe neste arquivo, e isso e proposital: a Clausula
   12.6 nao e uma validacao que se possa desligar, e a ausencia do campo.
   ========================================================================== */

(function () {
  'use strict';

  var KEY = 'refreshu.assessment.v1';
  var LAST = 5;

  var panels = document.querySelectorAll('[data-panel]');
  var steps = document.querySelectorAll('.as__step');
  var next = document.getElementById('next');
  var back = document.getElementById('back');
  var foot = document.getElementById('foot');
  var saved = document.getElementById('saved');
  var procs = document.getElementById('procs');
  var form = document.getElementById('aboutForm');
  var handoff = document.getElementById('handoffDone');
  var handoffAck = document.getElementById('handoffAck');
  var locCountry = document.getElementById('locCountry');
  var locState = document.getElementById('locState');
  var locStateWrap = document.getElementById('locStateWrap');
  var locBlock = document.getElementById('locBlock');

  // Restricoes por estado. Fica vazio de proposito: quem decide o que um
  // medico brasileiro pode revisar com o paciente fisicamente nos Estados
  // Unidos e o juridico, nao o codigo. O admin liga cada estado quando a
  // orientacao chegar, e a mensagem vem junto.
  var STATE_RULES = {};   // ex.: { 'California': 'message shown to the client' }

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

    back.hidden = step === 1 || step === LAST;
    foot.hidden = step === LAST;

    if (step === 2) paintProcs();
    if (step === 4) { paintDoctor(); paintLocation(); }
    if (step === 5) { paintRecap(); save(); }

    next.textContent = step === 3 ? 'Continue' : (step === 4 ? 'Send my assessment' : 'Continue');

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
      save();
      gate();
    });
  });

  /* ---------------------------------------------- 2. procedimento ------- */

  function paintProcs() {
    var cat = CATALOGUE[state.area];
    if (!cat) return;

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

  /* --------------------------------------------------- 4. hand-off ------ */

  function paintDoctor() {
    var cat = CATALOGUE[state.area];
    if (!cat) return;
    document.getElementById('docAv').textContent = cat.doctor.initials;
    document.getElementById('docName').textContent = cat.doctor.name;
    document.getElementById('docMeta').textContent = cat.doctor.meta;
  }

  if (handoff) {
    handoff.addEventListener('change', function () {
      state.handoff = handoff.checked;
      save();
    });
  }

  /* ------------------------------------------------ localizacao fisica --
     O endereco residencial nao responde a pergunta que importa: onde a
     pessoa esta quando o medico revisa o caso. A resposta e guardada com
     o evento de encaminhamento.                                          */

  function inUS() { return locCountry && locCountry.value === 'United States'; }

  function locationOk() {
    if (!locCountry) return true;
    if (!locCountry.value) return false;
    if (inUS() && !locState.value) return false;
    if (inUS() && STATE_RULES[locState.value]) return false;   // estado bloqueado
    return true;
  }

  function paintLocation() {
    if (!locCountry) return;
    var us = inUS();
    if (locStateWrap) locStateWrap.hidden = !us;
    if (locState) locState.required = us;

    var rule = us && locState.value ? STATE_RULES[locState.value] : null;
    if (locBlock) {
      locBlock.hidden = !rule;
      locBlock.textContent = rule || '';
    }
    state.locCountry = locCountry.value;
    state.locState = us ? locState.value : '';
    gate();
  }

  if (locCountry) locCountry.addEventListener('change', paintLocation);
  if (locState) locState.addEventListener('change', paintLocation);
  if (handoffAck) handoffAck.addEventListener('change', function () {
    state.ack = handoffAck.checked;
    state.ackAt = handoffAck.checked ? new Date().toISOString() : null;
    state.ackDoc = handoffAck.dataset.doc;
    state.ackVersion = handoffAck.dataset.version;
    gate();
  });

  /* -------------------------------------------------- 5. confirmado ----- */

  function paintRecap() {
    var put = function (id, v) { document.getElementById(id).textContent = v || 'Not given'; };
    put('rName', [state.fname, state.lname].filter(Boolean).join(' '));
    put('rMail', state.mail);
    put('rArea', state.areaLabel);
    put('rProc', state.procName);
    put('rState', state.state);
    put('rWindow', state.window);
    put('rComp', state.compLabel || 'Not answered');
    put('rLoc', [state.locState, state.locCountry].filter(Boolean).join(', '));
    put('rHandoff', state.handoff ? 'Marked as completed' : 'Still to complete');
  }

  /* --------------------------------------------------------- avancar ---- */

  // O botao so libera quando a etapa esta completa. Impedir de avancar e
  // melhor que deixar avancar e reclamar depois.
  function gate() {
    var ok = true;
    if (step === 1) ok = !!state.area;
    if (step === 2) ok = !!state.proc;
    if (step === 3) ok = REQUIRED.every(function (id) { return valid(id, true); });
    if (step === 4) ok = locationOk() && !!(handoffAck && handoffAck.checked);
    next.disabled = !ok;
  }

  next.addEventListener('click', function () {
    if (step === 3) {
      var bad = REQUIRED.filter(function (id) { return !valid(id); });
      if (bad.length) { field(bad[0]).focus(); return; }
    }
    if (step === LAST) return;

    if (step === 4) {
      next.disabled = true;
      next.textContent = 'Sending…';
      setTimeout(function () { go(5); }, 500);
      return;
    }

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
    if (state.handoff && handoff) handoff.checked = true;
    if (state.ack && handoffAck) handoffAck.checked = true;
    if (state.locCountry && locCountry) locCountry.value = state.locCountry;
    if (state.locState && locState) locState.value = state.locState;

    var at = 1;
    if (state.area) at = 2;
    if (state.proc) at = 3;
    if (REQUIRED.every(function (id) { return valid(id, true); })) at = 4;

    go(at);
  })();

})();
