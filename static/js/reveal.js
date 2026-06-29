(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const revealElements = document.querySelectorAll('.reveal');

  if (!revealElements.length) {
    return;
  }

  revealElements.forEach((el) => {
    el.classList.add('is-visible');
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
    { threshold: 0, rootMargin: '0px 0px 40px 0px' },
  );

  revealElements.forEach((el) => {
    observer.observe(el);
  });
})();
