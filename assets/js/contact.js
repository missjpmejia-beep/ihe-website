// Enquiry form: validates, then sends to Web3Forms without leaving the page.
(function () {
  var form = document.getElementById('enquiry-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var button = form.querySelector('button[type="submit"]');

  function show(kind, html) {
    status.className = 'form-status ' + (kind === 'ok' ? 'is-ok' : 'is-error');
    status.innerHTML = html;
  }

  var fallback = 'Please call us on <a href="tel:+441977644489">01977 644489</a> or email ' +
    '<a href="mailto:info@ih-equipment.co.uk">info@ih-equipment.co.uk</a>.';

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      var first = form.querySelector(':invalid');
      show('error', 'Please fill in the highlighted fields.');
      if (first) first.focus();
      form.reportValidity && form.reportValidity();
      return;
    }

    var key = form.querySelector('[name="access_key"]').value;
    if (!key || key.indexOf('WEB3FORMS') === 0) {
      show('error', 'Sorry, the form isn’t switched on yet. ' + fallback);
      return;
    }

    button.disabled = true;
    button.textContent = 'Sending…';

    fetch(form.action, {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        if (res.ok && res.d && res.d.success) {
          form.reset();
          show('ok', '<strong>Thanks, your enquiry has been sent.</strong> We’ll get back to you within 48 hours.');
        } else {
          show('error', 'Sorry, something went wrong sending the form. ' + fallback);
        }
      })
      .catch(function () {
        show('error', 'Sorry, something went wrong sending the form. ' + fallback);
      })
      .then(function () {
        button.disabled = false;
        button.textContent = 'Send enquiry';
      });
  });
})();
