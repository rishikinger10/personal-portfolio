// pulls everything from the flask api and renders the page.
// kept it framework-free on purpose - it's a portfolio, not a startup.

const ROLES = [
  'Embedded Systems',
  'Linux Device Drivers',
  'Computer Vision @ the Edge',
  'Socket Programming',
  'Electronics & Instrumentation',
];

// --- typing effect for the hero -------------------------------------------

function startTyper() {
  const el = document.getElementById('typed-text');
  let roleIdx = 0, charIdx = 0, deleting = false;

  function tick() {
    const word = ROLES[roleIdx];

    if (!deleting) {
      charIdx++;
      el.textContent = word.slice(0, charIdx);
      if (charIdx === word.length) {
        deleting = true;
        setTimeout(tick, 1700); // let people actually read it
        return;
      }
      setTimeout(tick, 55 + Math.random() * 45); // uneven typing feels more human
    } else {
      charIdx--;
      el.textContent = word.slice(0, charIdx);
      if (charIdx === 0) {
        deleting = false;
        roleIdx = (roleIdx + 1) % ROLES.length;
      }
      setTimeout(tick, 28);
    }
  }
  tick();
}

// --- rendering helpers -----------------------------------------------------

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text) node.textContent = text;
  return node;
}

async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(url + ' -> ' + res.status);
  return res.json();
}

// --- section renderers ------------------------------------------------------

function renderProfile(p) {
  document.getElementById('hero-name').textContent = p.full_name;
  document.getElementById('hero-tagline').textContent = p.tagline;
  document.getElementById('about-text').textContent = p.about;
  document.getElementById('edu-text').textContent = p.education;
  document.getElementById('cgpa-val').textContent = p.cgpa;
  document.getElementById('hero-meta').textContent =
    p.location + '  ·  ' + p.email;
  document.getElementById('footer-contact').textContent = p.email + ' · ' + p.phone;
}

function renderSkills(groups) {
  const grid = document.getElementById('skills-grid');
  groups.forEach(function (g) {
    const card = el('div', 'skill-card');
    // little "IC chip" header, matches the pcb theme
    card.appendChild(el('div', 'skill-cat mono', g.category));
    const wrap = el('div', 'chip-wrap');
    g.items.forEach(function (item) {
      wrap.appendChild(el('span', 'chip', item));
    });
    card.appendChild(wrap);
    grid.appendChild(card);
  });
}

function renderProjects(projects) {
  const grid = document.getElementById('projects-grid');
  projects.forEach(function (p, i) {
    const card = el('article', 'project-card');
    card.style.setProperty('--delay', (i * 90) + 'ms');

    const head = el('div', 'proj-head');
    head.appendChild(el('span', 'proj-index mono', String(i + 1).padStart(2, '0')));
    head.appendChild(el('h4', null, p.title));
    card.appendChild(head);

    card.appendChild(el('p', 'proj-summary', p.summary));

    const ul = el('ul', 'proj-points');
    p.highlights.forEach(function (h) {
      ul.appendChild(el('li', null, h));
    });
    card.appendChild(ul);

    const stack = el('div', 'proj-stack mono');
    p.stack.forEach(function (s) {
      stack.appendChild(el('span', 'stack-tag', s));
    });
    card.appendChild(stack);

    grid.appendChild(card);
  });
}

function renderExperience(entries) {
  const timeline = document.getElementById('exp-timeline');
  entries.forEach(function (e) {
    const item = el('div', 'tl-item');
    item.appendChild(el('div', 'tl-dot'));
    const body = el('div', 'tl-body');
    body.appendChild(el('div', 'tl-period mono', e.period));
    body.appendChild(el('h4', null, e.role + ' · ' + e.org));
    const ul = el('ul', 'proj-points');
    e.bullets.forEach(function (b) { ul.appendChild(el('li', null, b)); });
    body.appendChild(ul);
    item.appendChild(body);
    timeline.appendChild(item);
  });
}

// --- contact form ------------------------------------------------------------

function wireContactForm() {
  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-status');

  // the github pages copy has no backend, so there the form just opens mail
  if (document.body.dataset.static) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      const fd = new FormData(form);
      const subject = 'portfolio contact from ' + (fd.get('name') || fd.get('email'));
      location.href = 'mailto:rishikinger10@gmail.com'
        + '?subject=' + encodeURIComponent(subject)
        + '&body=' + encodeURIComponent(fd.get('message'));
    });
    return;
  }

  form.addEventListener('submit', async function (ev) {
    ev.preventDefault();
    status.textContent = 'transmitting...';
    status.className = 'mono';

    const fd = new FormData(form);
    try {
      const res = await fetch('api/contact.json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: fd.get('name'),
          email: fd.get('email'),
          message: fd.get('message'),
        }),
      });
      const data = await res.json();
      if (data.ok) {
        status.textContent = 'ACK ✓ message received';
        status.classList.add('ok');
        form.reset();
      } else {
        status.textContent = 'NAK ✗ ' + (data.error || 'something broke');
        status.classList.add('err');
      }
    } catch (e) {
      status.textContent = 'NAK ✗ server unreachable';
      status.classList.add('err');
    }
  });
}

// --- scroll reveal ------------------------------------------------------------

function setupReveal() {
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.panel, .project-card, .skill-card, .tl-item')
    .forEach(function (n) { observer.observe(n); });
}

// --- boot ----------------------------------------------------------------------

async function boot() {
  // ?noanim kills the reveal animations - useful for screenshots/debugging
  if (location.search.indexOf('noanim') !== -1) {
    document.documentElement.classList.add('no-anim');
  }

  startTyper();
  wireContactForm();

  try {
    // fire all four at once, no reason to waterfall
    const [profile, skills, projects, experience] = await Promise.all([
      getJSON('api/profile.json'),
      getJSON('api/skills.json'),
      getJSON('api/projects.json'),
      getJSON('api/experience.json'),
    ]);

    renderProfile(profile);
    renderSkills(skills);
    renderProjects(projects);
    renderExperience(experience);
  } catch (err) {
    console.error('api load failed:', err);
    document.getElementById('about-text').textContent =
      'Backend seems to be down. Run python app.py and refresh.';
  }

  // observe after content exists, otherwise cards never reveal
  setupReveal();
}

boot();
