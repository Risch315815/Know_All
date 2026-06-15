// 全知專案 — main.js
// Manages domain cards: load from localStorage, render, add new domains.

const STORAGE_KEY = 'knowall_domains';

const DEFAULT_DOMAINS = [
  {
    name: 'Self-Paid Medical Tx (TW)',
    desc: '65歲父親自費醫療項目整理 — 台灣醫學中心費用參考',
    icon: '🏥',
    slug: 'Self-Paid Medical Tx_TW',
    updatedAt: Date.now(),
  },
];

// ── Storage ──────────────────────────────────────────────

function loadDomains() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : DEFAULT_DOMAINS;
  } catch {
    return DEFAULT_DOMAINS;
  }
}

function saveDomains(domains) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(domains));
}

// ── Render ────────────────────────────────────────────────

function renderDomains() {
  const grid = document.getElementById('domainsGrid');
  if (!grid) return;

  const domains = loadDomains();
  grid.innerHTML = '';

  if (domains.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">◈</div>
        <p>還沒有任何知識領域<br />點擊下方按鈕新增第一個領域</p>
      </div>`;
    return;
  }

  domains.forEach((domain, index) => {
    const card = document.createElement('a');
    card.className = 'domain-card';
    card.href = `domains/${domain.slug}/index.html`;

    const updatedAt = domain.updatedAt
      ? new Date(domain.updatedAt).toLocaleDateString('zh-Hant', { month: 'short', day: 'numeric' })
      : '剛建立';

    card.innerHTML = `
      <div class="domain-card-icon">${domain.icon || '◈'}</div>
      <div class="domain-card-name">${escapeHtml(domain.name)}</div>
      <div class="domain-card-desc">${escapeHtml(domain.desc || '')}</div>
      <div class="domain-card-meta">
        <span class="domain-card-status">更新 ${updatedAt}</span>
        <span class="domain-card-arrow">→</span>
      </div>`;

    grid.appendChild(card);
  });
}

// ── Modal ─────────────────────────────────────────────────

function openModal() {
  document.getElementById('modalOverlay').classList.add('open');
  document.getElementById('domainName').focus();
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.getElementById('domainName').value = '';
  document.getElementById('domainDesc').value = '';
  document.getElementById('domainIcon').value = '';
}

function confirmAddDomain() {
  const name = document.getElementById('domainName').value.trim();
  const desc = document.getElementById('domainDesc').value.trim();
  const icon = document.getElementById('domainIcon').value.trim() || '◈';

  if (!name) {
    document.getElementById('domainName').focus();
    return;
  }

  const domains = loadDomains();
  const slug = toSlug(name);

  if (domains.find(d => d.slug === slug)) {
    alert(`「${name}」已存在`);
    return;
  }

  domains.push({ name, desc, icon, slug, updatedAt: Date.now() });
  saveDomains(domains);
  closeModal();
  renderDomains();
}

// ── Utils ─────────────────────────────────────────────────

function toSlug(str) {
  return str
    .toLowerCase()
    .replace(/[\s\u3000]+/g, '-')
    .replace(/[^\w\u4e00-\u9fff\-]/g, '')
    .replace(/^-+|-+$/g, '') || `domain-${Date.now()}`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Init ──────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  renderDomains();

  const addBtn   = document.getElementById('addDomainBtn');
  const overlay  = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalClose');
  const cancelBtn = document.getElementById('modalCancel');
  const confirmBtn = document.getElementById('modalConfirm');

  if (addBtn)    addBtn.addEventListener('click', openModal);
  if (closeBtn)  closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
  if (confirmBtn) confirmBtn.addEventListener('click', confirmAddDomain);

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
    if (e.key === 'Enter' && overlay && overlay.classList.contains('open')) {
      confirmAddDomain();
    }
  });
});
