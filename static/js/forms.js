(() => {
  function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input?.value) {
      return input.value;
    }
    const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  document.body.addEventListener('htmx:configRequest', (event) => {
    const token = getCsrfToken();
    if (token) {
      event.detail.headers['X-CSRFToken'] = token;
    }
  });

  document.body.addEventListener('htmx:afterSwap', (e) => {
    const target = e.detail.target;
    if (!target) return;
    target.querySelectorAll('.reveal').forEach((el) => {
      el.classList.add('is-visible');
    });
  });
})();
