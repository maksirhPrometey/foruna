(() => {
  const menu = document.querySelector('.mobile-menu');
  const openBtn = document.querySelector('[data-menu-open]');
  const closeBtns = document.querySelectorAll('[data-menu-close]');
  const panel = menu?.querySelector('.mobile-menu__panel');
  const root = document.documentElement;

  if (!menu || !panel) return;

  const FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';
  const coarsePointer = window.matchMedia('(hover: none) and (pointer: coarse)');

  let scrollY = 0;

  const getFocusables = () => (
    [...panel.querySelectorAll(FOCUSABLE)].filter(
      (el) => el.getAttribute('tabindex') !== '-1' && !el.closest('[hidden]'),
    )
  );

  const forceClose = ({ restoreFocus = false } = {}) => {
    menu.classList.remove('is-open');
    menu.setAttribute('aria-hidden', 'true');
    root.classList.remove('menu-open');
    document.body.classList.remove('menu-open');
    document.body.style.top = '';
    document.body.style.position = '';
    document.body.style.width = '';
    openBtn?.setAttribute('aria-expanded', 'false');

    if (restoreFocus && !coarsePointer.matches) {
      openBtn?.focus();
    }
  };

  const lockScroll = () => {
    scrollY = window.scrollY || root.scrollTop || 0;
    root.classList.add('menu-open');
  };

  const unlockScroll = () => {
    root.classList.remove('menu-open');
    document.body.classList.remove('menu-open');
    window.scrollTo(0, scrollY);
  };

  const open = () => {
    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    lockScroll();
    openBtn?.setAttribute('aria-expanded', 'true');

    if (!coarsePointer.matches) {
      const focusables = getFocusables();
      requestAnimationFrame(() => {
        (focusables[0] || panel.querySelector('.mobile-menu__close'))?.focus();
      });
    }
  };

  const close = ({ restoreFocus = true } = {}) => {
    forceClose({ restoreFocus: false });
    unlockScroll();

    if (restoreFocus && !coarsePointer.matches) {
      openBtn?.focus();
    }
  };

  const onKeydown = (e) => {
    if (!menu.classList.contains('is-open')) return;

    if (e.key === 'Escape') {
      close();
      return;
    }

    if (e.key !== 'Tab' || coarsePointer.matches) return;

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

  forceClose();

  window.addEventListener('pageshow', () => {
    forceClose();
  });

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      forceClose();
    }
  });

  openBtn?.addEventListener('click', open);
  closeBtns.forEach((btn) => btn.addEventListener('click', () => close()));

  panel.querySelectorAll('a[href]').forEach((link) => {
    link.addEventListener('click', () => {
      close({ restoreFocus: false });
    });
  });

  document.addEventListener('keydown', onKeydown);
})();
