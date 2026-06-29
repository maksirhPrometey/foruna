(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const DESKTOP_MIN = 1024;
  let lastY = 0;

  const isDesktop = () => window.matchMedia(`(min-width: ${DESKTOP_MIN}px)`).matches;

  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);

    if (isDesktop()) {
      header.classList.toggle('is-hidden', y > lastY && y > 200);
    } else {
      header.classList.remove('is-hidden');
    }

    lastY = y;
  };

  const onResize = () => {
    if (!isDesktop()) {
      header.classList.remove('is-hidden');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });
})();
