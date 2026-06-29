(() => {
  const menu = document.querySelector('.mobile-menu');
  const openBtn = document.querySelector('[data-menu-open]');
  const closeBtns = document.querySelectorAll('[data-menu-close]');
  const panel = menu?.querySelector('.mobile-menu__panel');

  if (!menu || !panel) return;

  const FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  let scrollY = 0;

  const getFocusables = () => (
    [...panel.querySelectorAll(FOCUSABLE)].filter(
      (el) => el.getAttribute('tabindex') !== '-1' && !el.closest('[hidden]'),
    )
  );

  const lockScroll = () => {
    scrollY = window.scrollY;
    document.body.style.top = `-${scrollY}px`;
    document.body.classList.add('menu-open');
  };

  const unlockScroll = () => {
    document.body.classList.remove('menu-open');
    document.body.style.top = '';
    window.scrollTo(0, scrollY);
  };

  const open = () => {
    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    lockScroll();
    openBtn?.setAttribute('aria-expanded', 'true');

    const focusables = getFocusables();
    requestAnimationFrame(() => {
      (focusables[0] || panel.querySelector('.mobile-menu__close'))?.focus();
    });
  };

  const close = () => {
    menu.classList.remove('is-open');
    menu.setAttribute('aria-hidden', 'true');
    unlockScroll();
    openBtn?.setAttribute('aria-expanded', 'false');
    openBtn?.focus();
  };

  const onKeydown = (e) => {
    if (!menu.classList.contains('is-open')) return;

    if (e.key === 'Escape') {
      close();
      return;
    }

    if (e.key !== 'Tab') return;

    const focusables = getFocusables();
    if (focusables.length === 0) return;

    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    const active = document.activeElement;

    if (e.shiftKey && active === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && active === last) {
      e.preventDefault();
      first.focus();
    }
  };

  openBtn?.addEventListener('click', open);
  closeBtns.forEach((btn) => btn.addEventListener('click', close));

  panel.querySelectorAll('a[href]').forEach((link) => {
    link.addEventListener('click', close);
  });

  document.addEventListener('keydown', onKeydown);
})();
