(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;

  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);
    header.classList.toggle('is-hidden', y > lastY && y > 200);
    lastY = y;
  };

  window.addEventListener('scroll', onScroll, { passive: true });
})();
