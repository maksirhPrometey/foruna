(() => {
  const list = document.getElementById('ui-probe-client');
  if (!list) return;

  const rows = [];

  const add = (status, label, value) => {
    rows.push({ status, label, value });
  };

  const badgeClass = (status) => {
    if (status === 'ok') return 'ui-probe__badge--ok';
    if (status === 'fail') return 'ui-probe__badge--fail';
    if (status === 'warn') return 'ui-probe__badge--warn';
    return 'ui-probe__badge--wait';
  };

  const badgeText = (status) => {
    if (status === 'ok') return 'OK';
    if (status === 'fail') return 'FAIL';
    if (status === 'warn') return 'WARN';
    return '…';
  };

  const render = () => {
    list.innerHTML = rows.map((row) => (
      `<div class="ui-probe__row">`
      + `<span class="ui-probe__badge ${badgeClass(row.status)}">${badgeText(row.status)}</span>`
      + `<div><div class="ui-probe__label">${row.label}</div>`
      + `<div class="ui-probe__value">${row.value}</div></div>`
      + `</div>`
    )).join('');
  };

  add('ok', 'User-Agent', navigator.userAgent);
  add(
    window.visualViewport ? 'ok' : 'warn',
    'Viewport',
    `${window.innerWidth}×${window.innerHeight}px`
      + (window.visualViewport
        ? ` (visual ${Math.round(window.visualViewport.width)}×${Math.round(window.visualViewport.height)})`
        : ''),
  );

  const coarse = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  add('ok', 'Touch-пристрій', coarse ? 'так (iPhone/iPad)' : 'ні (desktop)');

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  add(reduced ? 'warn' : 'ok', 'prefers-reduced-motion', reduced ? 'увімкнено' : 'вимкнено');

  const stylesheets = [...document.styleSheets].map((sheet) => {
    try {
      return sheet.href || '[inline]';
    } catch {
      return '[blocked]';
    }
  });
  const hasComponents = stylesheets.some((href) => href.includes('components.css'));
  add(hasComponents ? 'ok' : 'fail', 'components.css у document.styleSheets', hasComponents ? 'завантажено' : 'не знайдено');

  const revealEl = document.querySelector('.probe-reveal.reveal');
  if (revealEl) {
    const opacity = getComputedStyle(revealEl).opacity;
    add(Number(opacity) >= 0.99 ? 'ok' : 'fail', 'Computed opacity .reveal', opacity);
  }

  const carouselEl = document.querySelector('.probe-carousel');
  if (carouselEl) {
    const rect = carouselEl.getBoundingClientRect();
    const height = Math.round(rect.height);
    add(height >= 120 ? 'ok' : 'fail', 'Висота тест-каруселі', `${height}px (очікується ≥120px)`);
  }

  const menuOpen = document.documentElement.classList.contains('menu-open')
    || document.body.classList.contains('menu-open');
  const menuVisible = document.querySelector('.mobile-menu.is-open');
  add(
    menuOpen || menuVisible ? 'fail' : 'ok',
    'Меню / scroll lock',
    menuOpen || menuVisible
      ? 'застрягло — темний фон перекриває сторінку'
      : 'закрито',
  );

  let cspBlocksInline = false;
  try {
    const probe = document.createElement('span');
    probe.style.setProperty('color', 'red');
    cspBlocksInline = probe.style.color !== 'red' && probe.style.color !== 'rgb(255, 0, 0)';
  } catch {
    cspBlocksInline = true;
  }
  add(
    cspBlocksInline ? 'warn' : 'ok',
    'CSP + inline style (JS)',
    cspBlocksInline ? 'блокує setProperty — OK для безпеки' : 'дозволяє inline',
  );

  render();

  fetch('/static/css/components.css', { cache: 'no-store' })
    .then((response) => {
      add(response.ok ? 'ok' : 'fail', 'GET /static/css/components.css', `HTTP ${response.status}`);
      return response.text();
    })
    .then((css) => {
      const revealFixed = /\.reveal\s*\{[^}]*opacity:\s*1/.test(css.replace(/\s+/g, ' '));
      add(
        revealFixed ? 'ok' : 'fail',
        'CSS на сервері: .reveal opacity:1',
        revealFixed ? 'так (новий фікс)' : 'ні (старий CSS — кеш або не задеплоєно)',
      );

      const carouselFixed = /\.card-carousel\s*\{[^}]*height:\s*auto/.test(css.replace(/\s+/g, ' '));
      add(
        carouselFixed ? 'ok' : 'fail',
        'CSS на сервері: carousel height:auto',
        carouselFixed ? 'так' : 'ні',
      );
    })
    .catch((error) => {
      add('fail', 'GET components.css', String(error));
    })
    .finally(() => {
      render();
    });

  fetch('/marking/', { cache: 'no-store' })
    .then((response) => response.text())
    .then((html) => {
      const sections = (html.match(/class="laser-section/g) || []).length;
      const carousels = (html.match(/data-card-carousel/g) || []).length;
      add(
        sections > 0 ? 'ok' : 'fail',
        'HTML /marking/ — laser-section',
        `${sections} секцій`,
      );
      add(
        carousels > 0 ? 'ok' : 'warn',
        'HTML /marking/ — каруселі',
        `${carousels} шт.`,
      );
    })
    .catch((error) => {
      add('fail', 'GET /marking/', String(error));
    })
    .finally(() => {
      render();
    });
})();
