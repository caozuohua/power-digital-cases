// Power Industry Digital Transformation Case Studies
// data/cases.json → searchable, filterable, tag-driven

let allCases = [];
let activeFilters = { country: '', scale: '', year: '', tag: '', search: '' };

// ── Init ──
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('data/cases.json');
    allCases = await res.json();
  } catch (e) {
    console.error('Failed to load cases.json:', e);
    document.getElementById('case-list').innerHTML = '<p style="color:red">数据加载失败，请检查 data/cases.json</p>';
    return;
  }
  buildFilters();
  buildTagCloud();
  render();
  bindEvents();
});

// ── Build filter dropdowns ──
function buildFilters() {
  const countries = [...new Set(allCases.map(c => c.country))].sort();
  const scales = [...new Set(allCases.map(c => c.scale))];
  const years = [...new Set(allCases.map(c => c.year))].sort((a, b) => b - a);

  fillSelect('filter-country', countries);
  fillSelect('filter-scale', scales);
  fillSelect('filter-year', years);
}

function fillSelect(id, items) {
  const sel = document.getElementById(id);
  items.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v;
    opt.textContent = v;
    sel.appendChild(opt);
  });
}

// ── Tag cloud ──
function buildTagCloud() {
  const tagCounts = {};
  allCases.forEach(c => (c.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
  const sorted = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]);
  const container = document.getElementById('tag-cloud');
  container.innerHTML = '';
  sorted.forEach(([tag, count]) => {
    const btn = document.createElement('button');
    btn.className = 'tag';
    btn.textContent = `${tag} (${count})`;
    btn.dataset.tag = tag;
    btn.addEventListener('click', () => toggleTag(tag));
    container.appendChild(btn);
  });
}

function toggleTag(tag) {
  if (activeFilters.tag === tag) {
    activeFilters.tag = '';
  } else {
    activeFilters.tag = tag;
  }
  updateTagActive();
  render();
}

function updateTagActive() {
  document.querySelectorAll('#tag-cloud .tag').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tag === activeFilters.tag);
  });
}

// ── Filtering ──
function getFiltered() {
  return allCases.filter(c => {
    if (activeFilters.country && c.country !== activeFilters.country) return false;
    if (activeFilters.scale && c.scale !== activeFilters.scale) return false;
    if (activeFilters.year && c.year !== parseInt(activeFilters.year)) return false;
    if (activeFilters.tag && !(c.tags || []).includes(activeFilters.tag)) return false;
    if (activeFilters.search) {
      const q = activeFilters.search.toLowerCase();
      const haystack = [
        c.title, c.company, c.country, c.summary, c.detail || '',
        ...(c.tech || []), ...(c.tags || [])
      ].join(' ').toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });
}

// ── Render ──
function render() {
  const filtered = getFiltered();
  const grid = document.getElementById('case-list');
  const noResult = document.getElementById('no-result');
  const stats = document.getElementById('stats');
  const totalCount = document.getElementById('total-count');

  stats.textContent = `显示 ${filtered.length} / ${allCases.length} 个案例`;
  totalCount.textContent = `共收录 ${allCases.length} 个案例`;

  if (filtered.length === 0) {
    grid.innerHTML = '';
    noResult.style.display = 'block';
    return;
  }
  noResult.style.display = 'none';

  grid.innerHTML = filtered.map(c => `
    <div class="case-card" data-id="${c.id}">
      <span class="country">${c.country}</span>
      <h3>${c.title}</h3>
      <div class="company">${c.company} · ${c.year}</div>
      <div class="summary">${c.summary}</div>
      <div class="card-tags">${(c.tags || []).map(t => `<span>${t}</span>`).join('')}</div>
      <div class="meta">
        <span>${c.scale}</span>
        <span>${c.investment}</span>
      </div>
    </div>
  `).join('');

  // Bind card clicks
  grid.querySelectorAll('.case-card').forEach(card => {
    card.addEventListener('click', () => openModal(card.dataset.id));
  });
}

// ── Modal ──
function openModal(id) {
  const c = allCases.find(x => x.id === id);
  if (!c) return;
  const modal = document.getElementById('modal');
  const body = document.getElementById('modal-body');
  body.innerHTML = `
    <h2>${c.title}</h2>
    <div class="modal-company">${c.company} · ${c.country} · ${c.year}</div>
    <div class="modal-meta">
      <div class="meta-item"><label>规模</label><span>${c.scale}</span></div>
      <div class="meta-item"><label>投资额</label><span>${c.investment}</span></div>
      <div class="meta-item"><label>成效</label><span>${c.roi}</span></div>
      <div class="meta-item"><label>技术</label><span>${(c.tech || []).join('、')}</span></div>
    </div>
    <div class="modal-detail">${c.detail || c.summary}</div>
    <div class="modal-tags">${(c.tags || []).map(t => `<span>${t}</span>`).join('')}</div>
    <div class="modal-source">来源：<a href="${c.source}" target="_blank" rel="noopener">${c.source}</a></div>
  `;
  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
  document.body.style.overflow = '';
}

// ── Events ──
function bindEvents() {
  // Search
  let searchTimer;
  document.getElementById('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      activeFilters.search = e.target.value.trim();
      render();
    }, 200);
  });

  // Dropdowns
  ['filter-country', 'filter-scale', 'filter-year'].forEach(id => {
    document.getElementById(id).addEventListener('change', e => {
      const key = id.replace('filter-', '');
      activeFilters[key] = e.target.value;
      render();
    });
  });

  // Reset
  document.getElementById('btn-reset').addEventListener('click', () => {
    activeFilters = { country: '', scale: '', year: '', tag: '', search: '' };
    document.getElementById('search-input').value = '';
    document.getElementById('filter-country').value = '';
    document.getElementById('filter-scale').value = '';
    document.getElementById('filter-year').value = '';
    updateTagActive();
    render();
  });

  // Modal
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.querySelector('.modal-overlay').addEventListener('click', closeModal);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
}
