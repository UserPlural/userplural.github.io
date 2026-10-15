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
  window.matchMedia('(min-width: 801px)').addEventListener('change', close);
})();
