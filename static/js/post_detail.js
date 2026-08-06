(function () {
    // ---- Scroll unfurl ----
    const scrollWrap = document.getElementById('scroll-wrap');
    const scrollClose = document.getElementById('scroll-close');
    scrollWrap.addEventListener('click', (e) => {
        if (!scrollWrap.classList.contains('open')) {
            scrollWrap.classList.add('open');
        }
    });
    scrollClose.addEventListener('click', (e) => {
        e.stopPropagation();
        scrollWrap.classList.remove('open');
        scrollWrap.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    // ---- Resonate (like) button ----
    const resonateBtn = document.getElementById('resonate-btn');
    const revelationsCount = document.getElementById('revelations-count');
    let resonated = false;
    resonateBtn.addEventListener('click', () => {
        resonated = !resonated;
        let n = parseInt(revelationsCount.textContent.replace(/,/g, ''), 10);
        resonateBtn.classList.toggle('active', resonated);
        resonateBtn.classList.remove('pulse');
        void resonateBtn.offsetWidth; // restart animation
        resonateBtn.classList.add('pulse');
        n = resonated ? n + 1 : n - 1;
        revelationsCount.textContent = n.toLocaleString();
    });

    // ---- Save / bookmark ----
    const saveBtn = document.getElementById('save-btn');
    saveBtn.addEventListener('click', () => {
        saveBtn.classList.toggle('saved');
    });

    // ---- Share ----
    const shareBtn = document.getElementById('share-btn');
    const shareToast = document.getElementById('share-toast');
    shareBtn.addEventListener('click', () => {
        shareToast.classList.remove('hidden');
        navigator.clipboard?.writeText(window.location.href).catch(() => { });
        setTimeout(() => shareToast.classList.add('hidden'), 1600);
    });

    // ---- Like buttons on echoes ----
    document.querySelectorAll('.like-btn').forEach(btn => {
        let liked = false;
        btn.addEventListener('click', () => {
            liked = !liked;
            const countEl = btn.querySelector('.like-count');
            let n = parseInt(countEl.textContent, 10);
            countEl.textContent = liked ? n + 1 : n - 1;
            btn.classList.toggle('text-[var(--jade)]', liked);
        });
    });

    // ---- Reply toggles ----
    document.querySelectorAll('.reply-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const box = btn.closest('.flex-1').querySelector('.reply-box');
            box.classList.toggle('open');
            if (box.classList.contains('open')) {
                setTimeout(() => box.querySelector('textarea').focus(), 200);
            }
        });
    });

    document.querySelectorAll('.reply-submit').forEach(btn => {
        btn.addEventListener('click', () => {
            const box = btn.closest('.reply-box');
            const ta = box.querySelector('textarea');
            if (ta.value.trim()) {
                ta.value = '';
                box.classList.remove('open');
                bumpEchoCount();
            }
        });
    });

    // ---- Composer expand/collapse ----
    const echoInput = document.getElementById('echo-input');
    const echoActions = document.getElementById('echo-actions');
    const echoCancel = document.getElementById('echo-cancel');
    // const echoSubmit = document.getElementById('echo-submit');
    const echoList = document.getElementById('echo-list');
    const echoesCount = document.getElementById('echoes-count');

    function autoGrow(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
    }

    echoInput.addEventListener('input', () => {
        autoGrow(echoInput);
        echoActions.classList.toggle('hidden', echoInput.value.trim().length === 0);
        echoActions.classList.toggle('flex', echoInput.value.trim().length > 0);
    });

    echoCancel.addEventListener('click', () => {
        echoInput.value = '';
        echoInput.style.height = 'auto';
        echoActions.classList.add('hidden');
        echoActions.classList.remove('flex');
    });

    function bumpEchoCount() {
        const n = parseInt(echoesCount.textContent, 10);
        echoesCount.textContent = n + 1;
    }

    function timeAgoLabel() { return 'Just now'; }

    function postEcho() {
        const text = echoInput.value.trim();
        if (!text) return;

        const node = document.createElement('div');
        node.className = 'thread-line echo-enter';
        node.innerHTML = `
      <div class="flex gap-3">
        <div class="w-9 h-9 rounded-full bg-[var(--gold)]/15 border border-[var(--gold-soft)]/40 flex items-center justify-center shrink-0">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-sm font-semibold">Arjun Singh</span>
            <span class="text-[10px] font-semibold text-[var(--jade)]">(You)</span>
            <span class="text-xs text-[var(--ink-dim)]">${timeAgoLabel()}</span>
          </div>
          <p class="font-serif-flow text-[1.05rem] leading-relaxed text-[var(--ink)]/85 mt-1.5"></p>
          <div class="flex items-center gap-4 mt-2">
            <button class="like-btn flex items-center gap-1.5 text-xs text-[var(--ink-dim)] hover:text-[var(--gold)] transition-colors">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 10v12M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/></svg>
              <span class="like-count">0</span>
            </button>
            <button class="reply-toggle text-xs font-semibold text-[var(--ink-dim)] hover:text-[var(--gold)] transition-colors flex items-center gap-1.5">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 17H4a1 1 0 0 1-1-1v-2a4 4 0 0 1 4-4h4M14 7l5 5-5 5"/></svg>
              Reply
            </button>
          </div>
          <div class="reply-box">
            <textarea rows="2" placeholder="Write a reply..." class="w-full bg-[#0d100b] border border-[var(--line)] rounded-lg p-2.5 text-sm resize-none placeholder:text-[var(--ink-dim)]"></textarea>
            <div class="flex justify-end mt-2">
              <button class="reply-submit text-xs font-semibold bg-[var(--jade)] text-[#0a0d0a] px-3.5 py-1.5 rounded-full hover:brightness-110 transition-all">Send Reply</button>
            </div>
          </div>
        </div>
      </div>`;
        node.querySelector('p').textContent = text;

        echoList.prepend(node);
        bumpEchoCount();
        wireEcho(node);

        echoInput.value = '';
        echoInput.style.height = 'auto';
        echoActions.classList.add('hidden');
        echoActions.classList.remove('flex');
    }

    // echoSubmit.addEventListener('click', postEcho);
    // echoInput.addEventListener('keydown', (e) => {
    //     if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') postEcho();
    // });

    function wireEcho(scope) {
        scope.querySelectorAll('.like-btn').forEach(btn => {
            let liked = false;
            btn.addEventListener('click', () => {
                liked = !liked;
                const countEl = btn.querySelector('.like-count');
                let n = parseInt(countEl.textContent, 10);
                countEl.textContent = liked ? n + 1 : n - 1;
                btn.classList.toggle('text-[var(--jade)]', liked);
            });
        });
        scope.querySelectorAll('.reply-toggle').forEach(btn => {
            btn.addEventListener('click', () => {
                const box = btn.closest('.flex-1').querySelector('.reply-box');
                box.classList.toggle('open');
                if (box.classList.contains('open')) {
                    setTimeout(() => box.querySelector('textarea').focus(), 200);
                }
            });
        });
        scope.querySelectorAll('.reply-submit').forEach(btn => {
            btn.addEventListener('click', () => {
                const box = btn.closest('.reply-box');
                const ta = box.querySelector('textarea');
                if (ta.value.trim()) {
                    ta.value = '';
                    box.classList.remove('open');
                    bumpEchoCount();
                }
            });
        });
    }
})();