const content = document.querySelector('#content');
const status = document.querySelector('#status');
const designWidth = 375;
const cycleHeight = 18686; // Figma Mobile bottom (19,811px) minus Content start (1,125px).

async function startStory() {
  const response = await fetch('./cards.json');
  if (!response.ok) throw new Error(`Could not load the story (${response.status}).`);
  const cards = await response.json();
  cards.sort((a, b) => a.y - b.y);
  content.style.setProperty('--cycle-height', cycleHeight);
  const copies = new Map();
  const fragment = document.createDocumentFragment();

  for (let cycle = 0; cycle < 2; cycle += 1) {
    const section = document.createElement('section');
    section.className = 'sequence';
    section.setAttribute('aria-label', 'Social lives and media habits, 1990s–2020s');
    // The second copy is a visual buffer, not a second reading order.
    if (cycle === 1) section.setAttribute('aria-hidden', 'true');
    for (const card of cards) {
      const element = document.createElement(card.text ? 'h2' : 'figure');
      element.className = 'card';
      if (card.trimmed) element.classList.add('card--trimmed');
      element.dataset.card = card.id;
      element.style.left = `${(40 + card.x) / designWidth * 100}%`;
      element.style.top = `${card.y / cycleHeight * 100}%`;
      element.style.width = `${card.width / designWidth * 100}%`;
      element.style.height = `${card.height / cycleHeight * 100}%`;
      if (card.text) {
        element.textContent = card.text;
      } else {
        const image = document.createElement('img');
        image.alt = card.alt;
        image.width = Math.ceil(card.width);
        image.height = Math.ceil(card.height);
        image.decoding = 'async';
        image.dataset.src = card.src;
        element.append(image);
        const pair = copies.get(card.id) || [];
        pair.push(image);
        copies.set(card.id, pair);
      }
      section.append(element);
    }
    fragment.append(section);
  }
  content.append(fragment);
  status.hidden = true;

  // Load paired artwork together: crossing the seam never exposes an unloaded copy.
  const load = (image) => {
    const pair = copies.get(image.parentElement.dataset.card);
    for (const sibling of pair) {
      if (!sibling.hasAttribute('src')) sibling.src = sibling.dataset.src;
      observer?.unobserve(sibling);
    }
  };
  const observer = 'IntersectionObserver' in window
    ? new IntersectionObserver((entries) => {
      for (const entry of entries) if (entry.isIntersecting) load(entry.target);
    }, { rootMargin: '1200px 0px' })
    : null;
  for (const pair of copies.values()) {
    for (const image of pair) {
      if (observer) observer.observe(image);
      else load(image);
    }
  }

  let start = 0;
  let height = 0;
  let looped = false;
  const measure = () => {
    start = content.getBoundingClientRect().top + window.scrollY;
    height = content.firstElementChild.getBoundingClientRect().height;
  };
  measure();
  new ResizeObserver(measure).observe(document.querySelector('.canvas'));
  await document.fonts.ready;
  measure();

  // Two fixed-size copies keep the DOM bounded. Rebase by an exact cycle,
  // preserving the visible card and its pixel offset, rather than jumping to top.
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (height && y >= start + height) {
      looped = true;
      window.scrollTo({ top: y - height, behavior: 'instant' });
    } else if (looped && y < start) {
      window.scrollTo({ top: y + height, behavior: 'instant' });
    }
  }, { passive: true });
}

startStory().catch((error) => {
  status.hidden = false;
  status.textContent = 'The story could not load. Please refresh to try again.';
  console.error(error);
});
