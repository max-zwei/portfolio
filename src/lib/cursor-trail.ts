const TRAIL_LENGTH = 42;
const DECAY_MS = 30;
// The native 20,20 hotspot is clamped to the 16×16 asset's last pixel.
const HOTSPOT = 15;

let dispose: (() => void) | undefined;

function initializeCursorTrail() {
  if (dispose) return;

  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const listeners = new AbortController();
  const overlay = document.createElement('div');
  overlay.className = 'cursor-trail';
  overlay.setAttribute('aria-hidden', 'true');
  const marks = Array.from({ length: TRAIL_LENGTH }, () => {
    const mark = document.createElement('span');
    mark.hidden = true;
    overlay.append(mark);
    return mark;
  });
  document.body.append(overlay);

  let oldest = 0;
  let count = 0;
  let lastX = Number.NaN;
  let lastY = Number.NaN;
  let timer: number | undefined;
  let enabled = false;

  function stopTimer() {
    if (timer === undefined) return;
    window.clearInterval(timer);
    timer = undefined;
  }

  function clear() {
    stopTimer();
    for (const mark of marks) mark.hidden = true;
    oldest = 0;
    count = 0;
    lastX = Number.NaN;
    lastY = Number.NaN;
  }

  function updatePreference() {
    enabled = finePointer.matches && !reducedMotion.matches;
    if (!enabled) clear();
  }

  function decay() {
    marks[oldest].hidden = true;
    oldest = (oldest + 1) % TRAIL_LENGTH;
    count -= 1;
    if (count === 0) stopTimer();
  }

  function move(event: PointerEvent) {
    if (!enabled || document.hidden || event.pointerType === 'touch') return;
    const { clientX: x, clientY: y } = event;
    if (x === lastX && y === lastY) return;
    lastX = x;
    lastY = y;

    const mark = marks[(oldest + count) % TRAIL_LENGTH];
    mark.style.transform = `translate(${x - HOTSPOT}px, ${y - HOTSPOT}px)`;
    mark.hidden = false;
    if (count === TRAIL_LENGTH) {
      oldest = (oldest + 1) % TRAIL_LENGTH;
    } else {
      count += 1;
    }
    if (timer === undefined) timer = window.setInterval(decay, DECAY_MS);
  }

  const options = { signal: listeners.signal };
  window.addEventListener('pointermove', move, { ...options, passive: true });
  window.addEventListener(
    'pointerout',
    (event) => {
      if (event.relatedTarget === null) clear();
    },
    options,
  );
  window.addEventListener('blur', clear, options);
  document.addEventListener(
    'visibilitychange',
    () => {
      if (document.hidden) clear();
    },
    options,
  );
  finePointer.addEventListener('change', updatePreference, options);
  reducedMotion.addEventListener('change', updatePreference, options);
  updatePreference();

  dispose = () => {
    clear();
    listeners.abort();
    overlay.remove();
    dispose = undefined;
  };
}

window.addEventListener('pagehide', () => dispose?.());
window.addEventListener('pageshow', initializeCursorTrail);
initializeCursorTrail();
