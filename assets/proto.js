// Shared milestones prototype. Everything here is local to the page: nothing is stored or sent.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var TODAY = new Date(2026, 10, 22);
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // A made-up initiative. Six projects, four milestones.
  var P = [
    { id: 'sync', name: 'Sync engine', team: 'Platform', key: 'SYN' },
    { id: 'ios', name: 'iOS app', team: 'Mobile', key: 'IOS' },
    { id: 'and', name: 'Android app', team: 'Mobile', key: 'AND' },
    { id: 'web', name: 'Web app', team: 'Web', key: 'WEB' },
    { id: 'bill', name: 'Billing', team: 'Growth', key: 'BIL' },
    { id: 'docs', name: 'Help docs', team: 'Support', key: 'DOC' }
  ];
  var M = [
    { id: 'a', name: 'Alpha', date: '2026-09-14' },
    { id: 'b', name: 'Beta', date: '2026-10-26' },
    { id: 'l', name: 'Launch', date: '2026-12-07' },
    { id: 'p', name: 'After launch', date: null }
  ];
  // [project, title, state (d done, s in progress, t to do), path: every milestone the issue has been in, in order]
  var RAW = [
    ['sync', 'Queue writes while offline', 'd', 'a'],
    ['sync', 'Replay the queue on reconnect', 'd', 'a'],
    ['sync', 'Detect conflicting edits', 'd', 'ab'],
    ['sync', 'Merge rules for text fields', 'd', 'b'],
    ['sync', 'Retry with backoff', 'd', 'b'],
    ['sync', 'Resolve conflicts on attachments', 's', 'b'],
    ['sync', 'Cap the local store size', 't', 'abl'],
    ['sync', 'Sync status in the API', 's', 'bl'],
    ['sync', 'Load test with a long offline queue', 't', 'l'],
    ['sync', 'Migrate existing sessions', 't', 'l'],
    ['sync', 'Delta sync for large documents', 't', 'p'],
    ['ios', 'Local store on device', 'd', 'a'],
    ['ios', 'Offline banner', 'd', 'a'],
    ['ios', 'Edit issues offline', 'd', 'b'],
    ['ios', 'Create issues offline', 'd', 'b'],
    ['ios', 'Attachments offline', 's', 'b'],
    ['ios', 'Background sync', 't', 'b'],
    ['ios', 'Conflict sheet', 's', 'abl'],
    ['ios', 'Widget shows stale state', 't', 'bl'],
    ['ios', 'App Store notes and screenshots', 't', 'l'],
    ['ios', 'Crash-free rate check', 't', 'l'],
    ['and', 'Local store on device', 'd', 'a'],
    ['and', 'Offline banner', 'd', 'ab'],
    ['and', 'Edit issues offline', 'd', 'b'],
    ['and', 'Create issues offline', 's', 'b'],
    ['and', 'Background sync', 't', 'bl'],
    ['and', 'Conflict sheet', 't', 'bl'],
    ['and', 'Play Store listing', 't', 'l'],
    ['web', 'Service worker cache', 'd', 'a'],
    ['web', 'Offline indicator in the header', 'd', 'a'],
    ['web', 'Edit issues offline', 'd', 'b'],
    ['web', 'Queue comments', 'd', 'b'],
    ['web', 'Stale tab warning', 'd', 'b'],
    ['web', 'Keyboard shortcuts while offline', 's', 'l'],
    ['web', 'Settings page for storage', 't', 'l'],
    ['web', 'Clear local data', 't', 'p'],
    ['bill', 'Plan gate for offline mode', 'd', 'b'],
    ['bill', 'Usage event for synced writes', 's', 'bl'],
    ['bill', 'Pricing page copy', 't', 'l'],
    ['docs', 'Offline mode guide', 's', 'l'],
    ['docs', 'Troubleshooting sync', 't', 'l'],
    ['docs', 'Changelog entry', 't', 'l']
  ];
  var STATE = { d: 'Done', s: 'In progress', t: 'To do' };

  var seq = {};
  var ISSUES = RAW.map(function (r) {
    var p = P.filter(function (x) { return x.id === r[0]; })[0];
    seq[p.id] = (seq[p.id] || 10) + 1;
    return { id: p.key + '-' + seq[p.id], p: p.id, title: r[1], state: r[2], path: r[3].split('') };
  });
  // A project can join a milestone before it has any issues there.
  var joined = { 'bill|p': true };

  var view = { p: 1, m: 1, row: -1, zone: null, carried: false };
  var undo = [];
  var rows = []; // issues listed in the panel, in order

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mi(id) { for (var i = 0; i < M.length; i++) if (M[i].id === id) return i; return -1; }
  function fmt(d) { if (!d) return ''; var x = d.split('-'); return MONTHS[+x[1] - 1] + ' ' + (+x[2]); }
  function plural(n, one, many) { return n + ' ' + (n === 1 ? one : many); }
  function last(i) { return i.path[i.path.length - 1]; }

  // Everything known about one project's part of one milestone.
  function slice(p, m) {
    var mine = ISSUES.filter(function (i) { return i.p === p.id && i.path.indexOf(m.id) > -1; });
    var now = mine.filter(function (i) { return last(i) === m.id; });
    return {
      member: mine.length > 0 || !!joined[p.id + '|' + m.id],
      now: now,
      done: now.filter(function (i) { return i.state === 'd'; }).length,
      inn: mine.filter(function (i) { return i.path.indexOf(m.id) > 0; }),
      on: mine.filter(function (i) { return last(i) !== m.id; })
    };
  }
  function column(m) {
    var c = { now: 0, done: 0, inn: 0, on: 0, by: [], members: 0, twice: 0 };
    P.forEach(function (p) {
      var s = slice(p, m);
      if (s.member) c.members++;
      c.now += s.now.length; c.done += s.done; c.inn += s.inn.length; c.on += s.on.length;
      if (s.on.length) c.by.push(p.name + ' ' + s.on.length);
      c.twice += s.on.filter(function (i) { return i.path.length > 2; }).length;
    });
    c.open = c.now - c.done;
    return c;
  }
  // Done, overdue, next or later. A milestone with no issues gets no verdict.
  function verdict(m) {
    var c = column(m);
    if (!c.now) return { k: 'quiet', t: 'No issues yet' };
    if (!c.open) return { k: 'ok', t: 'Done' };
    if (m.date && new Date(m.date + 'T00:00:00') < TODAY) return { k: 'none', t: 'Overdue' };
    var firstOpen = M.filter(function (x) { var cc = column(x); return cc.open && !(x.date && new Date(x.date + 'T00:00:00') < TODAY); })[0];
    return firstOpen === m ? { k: 'move', t: 'Next' } : { k: 'quiet', t: 'Later' };
  }

  function headHTML(x) {
    var m = M[x], c = column(m), v = verdict(m);
    return '<b>' + esc(m.name) + '</b>'
      + '<button class="mdate" type="button" data-date="' + x + '" aria-label="' + esc(m.name) + ' date: ' + (m.date ? fmt(m.date) : 'none') + '. Change it for every project.">' + (m.date ? fmt(m.date) : 'Set a date') + '</button>'
      + '<span class="st ' + v.k + '">' + v.t + '</span>'
      + '<small>' + (c.now ? c.done + ' of ' + c.now + ' done' : 'Nothing planned') + '</small>';
  }
  function renderHead() { M.forEach(function (m, x) { var el = $('mh' + x); el.innerHTML = headHTML(x); el.className = 'mh' + (x === view.m ? ' on' : ''); }); }
  function renderGrid() {
    var h = '<div role="row" class="srow"><div class="scorner" role="columnheader"><span>Project</span></div>';
    M.forEach(function (m, x) { h += '<div class="mh' + (x === view.m ? ' on' : '') + '" role="columnheader" id="mh' + x + '">' + headHTML(x) + '</div>'; });
    h += '</div>';
    P.forEach(function (p, y) {
      h += '<div role="row" class="srow"><div class="prow" role="rowheader"><b>' + esc(p.name) + '</b><span>' + esc(p.team) + '</span></div>';
      M.forEach(function (m, x) {
        var s = slice(p, m), sel = y === view.p && x === view.m, body, label = p.name + ', ' + m.name + ': ';
        if (!s.member) {
          body = '<span class="out">Not in this milestone</span>'; label += 'not in this milestone.';
        } else if (view.carried) {
          body = s.inn.length || s.on.length
            ? (s.on.length ? '<span class="n">' + s.on.length + '</span><span class="cn">carried on</span>' : '<span class="n dim">0</span><span class="cq">carried on</span>')
              + (s.inn.length ? '<span class="cn in">' + s.inn.length + ' carried in</span>' : '')
            : '<span class="dash">&ndash;</span><span class="cq">Nothing carried</span>';
          label += s.on.length + ' carried on, ' + s.inn.length + ' carried in.';
        } else if (!s.now.length && !s.on.length) {
          body = '<span class="dash">&ndash;</span><span class="cq">No issues yet</span>'; label += 'no issues yet.';
        } else {
          body = (s.now.length
              ? '<span class="n">' + s.done + '<small> of ' + s.now.length + '</small></span><span class="pb"><i style="width:' + (100 * s.done / s.now.length) + '%"></i></span>'
              : '<span class="dash">&ndash;</span><span class="cq">All moved on</span>')
            + (s.inn.length ? '<span class="cn in">' + s.inn.length + ' carried in</span>' : '')
            + (s.on.length ? '<span class="cn">' + s.on.length + ' carried on</span>' : '');
          label += s.done + ' of ' + s.now.length + ' done, ' + s.inn.length + ' carried in, ' + s.on.length + ' carried on.';
        }
        h += '<button type="button" role="gridcell" class="sc' + (s.member ? '' : ' off') + '" data-p="' + y + '" data-m="' + x + '" aria-selected="' + sel + '" tabindex="' + (sel ? 0 : -1) + '" aria-label="' + esc(label) + '">' + body + '</button>';
      });
      h += '</div>';
    });
    $('grid').innerHTML = h;
  }

  function tag(i, m) {
    var t = '', at = i.path.indexOf(m.id);
    if (at > 0) t += '<span class="tg in">from ' + esc(M[mi(i.path[at - 1])].name) + '</span>';
    if (last(i) !== m.id) t += '<span class="tg">to ' + esc(M[mi(i.path[at + 1])].name) + '</span>';
    if (i.path.length > 2) t += '<span class="tg tw">moved twice</span>';
    return t;
  }
  function renderPanel() {
    var p = P[view.p], m = M[view.m], s = slice(p, m), next = M[view.m + 1], h;
    rows = [];
    h = '<h3>' + esc(p.name) + '</h3><p class="pm">' + esc(m.name) + (m.date ? ', ' + fmt(m.date) : ', no date') + '</p>';
    if (!s.member) {
      h += '<div class="pe"><p>' + esc(p.name) + ' has no work in ' + esc(m.name) + '.</p><button class="btn sm" type="button" id="join">Add ' + esc(p.name) + ' to ' + esc(m.name) + '</button></div>';
    } else if (!s.now.length && !s.on.length) {
      h += '<div class="pe"><p>' + esc(p.name) + ' shares this milestone and has no issues in it yet.</p><p class="note">It shows a dash, not 100%. Nothing done is not the same as everything done.</p></div>';
    } else {
      var open = s.now.filter(function (i) { return i.state !== 'd'; }), done = s.now.filter(function (i) { return i.state === 'd'; });
      var list = function (title, items, movable) {
        if (!items.length) return '';
        var o = '<h4>' + title + ' <span>' + items.length + '</span></h4><ul>';
        items.forEach(function (i) {
          var n = rows.push({ i: i, movable: movable && !!next }) - 1;
          o += '<li class="ir" tabindex="-1" data-row="' + n + '"><span class="is ' + i.state + '">' + STATE[i.state] + '</span>'
            + '<span class="it"><span class="id">' + i.id + '</span> ' + esc(i.title) + tag(i, m) + '</span>'
            + (movable && next ? '<button class="mv" type="button" data-move="' + n + '" tabindex="-1">Move to ' + esc(next.name) + '</button>' : '')
            + '</li>';
        });
        return o + '</ul>';
      };
      h += list('Open in ' + esc(m.name), open, true);
      if (!open.length && s.now.length) h += '<p class="allok"><span class="st ok">Nothing open</span></p>';
      h += list('Done', done, false) + list('Moved on', s.on, false);
      if (open.length && !next) h += '<p class="note">This is the last milestone. Open work stays here.</p>';
    }
    $('panel').innerHTML = h;
    if (view.row >= rows.length) view.row = rows.length - 1;
  }

  function renderSum() {
    var m = M[view.m], c = column(m), next = M[view.m + 1], prev = M[view.m - 1], t = [];
    $('sumT').textContent = 'What ' + m.name + ' carried over';
    if (!c.now && !c.on) {
      t.push(m.name + (m.date ? ', due ' + fmt(m.date) : ' has no date') + '. No issues yet in any project.');
    } else {
      var past = m.date && new Date(m.date + 'T00:00:00') < TODAY;
      t.push(m.name + (m.date ? (past ? ' was due ' : ' is due ') + fmt(m.date) : ' has no date') + '.');
      t.push(c.now ? c.done + ' of ' + c.now + ' done' + (c.open ? ', ' + c.open + ' still open.' : '.') : 'Nothing is in it now.');
      if (prev) t.push(c.inn ? plural(c.inn, 'issue', 'issues') + ' arrived from earlier milestones.' : 'Nothing arrived from earlier milestones.');
      if (next) t.push(c.on ? plural(c.on, 'issue', 'issues') + ' moved on: ' + c.by.join(', ') + '.' : 'Nothing has moved on.');
      if (c.twice) t.push(plural(c.twice, 'of those has', 'of those have') + ' now moved twice.');
    }
    $('sum').textContent = t.join(' ');
  }

  function say(text) { $('msg').textContent = text; $('undo').disabled = !undo.length; }

  function focusNow() {
    var el;
    if (view.zone === 'panel' && view.row > -1) el = document.querySelector('.ir[data-row="' + view.row + '"]');
    if (!el && view.zone === 'panel') el = $('join');
    if (!el && view.zone) { view.zone = 'grid'; view.row = -1; el = document.querySelector('.sc[aria-selected="true"]'); }
    if (el) el.focus({ preventScroll: false });
  }
  function draw() { renderGrid(); renderPanel(); renderSum(); $('carried').setAttribute('aria-pressed', view.carried); $('allwork').setAttribute('aria-pressed', !view.carried); focusNow(); }

  function select(p, m, zone) {
    view.p = Math.max(0, Math.min(P.length - 1, p)); view.m = Math.max(0, Math.min(M.length - 1, m));
    view.row = -1; view.zone = zone; draw();
  }
  function moveOn(n) {
    var r = rows[n]; if (!r) return;
    var m = M[view.m], next = M[view.m + 1];
    if (r.i.state === 'd') return say('Done work stays in ' + m.name + '.');
    if (last(r.i) !== m.id) return say(r.i.id + ' has already moved on.');
    if (!next) return say(m.name + ' is the last milestone.');
    r.i.path.push(next.id);
    undo.push({ t: 'move', i: r.i });
    view.zone = 'panel'; view.row = n; draw();
    say(r.i.id + ' moved to ' + next.name + '. ' + m.name + ' keeps the record.');
  }
  function join() {
    var p = P[view.p], m = M[view.m];
    joined[p.id + '|' + m.id] = true; undo.push({ t: 'join', k: p.id + '|' + m.id });
    view.zone = 'grid'; draw(); say(p.name + ' now shares ' + m.name + '.');
  }
  function setDate(x, value) {
    var m = M[x]; if ((m.date || '') === (value || '')) return false;
    undo.push({ t: 'date', x: x, prev: m.date }); m.date = value || null;
    var n = column(m).members;
    say(m.name + (m.date ? ' is now ' + fmt(m.date) : ' has no date') + ' in ' + plural(n, 'project', 'projects') + '. One edit.');
    return true;
  }
  function undoLast() {
    var u = undo.pop(), text = 'Nothing to undo.';
    if (u && u.t === 'move') { var to = u.i.path.pop(); text = u.i.id + ' is back in ' + M[mi(last(u.i))].name + ', not ' + M[mi(to)].name + '.'; }
    if (u && u.t === 'join') { delete joined[u.k]; text = 'That project no longer shares the milestone.'; }
    if (u && u.t === 'date') { M[u.x].date = u.prev; text = M[u.x].name + (u.prev ? ' is back to ' + fmt(u.prev) + '.' : ' has no date again.'); }
    if (u) draw();
    say(text);
  }
  // The date is edited in place. Only the header row is redrawn, so a click elsewhere is never lost.
  function editDate(x) {
    var b = document.querySelector('[data-date="' + x + '"]'); if (!b) return;
    var inp = document.createElement('input');
    inp.type = 'date'; inp.className = 'mdin'; inp.value = M[x].date || ''; inp.setAttribute('aria-label', M[x].name + ' date, for every project');
    b.replaceWith(inp); inp.focus();
    var finished = false;
    function finish(save, refocus) {
      if (finished) return; finished = true;
      if (save) setDate(x, inp.value);
      renderHead(); renderSum();
      if (refocus) { var nb = document.querySelector('[data-date="' + x + '"]'); if (nb) nb.focus(); }
    }
    inp.addEventListener('keydown', function (e) {
      e.stopPropagation();
      if (e.key === 'Enter') { e.preventDefault(); finish(true, true); }
      if (e.key === 'Escape') { e.preventDefault(); finish(false, true); }
    });
    inp.addEventListener('blur', function () { finish(true, false); });
  }

  var proto = $('proto');
  proto.addEventListener('click', function (e) {
    var t = e.target.closest('button, .ir'); if (!t) return;
    if (t.classList.contains('sc')) return select(+t.dataset.p, +t.dataset.m, 'grid');
    if (t.hasAttribute('data-date')) return editDate(+t.dataset.date);
    if (t.hasAttribute('data-move')) return moveOn(+t.dataset.move);
    if (t.classList.contains('ir')) { view.zone = 'panel'; view.row = +t.dataset.row; return focusNow(); }
    if (t.id === 'join') return join();
    if (t.id === 'undo') { view.zone = view.zone || 'grid'; return undoLast(); }
    if (t.id === 'carried' || t.id === 'allwork') { view.carried = t.id === 'carried'; view.zone = null; draw(); return t.focus(); }
    if (t.id === 'keysOpen') return $('keys').showModal();
  });
  proto.addEventListener('focusin', function (e) {
    if (e.target.classList.contains('sc')) view.zone = 'grid';
    if (e.target.classList.contains('ir')) { view.zone = 'panel'; view.row = +e.target.dataset.row; }
  });
  proto.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.metaKey || e.ctrlKey || e.altKey) return;
    var k = e.key, inGrid = e.target.classList.contains('sc'), inPanel = !!e.target.closest('#panel');
    var used = true;
    if (inGrid && k === 'ArrowRight') select(view.p, view.m + 1, 'grid');
    else if (inGrid && k === 'ArrowLeft') select(view.p, view.m - 1, 'grid');
    else if (inGrid && k === 'ArrowDown') select(view.p + 1, view.m, 'grid');
    else if (inGrid && k === 'ArrowUp') select(view.p - 1, view.m, 'grid');
    else if (inGrid && k === 'Home') select(view.p, 0, 'grid');
    else if (inGrid && k === 'End') select(view.p, M.length - 1, 'grid');
    else if (inGrid && (k === 'Enter' || k === ' ')) { view.zone = 'panel'; view.row = rows.length ? 0 : -1; focusNow(); }
    else if (inPanel && (k === 'ArrowDown' || k === 'j') && rows.length) { view.row = Math.min(rows.length - 1, view.row + 1); focusNow(); }
    else if (inPanel && (k === 'ArrowUp' || k === 'k') && rows.length) { view.row = Math.max(0, view.row - 1); focusNow(); }
    else if (inPanel && k === 'Escape') { view.zone = 'grid'; view.row = -1; focusNow(); }
    else if (inPanel && (k === 'm' || k === 'M') && view.row > -1) moveOn(view.row);
    else if (k === 'u' || k === 'U') { view.zone = view.zone || 'grid'; undoLast(); }
    else if (k === 'c' || k === 'C') { view.carried = !view.carried; view.zone = view.zone || 'grid'; draw(); }
    else if (k === 'd' || k === 'D') editDate(view.m);
    else if (k === '?') $('keys').showModal();
    else used = false;
    if (used) e.preventDefault();
  });
  $('keysX').addEventListener('click', function () { $('keys').close(); });

  draw();
  say('Nothing moved yet.');
})();
