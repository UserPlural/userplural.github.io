// The navigation remains visible when JavaScript is unavailable.
(() => {
  const button = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#primary-nav');
  if (!button || !navigation) return;
  document.documentElement.classList.add('js');
  button.hidden = false;
  const close = () => {
    button.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  };
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      close();
      button.focus();
    }
  });
  window.matchMedia('(min-width: 1081px)').addEventListener('change', close);
})();

// Organizer bios open in a dialog; without JavaScript they stay inline.
(() => {
  const dialog = document.querySelector('.bio-dialog');
  if (!dialog || !dialog.showModal) return;
  const cards = [...document.querySelectorAll('.organizer')];
  const name = card => card.querySelector('h3').textContent;
  let current = 0;
  const label = (button, text, card) => {
    const caption = document.createElement('span');
    caption.textContent = text;
    button.replaceChildren(caption, name(card));
  };
  const show = index => {
    current = (index + cards.length) % cards.length;
    const card = cards[current];
    const photo = card.querySelector('.portrait');
    const image = dialog.querySelector('.portrait');
    image.src = photo.src;
    image.className = photo.className;
    dialog.querySelector('#bio-name').textContent = name(card);
    dialog.querySelector('.bio-affiliation').textContent = card.querySelector('.affiliation').textContent;
    dialog.querySelector('.bio-text').innerHTML = card.querySelector('.bio').innerHTML;
    const website = card.querySelector('h3 a').cloneNode();
    website.textContent = 'Visit website';
    dialog.querySelector('.bio-website').replaceChildren(website);
    label(dialog.querySelector('.bio-prev'), 'Previous', cards[(current - 1 + cards.length) % cards.length]);
    label(dialog.querySelector('.bio-next'), 'Next', cards[(current + 1) % cards.length]);
  };
  cards.forEach((card, index) => {
    const open = event => {
      event.preventDefault();
      show(index);
      dialog.showModal();
    };
    card.querySelector('.bio-button').addEventListener('click', open);
    card.querySelector('.portrait-link').addEventListener('click', open);
  });
  dialog.querySelector('.bio-prev').addEventListener('click', () => show(current - 1));
  dialog.querySelector('.bio-next').addEventListener('click', () => show(current + 1));
  dialog.querySelector('.bio-close').addEventListener('click', () => dialog.close());
  // A click on the dialog element itself lands on the backdrop.
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  document.addEventListener('keydown', event => {
    if (!dialog.open) return;
    if (event.key === 'ArrowLeft') show(current - 1);
    if (event.key === 'ArrowRight') show(current + 1);
  });
})();
