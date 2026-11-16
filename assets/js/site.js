// Header state, mobile menu, and a one-time reveal for content below the fold.
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var btn = document.querySelector('.menu-btn');
  var panel = document.getElementById('menu-panel');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    if (btn) btn.setAttribute('aria-expanded', String(open));
    if (panel) panel.hidden = !open;
  }
  if (btn && panel) {
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1080) setMenu(false); });
  }

})();
