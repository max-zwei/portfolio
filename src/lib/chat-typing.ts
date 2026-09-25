/** Typing pace, in ms. 1.5× the original 18/240 pace Max signed off on. */
export const PER_CHAR = 12;
export const BETWEEN = 160;

/** Rebuild a paragraph as per-character spans, then reveal them in turn. */
export const type = (el: HTMLElement, startDelay: number) => {
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const texts: Text[] = [];
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    texts.push(node as Text);
  }

  let index = 0;
  for (const node of texts) {
    const fragment = document.createDocumentFragment();
    // Array.from, not split(''), so an emoji or accent stays one unit.
    for (const character of Array.from(node.data)) {
      const span = document.createElement('span');
      span.textContent = character;
      span.className = 'chat__char';
      span.style.setProperty('--c', String(index++));
      fragment.append(span);
    }
    node.replaceWith(fragment);
  }

  el.style.setProperty('--start', `${startDelay}ms`);
  el.style.setProperty('--per-char', `${PER_CHAR}ms`);
  el.dataset.typed = 'true';
};
