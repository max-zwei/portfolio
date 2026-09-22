/*
 * The artefact strip scrolls itself until the visitor takes it over.
 *
 * Motion the Figma file does not define — requested directly: an endless
 * 40 px/s drift, latched off by any deliberate interaction. It drives
 * `scrollLeft` rather than a CSS transform because the strip is already a
 * native scroller: a transformed track would fight the visitor's own
 * scrolling, and CSS cannot latch a pause. `global.css`'s reduced-motion
 * blanket covers CSS duration only, so this checks the query itself.
 */
const SPEED = 40; // px per second

const still = matchMedia('(prefers-reduced-motion: reduce)');

document
  .querySelectorAll<HTMLElement>('[data-artefact-strip]')
  .forEach((strip) => {
    const items = Array.from(strip.children) as HTMLElement[];
    if (items.length === 0) return;

    /** Set by a deliberate interaction. Never cleared: the pause is final. */
    let latched = false;
    let hovered = false;
    let onScreen = false;
    let built = false;
    let frame = 0;
    let last = 0;
    /** Own float accumulator — `scrollLeft` reads back rounded. */
    let pos = 0;
    /** Distance from an item to its own copy: one seamless lap. */
    let period = 0;

    const addCopy = () => {
      for (const item of items) {
        const copy = item.cloneNode(true) as HTMLElement;
        copy.setAttribute('aria-hidden', 'true');
        copy.dataset.artefactClone = 'true';
        // A lazy copy would pop in mid-lap; it is one viewport away.
        copy.querySelector('img')?.setAttribute('loading', 'eager');
        strip.append(copy);
      }
    };

    /** One lap, plus enough copies that a lap never hits the scroll end. */
    const measure = () => {
      const copy = strip.children[items.length] as HTMLElement | undefined;
      if (!copy) return;
      period = copy.offsetLeft - items[0].offsetLeft;
      while (period > 0 && strip.scrollWidth - strip.clientWidth < period) {
        addCopy();
      }
    };

    const build = () => {
      // A strip that fits has nothing to scroll.
      if (built || strip.scrollWidth - strip.clientWidth <= 1) return;
      pos = strip.scrollLeft;
      addCopy();
      measure();
      built = true;
      io.observe(strip);
    };

    const teardown = () => {
      if (!built) return;
      built = false;
      io.unobserve(strip);
      cancelAnimationFrame(frame);
      frame = 0;
      for (const copy of strip.querySelectorAll('[data-artefact-clone]')) {
        copy.remove();
      }
      period = 0;
      pos = 0;
      strip.scrollLeft = 0;
    };

    const step = (now: number) => {
      frame = requestAnimationFrame(step);
      if (!last) {
        last = now;
        return;
      }
      const dt = Math.min(now - last, 100);
      last = now;
      // Wrapping by one lap lands on an identical copy: no visible seam.
      pos = (pos + (SPEED * dt) / 1000) % period;
      strip.scrollLeft = pos;
    };

    const sync = () => {
      const run =
        built &&
        period > 0 &&
        onScreen &&
        !latched &&
        !hovered &&
        !still.matches &&
        document.visibilityState === 'visible';

      if (run && !frame) {
        last = 0;
        frame = requestAnimationFrame(step);
      } else if (!run && frame) {
        cancelAnimationFrame(frame);
        frame = 0;
      }
    };

    const io = new IntersectionObserver((entries) => {
      for (const entry of entries) onScreen = entry.isIntersecting;
      sync();
    });

    // Images carry width and height, so a lap only changes length when the
    // container does — `img { max-width: 100% }` shrinks them on narrow
    // viewports.
    new ResizeObserver(() => {
      if (still.matches) return;
      if (!built) {
        build();
        sync();
        return;
      }
      measure();
      if (strip.clientWidth >= period) {
        teardown();
        return;
      }
      pos %= period;
    }).observe(strip);

    for (const type of [
      'pointerdown',
      'wheel',
      'touchstart',
      'keydown',
      'focusin',
    ]) {
      strip.addEventListener(
        type,
        () => {
          latched = true;
          sync();
        },
        { passive: true },
      );
    }

    strip.addEventListener('mouseenter', () => {
      hovered = true;
      sync();
    });
    strip.addEventListener('mouseleave', () => {
      hovered = false;
      sync();
    });

    document.addEventListener('visibilitychange', sync);

    still.addEventListener('change', () => {
      if (still.matches) teardown();
      else build();
      sync();
    });

    if (!still.matches) build();
  });
