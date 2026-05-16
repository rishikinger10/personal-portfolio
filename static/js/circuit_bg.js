// animated pcb-trace background
// idea: spawn "pulses" that crawl along a grid like signals on copper traces.
// they only turn in 45/90 degree steps so it actually looks like a circuit board
// and not generic particle soup.

(function () {
  const canvas = document.getElementById('pcb-canvas');
  const ctx = canvas.getContext('2d');

  let w, h;
  const GRID = 26;            // trace spacing, px
  const MAX_PULSES = 26;      // more than this tanks the fps on my laptop
  const TRAIL = 34;           // how many segments a pulse remembers

  const pulses = [];
  let mouseX = -9999, mouseY = -9999;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  window.addEventListener('mousemove', function (e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // directions restricted to the 8 compass points, weighted so pulses
  // mostly go straight and occasionally do the classic 45-degree pcb bend
  const DIRS = [
    [1, 0], [-1, 0], [0, 1], [0, -1],
    [1, 1], [1, -1], [-1, 1], [-1, -1],
  ];

  function spawnPulse() {
    // start from a random edge so they flow across the screen
    const edge = Math.floor(Math.random() * 4);
    let gx, gy;
    if (edge === 0) { gx = 0; gy = Math.floor(Math.random() * (h / GRID)); }
    else if (edge === 1) { gx = Math.floor(w / GRID); gy = Math.floor(Math.random() * (h / GRID)); }
    else if (edge === 2) { gx = Math.floor(Math.random() * (w / GRID)); gy = 0; }
    else { gx = Math.floor(Math.random() * (w / GRID)); gy = Math.floor(h / GRID); }

    pulses.push({
      x: gx, y: gy,
      dir: DIRS[Math.floor(Math.random() * 4)], // start orthogonal, looks cleaner
      trail: [],
      hue: Math.random() < 0.82 ? 160 : 38,     // mostly teal, sometimes amber
      speed: 0.35 + Math.random() * 0.5,
      acc: 0,
      life: 220 + Math.random() * 260,
    });
  }

  function stepPulse(p) {
    p.life--;
    p.acc += p.speed;
    if (p.acc < 1) return;
    p.acc = 0;

    p.trail.push([p.x, p.y]);
    if (p.trail.length > TRAIL) p.trail.shift();

    // small chance to bend; bends are what sell the pcb look
    if (Math.random() < 0.14) {
      const cur = p.dir;
      const options = DIRS.filter(function (d) {
        // no u-turns, no repeating current dir
        return !(d[0] === -cur[0] && d[1] === -cur[1]) && !(d[0] === cur[0] && d[1] === cur[1]);
      });
      p.dir = options[Math.floor(Math.random() * options.length)];
    }

    p.x += p.dir[0];
    p.y += p.dir[1];
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);

    // faint dot grid, like unpopulated pads
    ctx.fillStyle = 'rgba(94, 234, 212, 0.05)';
    for (let x = 0; x < w; x += GRID * 2) {
      for (let y = 0; y < h; y += GRID * 2) {
        ctx.fillRect(x, y, 1.5, 1.5);
      }
    }

    for (let i = pulses.length - 1; i >= 0; i--) {
      const p = pulses[i];
      stepPulse(p);

      if (p.life <= 0 || p.x < -2 || p.y < -2 || p.x * GRID > w + 50 || p.y * GRID > h + 50) {
        pulses.splice(i, 1);
        continue;
      }

      // trail segments fade out toward the tail
      for (let j = 1; j < p.trail.length; j++) {
        const a = p.trail[j - 1], b = p.trail[j];
        const alpha = (j / p.trail.length) * 0.5;
        ctx.strokeStyle = 'hsla(' + p.hue + ', 80%, 62%, ' + alpha + ')';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(a[0] * GRID, a[1] * GRID);
        ctx.lineTo(b[0] * GRID, b[1] * GRID);
        ctx.stroke();
      }

      // the pulse head glows, brighter when the cursor is nearby
      const px = p.x * GRID, py = p.y * GRID;
      const dx = px - mouseX, dy = py - mouseY;
      const near = Math.sqrt(dx * dx + dy * dy) < 160;

      ctx.shadowBlur = near ? 18 : 8;
      ctx.shadowColor = 'hsla(' + p.hue + ', 90%, 65%, 0.9)';
      ctx.fillStyle = 'hsla(' + p.hue + ', 95%, ' + (near ? 78 : 66) + '%, 1)';
      ctx.beginPath();
      ctx.arc(px, py, near ? 3 : 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    if (pulses.length < MAX_PULSES && Math.random() < 0.3) spawnPulse();

    requestAnimationFrame(draw);
  }

  // seed a few so the page doesn't start empty
  for (let i = 0; i < 10; i++) spawnPulse();
  draw();
})();
