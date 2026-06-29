(() => {
  const SWIPE_THRESHOLD = 48;

  const goToSlide = (track, slides, dots, index, total) => {
    const next = (index + total) % total;
    const offset = next * 100;
    track.style.transform = `translate3d(-${offset}%, 0, 0)`;
    track.style.webkitTransform = `translate3d(-${offset}%, 0, 0)`;

    dots.forEach((dot, dotIndex) => {
      const active = dotIndex === next;
      dot.classList.toggle('is-active', active);
      dot.setAttribute('aria-selected', active ? 'true' : 'false');
    });

    slides.forEach((slide, slideIndex) => {
      slide.setAttribute('aria-hidden', slideIndex === next ? 'false' : 'true');
    });

    return next;
  };

  document.querySelectorAll('[data-card-carousel]').forEach((root) => {
    const track = root.querySelector('[data-carousel-track]');
    const slides = root.querySelectorAll('[data-carousel-slide]');
    const prevBtn = root.querySelector('[data-carousel-prev]');
    const nextBtn = root.querySelector('[data-carousel-next]');
    const dots = root.querySelectorAll('[data-carousel-dot]');
    const viewport = root.querySelector('[data-carousel-viewport]');

    if (!track || slides.length < 2) {
      return;
    }

    let index = 0;
    const total = slides.length;
    let startX = 0;
    let startY = 0;
    let deltaX = 0;
    let isDragging = false;

    const goTo = (nextIndex) => {
      index = goToSlide(track, slides, dots, nextIndex, total);
    };

    const onPrev = (event) => {
      event.preventDefault();
      goTo(index - 1);
    };

    const onNext = (event) => {
      event.preventDefault();
      goTo(index + 1);
    };

    prevBtn?.addEventListener('click', onPrev);
    nextBtn?.addEventListener('click', onNext);

    dots.forEach((dot) => {
      dot.addEventListener('click', (event) => {
        event.preventDefault();
        const target = Number.parseInt(dot.dataset.carouselDot, 10);
        if (!Number.isNaN(target)) {
          goTo(target);
        }
      });
    });

    viewport?.addEventListener('touchstart', (event) => {
      if (event.touches.length !== 1) {
        return;
      }
      isDragging = true;
      startX = event.touches[0].clientX;
      startY = event.touches[0].clientY;
      deltaX = 0;
    }, { passive: true });

    viewport?.addEventListener('touchmove', (event) => {
      if (!isDragging || event.touches.length !== 1) {
        return;
      }
      const touch = event.touches[0];
      const moveX = touch.clientX - startX;
      const moveY = touch.clientY - startY;

      if (Math.abs(moveX) > Math.abs(moveY) && Math.abs(moveX) > 8) {
        deltaX = moveX;
      }
    }, { passive: true });

    viewport?.addEventListener('touchend', () => {
      if (!isDragging) {
        return;
      }
      isDragging = false;

      if (deltaX > SWIPE_THRESHOLD) {
        goTo(index - 1);
      } else if (deltaX < -SWIPE_THRESHOLD) {
        goTo(index + 1);
      }

      deltaX = 0;
    }, { passive: true });

    viewport?.addEventListener('touchcancel', () => {
      isDragging = false;
      deltaX = 0;
    }, { passive: true });
  });
})();
