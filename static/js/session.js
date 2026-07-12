
  // ---------- DATA ----------
  const sessions = {
    live: [
      {
        img: "https://images.unsplash.com/photo-1596568802910-9d0a49f5fc12?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=100&h=100&fit=crop",
        mentor: "Master Liang", role: "Grandmaster Architect",
        tags: ["FRONTEND", "INTERMEDIATE"],
        title: "Mastering the React Talisman: Advanced Hooks",
        desc: "Understand how to channel component state through custom hooks without disturbing the spiritual balance of your app.",
        meta: "432 Disciples", metaIcon: "users", cta: "Join Pavilion", ctaStyle: "glow", status: "LIVE NOW"
      },
      {
        img: "https://images.unsplash.com/photo-1548013146-72479768bada?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop",
        mentor: "Disciple Chen", role: "Database Sessions · SkillForge",
        tags: ["BACKEND", "BEGINNER"],
        title: "Forging Persistent Realms: The SQL Rite",
        desc: "Learn the foundational runes of data persistence and how to query the celestial archives efficiently.",
        meta: "Today, 4:00 PM", metaIcon: "calendar", cta: "Set Reminder", ctaStyle: "ghost", status: "STARTS IN 2H"
      },
      {
        img: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop",
        mentor: "Elder Zhang", role: "Cloud Immortal",
        tags: ["DEVOPS", "ADVANCED"],
        title: "Ascending to the Cloud: Deployment Rituals",
        desc: "Automate your cultivation path with CI/CD pipelines that never flicker, even in the coldest server winters.",
        meta: "Tomorrow, 10:00 AM", metaIcon: "clock", cta: "Set Reminder", ctaStyle: "ghost", status: "TOMORROW"
      }
    ],
    upcoming: [
      {
        img: "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=100&h=100&fit=crop",
        mentor: "Grand Architect Hana", role: "UI Sage",
        tags: ["FRONTEND", "BEGINNER"],
        title: "Visual Qi: Balancing Layout Energies",
        desc: "Discover how spacing, rhythm, and hierarchy channel the eye like qi through meridians.",
        meta: "Fri, 6:00 PM", metaIcon: "calendar", cta: "Set Reminder", ctaStyle: "ghost", status: "IN 3 DAYS"
      },
      {
        img: "https://images.unsplash.com/photo-1526378800651-c32d170fe6f8?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop",
        mentor: "Sect Guard Kael", role: "API Sentinel",
        tags: ["BACKEND", "INTERMEDIATE"],
        title: "API Gatekeeper Rituals: Auth & Rate Limits",
        desc: "Ward your endpoints against intruders with tokens, throttles, and vigilant middleware.",
        meta: "Sat, 11:00 AM", metaIcon: "calendar", cta: "Set Reminder", ctaStyle: "ghost", status: "IN 4 DAYS"
      },
      {
        img: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=100&h=100&fit=crop",
        mentor: "Master Liang", role: "Grandmaster Architect",
        tags: ["FRONTEND", "ADVANCED"],
        title: "The Binary Fist Technique: Bitwise Mastery",
        desc: "Strike straight to the bit-level truth behind flags, masks, and lightning-fast operations.",
        meta: "Next Mon, 2:00 PM", metaIcon: "calendar", cta: "Set Reminder", ctaStyle: "ghost", status: "NEXT WEEK"
      }
    ],
    recorded: [
      {
        img: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=100&h=100&fit=crop",
        mentor: "Master Liang", role: "Grandmaster Architect",
        tags: ["FRONTEND", "ALL LEVELS"],
        title: "Clean Code Sutras",
        desc: "The founding scripture on writing code that future disciples can actually read.",
        meta: "45:12 · Oct 12", metaIcon: "play", cta: "Watch Now", ctaStyle: "ghost", status: "RECORDED"
      },
      {
        img: "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop",
        mentor: "Elder Zhao", role: "Systems Immortal",
        tags: ["ALGORITHMS", "ADVANCED"],
        title: "The Binary Fist Tech",
        desc: "Precision strikes at the bit level — the full technique, uncut.",
        meta: "1:02:05 · Oct 10", metaIcon: "play", cta: "Watch Now", ctaStyle: "ghost", status: "RECORDED"
      },
      {
        img: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop",
        mentor: "Sect Guard Kael", role: "API Sentinel",
        tags: ["BACKEND", "INTERMEDIATE"],
        title: "API Gatekeeper Rituals",
        desc: "The original recording — warding endpoints with tokens and vigilant middleware.",
        meta: "38:50 · Oct 08", metaIcon: "play", cta: "Watch Now", ctaStyle: "ghost", status: "RECORDED"
      },
      {
        img: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=340&fit=crop",
        mentorImg: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=100&h=100&fit=crop",
        mentor: "Grand Architect Hana", role: "UI Sage",
        tags: ["FRONTEND", "BEGINNER"],
        title: "Visual Qi: UI Balancing",
        desc: "Layout rhythm, hierarchy, and the eye's natural path across a screen.",
        meta: "55:20 · Oct 05", metaIcon: "play", cta: "Watch Now", ctaStyle: "ghost", status: "RECORDED"
      }
    ]
  };

  const archive = sessions.recorded;

  const icons = {
    users: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    calendar: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 3v3M16 3v3"/></svg>',
    clock: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>',
    play: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
  };

  let currentTab = 'live';
  const grid = document.getElementById('cardsGrid');
  const archiveGrid = document.getElementById('archiveGrid');
  const searchInput = document.getElementById('searchInput');

  function statusBadge(status){
    const live = status === 'LIVE NOW';
    return `<span class="badge inline-flex items-center gap-1.5 font-semibold uppercase px-2.5 py-1 rounded-full ${live ? 'bg-[var(--gold)] text-[#1a1305]' : 'bg-black/50 text-[var(--gold-soft)] border border-[var(--line)]'}">
      ${live ? '<span class="w-1.5 h-1.5 rounded-full bg-[#1a1305] pulse-dot"></span>' : ''}${status}
    </span>`;
  }

  function tagPill(tag, i){
    const colors = ['text-[var(--jade)] border-[var(--jade)]/30', 'text-[var(--amethyst)] border-[var(--amethyst)]/30'];
    return `<span class="text-[10px] tracking-wider font-medium px-2 py-1 rounded border ${colors[i % 2]} bg-white/[0.02]">${tag}</span>`;
  }

  function renderCard(s, idx){
    const ctaClass = s.ctaStyle === 'glow'
      ? 'glow-btn'
      : 'ghost-btn';
    return `
    <article class="card card-enter rounded-2xl overflow-hidden flex flex-col group" style="animation-delay:${idx*40}ms">
      <div class="relative h-44 overflow-hidden">
        <img src="${s.img}" alt="${s.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent"></div>
        <div class="absolute top-3 right-3">${statusBadge(s.status)}</div>
        <div class="absolute bottom-3 left-3 flex items-center gap-2">
          <img src="${s.mentorImg}" class="w-9 h-9 rounded-full border-2 border-[var(--gold)] object-cover" alt="${s.mentor}">
          <div class="leading-tight">
            <p class="text-sm font-semibold text-white">${s.mentor}</p>
            <p class="text-[10px] tracking-wider text-[var(--gold-soft)]/90 uppercase">${s.role}</p>
          </div>
        </div>
      </div>
      <div class="p-5 flex flex-col flex-1">
        <div class="flex gap-2 mb-3">${s.tags.map(tagPill).join('')}</div>
        <h4 class="font-display font-bold text-lg leading-snug mb-2">${s.title}</h4>
        <p class="text-sm text-[var(--muted)] leading-relaxed flex-1">${s.desc}</p>
        <div class="flex items-center justify-between mt-5 pt-4 border-t border-[var(--line)]">
          <span class="flex items-center gap-1.5 text-xs text-[var(--muted)]">${icons[s.metaIcon]}${s.meta}</span>
          <button data-action="${s.cta}" data-title="${s.title}" class="cta-btn ${ctaClass} text-sm font-medium px-4 py-2 rounded-lg transition whitespace-nowrap">${s.cta}</button>
        </div>
      </div>
    </article>`;
  }

  function renderArchiveCard(s){
    return `
    <article class="card card-enter rounded-xl overflow-hidden cursor-pointer group" data-watch="${s.title}">
      <div class="relative h-28 sm:h-36 overflow-hidden">
        <img src="${s.img}" alt="${s.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-black/25 group-hover:bg-black/10 transition flex items-center justify-center">
          <div class="w-9 h-9 rounded-full bg-[var(--gold)]/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="#1a1305"><path d="M8 5v14l11-7z"/></svg>
          </div>
        </div>
        <span class="absolute bottom-1.5 right-1.5 text-[10px] bg-black/70 px-1.5 py-0.5 rounded text-[var(--gold-soft)] font-mono">${s.meta.split('·')[0].trim()}</span>
      </div>
      <div class="p-3">
        <p class="text-sm font-semibold leading-snug truncate">${s.title}</p>
        <p class="text-[10px] tracking-wider text-[var(--muted)] uppercase mt-1 truncate">${s.mentor} · ${s.meta.split('·')[1] ? s.meta.split('·')[1].trim() : ''}</p>
      </div>
    </article>`;
  }

  function renderTab(){
    const query = searchInput.value.trim().toLowerCase();
    const list = sessions[currentTab].filter(s =>
      !query || s.title.toLowerCase().includes(query) || s.mentor.toLowerCase().includes(query) || s.tags.join(' ').toLowerCase().includes(query)
    );
    grid.innerHTML = list.length
      ? list.map(renderCard).join('')
      : `<div class="col-span-full text-center py-16 text-[var(--muted)]">
           <p class="font-display text-lg text-[var(--gold-soft)] mb-1">No sessions found</p>
           <p class="text-sm">Try a different search, disciple.</p>
         </div>`;
    attachCardHandlers();
  }

  function renderArchive(){
    archiveGrid.innerHTML = archive.map(renderArchiveCard).join('');
    archiveGrid.querySelectorAll('[data-watch]').forEach(el => {
      el.addEventListener('click', () => showToast(`Now watching "${el.dataset.watch}"`, 'jade'));
    });
  }

  function attachCardHandlers(){
    grid.querySelectorAll('.cta-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        const title = btn.dataset.title;
        if(action === 'Join Pavilion'){
          showToast(`Joining "${title}" — may your qi flow steady.`, 'gold');
        } else if(action === 'Set Reminder'){
          const wasSet = btn.dataset.set === 'true';
          btn.dataset.set = wasSet ? 'false' : 'true';
          btn.textContent = wasSet ? 'Set Reminder' : 'Reminder Set ✓';
          btn.classList.toggle('ghost-btn', wasSet);
          btn.classList.toggle('glow-btn', !wasSet);
          showToast(wasSet ? `Reminder removed for "${title}"` : `Reminder set for "${title}"`, wasSet ? 'muted' : 'jade');
        } else if(action === 'Watch Now'){
          showToast(`Opening recording: "${title}"`, 'jade');
        }
      });
    });
  }

  // ---------- TOASTS ----------
  function showToast(msg, tone='gold'){
    const wrap = document.getElementById('toastWrap');
    const colors = {
      gold: 'border-[var(--gold)]/40 text-[var(--gold-soft)]',
      jade: 'border-[var(--jade)]/40 text-[var(--jade)]',
      muted: 'border-[var(--line)] text-[var(--muted)]'
    };
    const el = document.createElement('div');
    el.className = `toast card border ${colors[tone] || colors.gold} rounded-lg px-4 py-3 text-sm shadow-xl max-w-xs`;
    el.textContent = msg;
    wrap.appendChild(el);
    setTimeout(() => {
      el.style.transition = 'opacity .3s, transform .3s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(10px)';
      setTimeout(() => el.remove(), 300);
    }, 2600);
  }

  // ---------- TABS ----------
  document.getElementById('tabGroup').addEventListener('click', (e) => {
    const btn = e.target.closest('[data-tab]');
    if(!btn) return;
    document.querySelectorAll('.tab-btn').forEach(b => {
      b.classList.remove('active');
      b.classList.add('text-[var(--muted)]');
    });
    btn.classList.add('active');
    btn.classList.remove('text-[var(--muted)]');
    currentTab = btn.dataset.tab;
    renderTab();
  });

  searchInput.addEventListener('input', renderTab);

  // ---------- HERO / TOP ACTIONS ----------
  document.getElementById('joinPavilionHero').addEventListener('click', () => {
    showToast('Entering the Live Pavilion...', 'gold');
  });

  document.getElementById('viewArchiveLink').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('archiveGrid').scrollIntoView({behavior:'smooth', block:'center'});
    showToast('Browsing the full archive', 'jade');
  });

  document.getElementById('logoutBtn').addEventListener('click', () => {
    showToast('Farewell, disciple. Come back soon.', 'muted');
  });

  // ---------- SIDEBAR NAV ----------
  document.getElementById('mainNav').addEventListener('click', (e) => {
    const link = e.target.closest('.nav-item');
    if(!link) return;
    e.preventDefault();
    document.querySelectorAll('#mainNav .nav-item').forEach(n => n.classList.remove('active'));
    link.classList.add('active');
    const label = link.textContent.trim();
    if(label !== 'Sessions') showToast(`"${label}" page is under construction in this preview.`, 'muted');
  });

  // ---------- MOBILE MENU ----------
  const menuBtn = document.getElementById('menuBtn');
  const closeMenuBtn = document.getElementById('closeMenuBtn');
  const mobileSidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('overlay');
  function openMenu(){ mobileSidebar.classList.remove('hidden'); overlay.classList.remove('hidden'); }
  function closeMenu(){ mobileSidebar.classList.add('hidden'); overlay.classList.add('hidden'); }
  menuBtn.addEventListener('click', openMenu);
  closeMenuBtn.addEventListener('click', closeMenu);
  overlay.addEventListener('click', closeMenu);

  // ---------- INIT ----------
  renderTab();
  renderArchive();