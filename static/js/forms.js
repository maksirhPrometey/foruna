(() => {
  // HTMX lead form — after swap, re-run reveal observer on new elements
  document.body.addEventListener('htmx:afterSwap', (e) => {
    const target = e.detail.target;
    if (!target) return;
    target.querySelectorAll('.reveal').forEach((el) => {
      el.classList.add('is-visible');
    });
  });
})();
