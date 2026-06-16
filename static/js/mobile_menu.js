(() => {
  const menu = document.querySelector('.mobile-menu');
  const openBtn = document.querySelector('[data-menu-open]');
  const closeBtns = document.querySelectorAll('[data-menu-close]');

  if (!menu) return;

  const open = () => {
    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    document.body.classList.add('menu-open');
    openBtn?.setAttribute('aria-expanded', 'true');
  };

  const close = () => {
    menu.classList.remove('is-open');
    menu.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('menu-open');
    openBtn?.setAttribute('aria-expanded', 'false');
  };

  openBtn?.addEventListener('click', open);
  closeBtns.forEach((btn) => btn.addEventListener('click', close));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) close();
  });
})();
