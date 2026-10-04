/*
 * The artefact strip drifts endlessly at 40 px/s, pausing while the visitor
 * hovers, focuses, or gestures on it. Native `scrollLeft` keeps manual
 * navigation available; each resume starts from the visitor's position.
 * `global.css`'s reduced-motion blanket covers CSS duration only, so this
 * checks the query itself and leaves only the original items when enabled.
 */
const SPEED = 40; // px per second

const still = matchMedia('(prefers-reduced-motion: reduce)');

document
  .querySelectorAll<HTMLElement>('[data-artefact-strip]')
  .forEach((strip) => {
    if (!('IntersectionObserver' in window) || !('ResizeObserver' in window)) {
      return;
    }
    const items = Array.from(strip.children) as HTMLElement[];
    if (items.length === 0) return;

    let hovered = false;
    let pressed = false;
    let touching = false;
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
        copy.inert = true;
        copy.dataset.artefactClone = 'true';
        // A lazy copy would pop in mid-lap; it is one viewport away.
        copy.querySelector('img')?.setAttribute('loading', 'eager');
        strip.append(copy);
      }
    };

    /** One lap, plus enough copies that a lap never hits the scroll end. */
    const measure = () => {
      period = 0;
      if (strip.clientWidth > 0 && strip.clientHeight > 0) {
        const copy = strip.children[items.length] as HTMLElement | undefined;
        if (copy) {
          period = copy.offsetLeft - items[0].offsetLeft;
          while (period > 0 && strip.scrollWidth - strip.clientWidth < period) {
            addCopy();
          }
        }
      }
      pos = strip.scrollLeft;
      sync();
    };

    const build = () => {
      if (built || strip.clientWidth === 0 || strip.clientHeight === 0) return;
      addCopy();
      built = true;
      io.observe(strip);
      measure();
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
        !hovered &&
        !pressed &&
        !touching &&
        !strip.contains(document.activeElement) &&
        !still.matches &&
        document.visibilityState === 'visible';

      if (run && !frame) {
        pos = strip.scrollLeft;
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
      if (!built) build();
      else measure();
    }).observe(strip);

    strip.addEventListener('pointerenter', (event) => {
      if (event.pointerType === 'touch') return;
      hovered = true;
      sync();
    });
    strip.addEventListener('pointerleave', (event) => {
      if (event.pointerType === 'touch') return;
      hovered = false;
      sync();
    });
    strip.addEventListener('pointerdown', () => {
      pressed = true;
      sync();
    });
    const releasePointer = () => {
      pressed = false;
      sync();
    };
    window.addEventListener('pointerup', releasePointer);
    window.addEventListener('pointercancel', releasePointer);

    // Native touch scrolling cancels the pointer before the finger lifts.
    strip.addEventListener(
      'touchstart',
      () => {
        touching = true;
        sync();
      },
      { passive: true },
    );
    const releaseTouch = (event: TouchEvent) => {
      if (!touching) return;
      touching = event.touches.length > 0;
      sync();
    };
    window.addEventListener('touchend', releaseTouch, { passive: true });
    window.addEventListener('touchcancel', releaseTouch, { passive: true });
    window.addEventListener('blur', () => {
      pressed = false;
      touching = false;
      hovered = false;
      sync();
    });

    strip.addEventListener('focusin', sync);
    strip.addEventListener('focusout', (event) => {
      if (!strip.contains(event.relatedTarget as Node | null)) {
        // focusout fires before document.activeElement reflects its new target.
        queueMicrotask(sync);
      }
    });

    document.addEventListener('visibilitychange', sync);

    still.addEventListener('change', () => {
      if (still.matches) teardown();
      else build();
      sync();
    });

    if (!still.matches) build();
  });
