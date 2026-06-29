(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const revealElements = document.querySelectorAll('.reveal');

  if (!revealElements.length) {
    return;
  }

  const showElement = (el) => {
    el.classList.add('is-visible');
  };

  const isInViewport = (el) => {
    const rect = el.getBoundingClientRect();
    const viewHeight = window.innerHeight || document.documentElement.clientHeight;
    return rect.top < viewHeight && rect.bottom > 0;
  };

  revealElements.forEach((el) => {
    const delay = el.dataset.revealDelay;
    if (delay) {
      el.style.setProperty('--delay', delay);
    }

    if (reduceMotion.matches || isInViewport(el)) {
      showElement(el);
    }
  });

  if (reduceMotion.matches) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          showElement(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0, rootMargin: '0px 0px 40px 0px' },
  );

  revealElements.forEach((el) => {
    if (!el.classList.contains('is-visible')) {
      observer.observe(el);
    }
  });

  window.setTimeout(() => {
    revealElements.forEach((el) => {
      if (!el.classList.contains('is-visible')) {
        showElement(el);
      }
    });
  }, 800);
})();
