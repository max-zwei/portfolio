/** Handoff §16: the focused reading band is the centre third of the viewport. */
export const FOCUS_BAND = 1 / 3;

export const observeFocusBand = <T extends Element>(
  elements: Iterable<T>,
  update: (element: T, active: boolean) => void,
) => {
  const targets = Array.from(elements);
  if (targets.length === 0 || !('IntersectionObserver' in window)) {
    return () => {};
  }

  const onIntersect = (records: IntersectionObserverEntry[]) => {
    for (const record of records) {
      update(record.target as T, record.isIntersecting);
    }
  };

  let observer: IntersectionObserver | undefined;
  const observe = () => {
    observer?.disconnect();
    const inset =
      (document.documentElement.clientHeight * (1 - FOCUS_BAND)) / 2;
    observer = new IntersectionObserver(onIntersect, {
      rootMargin: `-${inset}px 0px -${inset}px 0px`,
    });
    for (const target of targets) observer.observe(target);
  };

  observe();
  window.addEventListener('resize', observe);

  return () => {
    observer?.disconnect();
    window.removeEventListener('resize', observe);
  };
};
