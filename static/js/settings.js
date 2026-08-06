document.querySelectorAll('[data-toggle]').forEach(sw => {
    sw.addEventListener('click', () => {
        sw.classList.toggle('off');
    });
});

// const editModal = document.getElementById("editProfileModal");

// document.getElementById("editProfileBtn").addEventListener("click", () => {
//     editModal.classList.remove("hidden");
// });

// document.getElementById("closeEditModal").addEventListener("click", () => {
//     editModal.classList.add("hidden");
// });



(function () {
  "use strict";

  var URLS = window.SETTINGS_URLS;

  function toast(message, isError) {
    var stack = document.getElementById('toastStack');
    var el = document.createElement('div');
    el.className = 'toast' + (isError ? ' error' : '');
    el.textContent = message;
    stack.appendChild(el);
    setTimeout(function () {
      el.classList.add('fade-out');
      setTimeout(function () { el.remove(); }, 200);
    }, 3200);
  }

  function postJSON(url, body) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(body || {})
    }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok) throw new Error(data.message || 'Something went wrong.');
        return data;
      });
    });
  }

  document.querySelectorAll('#settingsNav button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('#settingsNav button').forEach(function (b) { b.classList.remove('active'); });
      document.querySelectorAll('.settings-panel').forEach(function (p) { p.classList.remove('active'); });
      btn.classList.add('active');
      document.querySelector('.settings-panel[data-panel="' + btn.dataset.tab + '"]').classList.add('active');
    });
  });

  var avatarInput = document.getElementById('avatarInput');
  var dropzone = document.getElementById('avatarDropzone');

  function previewFile(file) {
    if (!file) return;
    document.getElementById('avatarPreview').src = URL.createObjectURL(file);
  }

  if (avatarInput) {
    avatarInput.addEventListener('change', function (e) { previewFile(e.target.files[0]); });
  }

  if (dropzone) {
    ['dragenter', 'dragover'].forEach(function (evt) {
      dropzone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropzone.classList.add('drag-over');
      });
    });
    ['dragleave', 'drop'].forEach(function (evt) {
      dropzone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
      });
    });
    dropzone.addEventListener('drop', function (e) {
      var file = e.dataTransfer.files[0];
      if (file) {
        avatarInput.files = e.dataTransfer.files;
        previewFile(file);
      }
    });
  }

  var profileForm = document.getElementById('profileForm');
  if (profileForm) {
    profileForm.addEventListener('submit', function () {
      var btn = profileForm.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Saving...';
    });
  }

  var passwordForm = document.getElementById('passwordForm');
  if (passwordForm) {
    passwordForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var newPass = passwordForm.new_password.value;
      var confirmPass = passwordForm.confirm_password.value;

      if (newPass !== confirmPass) {
        toast('New revelation and confirmation do not match.', true);
        return;
      }

      var btn = passwordForm.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Updating...';

      postJSON(URLS.password, {
        current_password: passwordForm.current_password.value,
        new_password: newPass,
        confirm_password: confirmPass
      }).then(function (data) {
        toast(data.message, !data.success);
        if (data.success) passwordForm.reset();
      }).catch(function (err) {
        toast(err.message, true);
      }).finally(function () {
        btn.disabled = false;
        btn.textContent = 'Update Revelation';
      });
    });
  }

  document.querySelectorAll('[data-toggle-url], [data-notify-field]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (el.classList.contains('is-busy')) return;

      var wasOn = el.classList.contains('is-on');
      el.classList.add('is-busy');
      el.classList.toggle('is-on');

      var request;
      if (el.dataset.toggleUrl) {
        request = postJSON(el.dataset.toggleUrl, {});
      } else {
        request = postJSON(URLS.notifications, {
          field: el.dataset.notifyField,
          value: !wasOn
        });
      }

      request.then(function (data) {
        toast(data.message, !data.success);
        if (!data.success) el.classList.toggle('is-on', wasOn);
      }).catch(function (err) {
        el.classList.toggle('is-on', wasOn);
        toast(err.message, true);
      }).finally(function () {
        el.classList.remove('is-busy');
      });
    });
  });

  document.querySelectorAll('.theme-swatch').forEach(function (el) {
    el.addEventListener('click', function () {
      document.querySelectorAll('.theme-swatch').forEach(function (s) { s.classList.remove('selected'); });
      el.classList.add('selected');
      postJSON(URLS.appearance, { theme: el.dataset.theme })
        .then(function (data) { toast(data.message, !data.success); })
        .catch(function (err) { toast(err.message, true); });
    });
  });

  document.querySelectorAll('.accent-dot').forEach(function (el) {
    el.addEventListener('click', function () {
      document.querySelectorAll('.accent-dot').forEach(function (d) { d.classList.remove('selected'); });
      el.classList.add('selected');
      postJSON(URLS.appearance, { accent: el.dataset.accent })
        .then(function (data) { toast(data.message, !data.success); })
        .catch(function (err) { toast(err.message, true); });
    });
  });

  function bindLinkButton(btn) {
    btn.addEventListener('click', function () {
      var provider = btn.dataset.link || btn.dataset.unlink;
      var isLink = !!btn.dataset.link;
      var url = (isLink ? URLS.link : URLS.unlink) + provider;

      btn.disabled = true;
      postJSON(url, {}).then(function (data) {
        toast(data.message, !data.success);
        if (data.success) {
          var row = document.querySelector('.connect-row[data-provider-row="' + provider + '"] .provider-actions');
          if (isLink) {
            row.innerHTML = '<span class="link-badge">LINKED</span>' +
              '<button type="button" class="btn-link" data-unlink="' + provider + '">Unlink</button>';
          } else {
            row.innerHTML = '<button type="button" class="btn-link" data-link="' + provider + '">Link</button>';
          }
          bindLinkButton(row.querySelector('button'));
        } else {
          btn.disabled = false;
        }
      }).catch(function (err) {
        toast(err.message, true);
        btn.disabled = false;
      });
    });
  }

  document.querySelectorAll('[data-link], [data-unlink]').forEach(bindLinkButton);
})();