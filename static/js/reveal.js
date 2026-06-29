(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('.reveal').forEach((el) => {
    const delay = el.dataset.revealDelay;
    if (delay) {
      el.style.setProperty('--delay', delay);
    }

    if (reduceMotion.matches) {
      el.classList.add('is-visible');
    }
  });

  if (reduceMotion.matches) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -32px 0px' },
  );

  document.querySelectorAll('.reveal:not(.is-visible)').forEach((el) => {
    observer.observe(el);
  });
})();
