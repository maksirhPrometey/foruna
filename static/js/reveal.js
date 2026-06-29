(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const coarsePointer = window.matchMedia('(hover: none) and (pointer: coarse)');

  const revealElements = document.querySelectorAll('.reveal');

  revealElements.forEach((el) => {
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

  const showElement = (el) => {
    el.classList.add('is-visible');
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          showElement(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: coarsePointer.matches ? 0.01 : 0.08,
      rootMargin: coarsePointer.matches ? '0px 0px 0px 0px' : '0px 0px -32px 0px',
    },
  );

  revealElements.forEach((el) => {
    if (el.classList.contains('is-visible')) {
      return;
    }
    observer.observe(el);
  });

  if (coarsePointer.matches) {
    window.setTimeout(() => {
      revealElements.forEach((el) => {
        if (!el.classList.contains('is-visible')) {
          showElement(el);
        }
      });
    }, 1200);
  }
})();
