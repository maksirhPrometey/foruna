(() => {
  const SWIPE_THRESHOLD = 48;

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
      index = (nextIndex + total) % total;
      track.style.transform = `translate3d(-${index * 100}%, 0, 0)`;

      dots.forEach((dot, dotIndex) => {
        const active = dotIndex === index;
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-selected', active ? 'true' : 'false');
      });

      slides.forEach((slide, slideIndex) => {
        slide.setAttribute('aria-hidden', slideIndex === index ? 'false' : 'true');
      });
    };

    prevBtn?.addEventListener('click', () => goTo(index - 1));
    nextBtn?.addEventListener('click', () => goTo(index + 1));

    dots.forEach((dot) => {
      dot.addEventListener('click', () => {
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
