(function () {
  // Close the Work dropdown when clicking elsewhere
  document.addEventListener('click', function (e) {
    document.querySelectorAll('details.work[open]').forEach(function (d) {
      if (!d.contains(e.target)) d.removeAttribute('open');
    });
  });

  // Lightbox for gallery images
  var links = [].slice.call(document.querySelectorAll('a.zoom'));
  if (links.length && window.HTMLDialogElement) {
    var dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.innerHTML = '<button class="lb-close" aria-label="Close">\u00d7</button>' +
      '<button class="lb-prev" aria-label="Previous image">\u2039</button>' +
      '<button class="lb-next" aria-label="Next image">\u203a</button>' +
      '<figure><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector('img'), cap = dlg.querySelector('figcaption'), i = 0;
    function show(n) {
      i = (n + links.length) % links.length;
      var a = links[i], t = a.querySelector('img');
      img.src = a.href; img.alt = t ? t.alt : ''; cap.textContent = a.dataset.caption || '';
    }
    links.forEach(function (a, n) {
      a.addEventListener('click', function (e) { e.preventDefault(); show(n); dlg.showModal(); });
    });
    dlg.querySelector('.lb-close').onclick = function () { dlg.close(); };
    dlg.querySelector('.lb-prev').onclick = function () { show(i - 1); };
    dlg.querySelector('.lb-next').onclick = function () { show(i + 1); };
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.tagName === 'FIGURE') dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(i - 1);
      if (e.key === 'ArrowRight') show(i + 1);
    });
  }

  // Contact form: opens the visitor's email app (static sites cannot send mail themselves)
  var f = document.getElementById('contact-form');
  if (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(f);
      var body = (d.get('message') || '') + '\n\n' + (d.get('name') || '') + '\n' + (d.get('email') || '');
      window.location.href = 'mailto:billfinksos@yahoo.com?subject=' +
        encodeURIComponent('FinkArt website message from ' + (d.get('name') || '')) +
        '&body=' + encodeURIComponent(body);
    });
  }
})();
