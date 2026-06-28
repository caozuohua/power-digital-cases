// ═══════════════════════════════════════════════════
// Power Digital Cases — Frontend App
// Map (Leaflet) + Charts (Chart.js) + Search/Filter
// ═══════════════════════════════════════════════════

// ── Config ──
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/caozuohua/power-digital-cases/main';
const GEOJSON_URL = `${GITHUB_RAW_BASE}/data/world.geojson`;
let allCases = [];
let map = null;
let markers = null;
let chartsBuilt = false;

// ── Country center coordinates ──
const COUNTRY_COORDS = {
  '中国': [35.86, 104.19], '美国': [37.09, -95.71], '德国': [51.16, 10.45],
  '全球': [20, 0], '英国': [55.38, -3.44], '澳大利亚': [-25.27, 133.78],
  '意大利': [41.87, 12.46], '日本': [36.20, 138.25], '印度': [20.59, 78.96],
  '瑞士': [46.82, 8.23], '韩国': [35.91, 127.77], '哥伦比亚': [4.57, -74.30],
  '西班牙': [40.46, -3.75], '巴西': [-14.24, -51.93], '挪威': [59.95, 10.75],
  '法国': [46.23, 2.21], '泰国': [15.87, 100.99], '瑞典': [60.13, 18.64],
  '越南': [14.06, 108.28], '阿联酋': [23.42, 53.85], '新加坡': [1.35, 103.82],
  '丹麦': [56.26, 9.50], '南非': [-30.56, 22.94], '尼日利亚': [9.08, 8.68],
  '肯尼亚': [-1.29, 36.82], '比利时': [50.50, 4.47], '波兰': [51.92, 19.15],
  '荷兰': [52.13, 5.29], '菲律宾': [12.88, 121.77], '伊拉克': [33.22, 43.68],
  '印度尼西亚': [-0.79, 113.92], '墨西哥': [23.63, -102.55],
  '沙特阿拉伯': [23.89, 45.08], '阿曼': [21.47, 55.98], '马来西亚': [4.21, 101.98],
  '匈牙利': [47.16, 19.50], '埃及': [26.82, 30.80], '捷克': [49.82, 15.47],
  '摩洛哥': [31.79, -7.09], '约旦': [30.59, 36.24], '罗马尼亚': [45.94, 24.97],
  '加拿大': [56.13, -106.35], '莫桑比克': [-18.67, 35.53]
};

const CHART_COLORS = ['#0f4c81','#00c9a7','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#10b981','#f97316','#ec4899','#6366f1'];

// ── Init ──
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch(`${GITHUB_RAW_BASE}/data/cases.json`);
    allCases = await res.json();
  } catch (e) {
    try {
      const res = await fetch('data/cases.json');
      allCases = await res.json();
    } catch (e2) {
      console.error('Failed to load cases.json:', e2);
      document.getElementById('case-list').innerHTML = '<p style="color:red;padding:40px;text-align:center">数据加载失败。请确认 data/cases.json 存在。</p>';
      return;
    }
  }

  buildStats();
  buildFilters();
  buildTagCloud();
  render();
  bindEvents();
  initMap();
  initCharts();
});

// ── Hero Stats ──
function buildStats() {
  const countries = new Set(allCases.map(c => c.country));
  const companies = new Set(allCases.map(c => c.company));
  const years = [...new Set(allCases.map(c => c.year))].sort((a,b) => b-a);
  const statsEl = document.getElementById('hero-stats');
  statsEl.innerHTML = `
    <div class="hero-stat"><div class="num">${allCases.length}</div><div class="label">Cases</div></div>
    <div class="hero-stat"><div class="num">${countries.size}</div><div class="label">Countries</div></div>
    <div class="hero-stat"><div class="num">${companies.size}</div><div class="label">Companies</div></div>
    <div class="hero-stat"><div class="num">${years[0]}-${years[years.length-1]}</div><div class="label">Range</div></div>
  `;
  document.getElementById('total-count').textContent = `共 ${allCases.length} 个案例 · ${countries.size} 个国家 · ${companies.size} 家企业`;
}

// ── Filters ──
function buildFilters() {
  const countries = [...new Set(allCases.map(c => c.country))].filter(c => c !== '全球').sort();
  const scales = [...new Set(allCases.map(c => c.scale))].filter(s => !/[0-9]/.test(s) && !s.includes('亿') && !s.includes('MW'));
  const years = [...new Set(allCases.map(c => c.year))].sort((a, b) => b - a);
  const confidences = [...new Set(allCases.map(c => c.confidence || '未标注'))];

  fillSelect('filter-country', countries);
  fillSelect('filter-scale', scales);
  fillSelect('filter-year', years);
  fillSelect('filter-confidence', confidences);
}

function fillSelect(id, items) {
  const el = document.getElementById(id);
  if (!el) return;
  items.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v;
    opt.textContent = v;
    el.appendChild(opt);
  });
}

// ── Tag Cloud ──
function buildTagCloud() {
  const tagCounts = {};
  allCases.forEach(c => (c.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
  const sorted = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]);
  const container = document.getElementById('tag-cloud');
  container.innerHTML = '';
  sorted.forEach(([tag, count]) => {
    const btn = document.createElement('button');
    btn.className = 'tag';
    btn.innerHTML = `${tag} <span class="count">${count}</span>`;
    btn.dataset.tag = tag;
    btn.addEventListener('click', () => toggleTag(tag));
    container.appendChild(btn);
  });
}

// ── Filtering ──
let activeFilters = { country: '', scale: '', year: '', tag: '', search: '', confidence: '' };

function toggleTag(tag) {
  activeFilters.tag = activeFilters.tag === tag ? '' : tag;
  updateTagActive();
  render();
}

function updateTagActive() {
  document.querySelectorAll('#tag-cloud .tag').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tag === activeFilters.tag);
  });
}

function getFiltered() {
  return allCases.filter(c => {
    if (activeFilters.country && c.country !== activeFilters.country) return false;
    if (activeFilters.scale && c.scale !== activeFilters.scale) return false;
    if (activeFilters.year && c.year !== parseInt(activeFilters.year)) return false;
    if (activeFilters.tag && !(c.tags || []).includes(activeFilters.tag)) return false;
    if (activeFilters.confidence && (c.confidence || '未标注') !== activeFilters.confidence) return false;
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

  stats.textContent = `Showing ${filtered.length} / ${allCases.length} cases`;

  if (filtered.length === 0) {
    grid.innerHTML = '';
    noResult.style.display = 'block';
    return;
  }
  noResult.style.display = 'none';

  grid.innerHTML = filtered.map(c => `
    <div class="case-card" data-id="${c.id}">
      <div class="card-header">
        <span class="country">${c.country}</span>
        ${confidenceBadge(c)}
      </div>
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

  grid.querySelectorAll('.case-card').forEach(card => {
    card.addEventListener('click', () => openModal(card.dataset.id));
  });
}

function confidenceBadge(c) {
  const level = c.confidence || '未标注';
  const cls = level === '高' ? 'conf-high' : level === '中' ? 'conf-mid' : level === '低' ? 'conf-low' : 'conf-none';
  return `<span class="confidence ${cls}">${level}</span>`;
}

// ── Modal ──
function openModal(id) {
  const c = allCases.find(x => x.id === id);
  if (!c) return;
  const modal = document.getElementById('modal');
  const body = document.getElementById('modal-body');
  body.innerHTML = `
    <h2>${c.title}</h2>
    <div class="modal-company">${c.company} · ${c.country} · ${c.year} · Confidence: ${confidenceBadge(c)}</div>
    <div class="modal-meta">
      <div class="meta-item"><label>Scale</label><span>${c.scale}</span></div>
      <div class="meta-item"><label>Investment</label><span>${c.investment}</span></div>
      <div class="meta-item"><label>ROI</label><span>${c.roi || 'N/A'}</span></div>
      <div class="meta-item"><label>Tech</label><span>${(c.tech || []).join(', ')}</span></div>
    </div>
    <div class="modal-detail">${c.detail || c.summary}</div>
    <div class="modal-tags">${(c.tags || []).map(t => `<span>${t}</span>`).join('')}</div>
    <div class="modal-source">Source: <a href="${c.source}" target="_blank" rel="noopener">${c.source}</a></div>
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
  let searchTimer;
  document.getElementById('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      activeFilters.search = e.target.value.trim();
      render();
    }, 250);
  });

  ['filter-country', 'filter-scale', 'filter-year', 'filter-confidence'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', e => {
      const key = id.replace('filter-', '');
      activeFilters[key] = e.target.value;
      render();
    });
  });

  document.getElementById('btn-reset').addEventListener('click', () => {
    activeFilters = { country: '', scale: '', year: '', tag: '', search: '', confidence: '' };
    document.getElementById('search-input').value = '';
    document.getElementById('filter-country').value = '';
    document.getElementById('filter-scale').value = '';
    document.getElementById('filter-year').value = '';
    const confEl = document.getElementById('filter-confidence');
    if (confEl) confEl.value = '';
    updateTagActive();
    render();
  });

  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.querySelector('.modal-overlay').addEventListener('click', closeModal);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
}

// ── Map ──
function initMap() {
  map = L.map('world-map', {
    center: [25, 20],
    zoom: 2,
    minZoom: 2,
    maxZoom: 8,
    zoomControl: true,
    scrollWheelZoom: true,
    worldCopyJump: true
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);

  // Aggregate by country
  const countryCounts = {};
  allCases.forEach(c => {
    if (c.country === '全球') return;
    countryCounts[c.country] = (countryCounts[c.country] || 0) + 1;
  });

  // Bubble markers
  const maxCount = Math.max(...Object.values(countryCounts));
  markers = L.layerGroup().addTo(map);

  Object.entries(countryCounts).forEach(([country, count]) => {
    const coords = COUNTRY_COORDS[country];
    if (!coords) return;
    const radius = Math.max(8, (count / maxCount) * 40);
    const circle = L.circleMarker(coords, {
      radius: radius,
      fillColor: '#0f4c81',
      color: '#00c9a7',
      weight: 2,
      opacity: 0.9,
      fillOpacity: 0.6,
    });

    // Top tags for this country
    const cTags = {};
    allCases.filter(c => c.country === country).forEach(c => {
      (c.tags || []).forEach(t => { cTags[t] = (cTags[t] || 0) + 1; });
    });
    const topTags = Object.entries(cTags).sort((a,b) => b[1]-a[1]).slice(0,3).map(([t]) => t).join(', ');

    circle.bindPopup(`
      <div class="popup-title">${country}</div>
      <div class="popup-count">${count} case(s)</div>
      <div class="popup-tags">Top: ${topTags}</div>
    `);

    circle.on('click', () => {
      activeFilters.country = country;
      document.getElementById('filter-country').value = country;
      render();
      // Scroll to cases section
      document.getElementById('cases').scrollIntoView({ behavior: 'smooth' });
    });

    markers.addLayer(circle);
  });

  // Legend
  document.getElementById('map-legend').innerHTML = `
    <div class="legend-item"><div class="legend-dot" style="width:12px;height:12px;background:#0f4c81;border:2px solid #00c9a7;border-radius:50%"></div> 1-10 cases</div>
    <div class="legend-item"><div class="legend-dot" style="width:20px;height:20px;background:#0f4c81;border:2px solid #00c9a7;border-radius:50%"></div> 10-50 cases</div>
    <div class="legend-item"><div class="legend-dot" style="width:30px;height:30px;background:#0f4c81;border:2px solid #00c9a7;border-radius:50%"></div> 50+ cases</div>
  `;
}

// ── Charts (Pure Canvas, zero dependencies) ──
function initCharts() {
  if (chartsBuilt) return;
  chartsBuilt = true;

  const COLORS = ['#0f4c81','#00c9a7','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#10b981','#f97316','#ec4899','#6366f1'];

  // Helper: get canvas from container
  function getCanvas(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    const canvas = document.createElement('canvas');
    container.innerHTML = '';
    container.appendChild(canvas);
    const dpr = window.devicePixelRatio || 1;
    const w = container.clientWidth || 300;
    const h = container.clientHeight || 220;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx, w, h };
  }

  // ── 1. Tech Trend (Multi-line) ──
  const yearTags = {};
  const allYears = [...new Set(allCases.map(c => c.year))].sort();
  allCases.forEach(c => {
    const y = c.year;
    if (!yearTags[y]) yearTags[y] = {};
    (c.tags || []).forEach(t => { yearTags[y][t] = (yearTags[y][t] || 0) + 1; });
  });
  const topTechs = ['AI', '智能电网', '数字孪生', 'IoT', '储能', '虚拟电厂', '需求侧管理', '5G'];
  {
    const cv = getCanvas('trend-chart');
    if (cv) {
      const { ctx, w, h } = cv;
      const pad = { top: 15, right: 15, bottom: 35, left: 38 };
      const cw = w - pad.left - pad.right;
      const ch = h - pad.top - pad.bottom;
      const maxVal = Math.max(...topTechs.map(t => Math.max(...allYears.map(y => (yearTags[y]||{})[t]||0))), 1);

      // Grid + Y labels
      ctx.strokeStyle = '#f1f5f9';
      ctx.fillStyle = '#94a3b8';
      ctx.font = '10px Inter, sans-serif';
      ctx.lineWidth = 1;
      const ySteps = 4;
      for (let i = 0; i <= ySteps; i++) {
        const y = pad.top + ch - (ch * i / ySteps);
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
        const val = Math.round(maxVal * i / ySteps);
        ctx.textAlign = 'right'; ctx.fillText(val, pad.left - 5, y + 3);
      }
      // X labels
      ctx.textAlign = 'center';
      allYears.forEach((yr, i) => {
        const x = pad.left + (cw * i / (allYears.length - 1));
        ctx.fillText(yr, x, h - 8);
      });
      // Lines
      topTechs.forEach((tech, ti) => {
        const data = allYears.map(y => (yearTags[y]||{})[tech] || 0);
        ctx.strokeStyle = COLORS[ti % COLORS.length];
        ctx.lineWidth = 2;
        ctx.beginPath();
        data.forEach((v, i) => {
          const x = pad.left + (cw * i / (data.length - 1));
          const y = pad.top + ch - (ch * v / maxVal);
          i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        });
        ctx.stroke();
        // Dots
        ctx.fillStyle = COLORS[ti % COLORS.length];
        data.forEach((v, i) => {
          const x = pad.left + (cw * i / (data.length - 1));
          const y = pad.top + ch - (ch * v / maxVal);
          ctx.beginPath(); ctx.arc(x, y, 2.5, 0, Math.PI * 2); ctx.fill();
        });
      });
      // Legend
      const legendY = h - 1;
      let legendX = pad.left;
      ctx.font = '9px Inter, sans-serif';
      topTechs.forEach((tech, ti) => {
        ctx.fillStyle = COLORS[ti % COLORS.length];
        ctx.fillRect(legendX, legendY - 8, 8, 8);
        ctx.fillStyle = '#64748b';
        ctx.textAlign = 'left';
        ctx.fillText(tech, legendX + 11, legendY);
        legendX += ctx.measureText(tech).width + 24;
      });
    }
  }

  // ── 2. Confidence Distribution (Doughnut) ──
  const confCounts = {};
  allCases.forEach(c => { const k = c.confidence || '未标注'; confCounts[k] = (confCounts[k] || 0) + 1; });
  {
    const cv = getCanvas('confidence-chart');
    if (cv) {
      const { ctx, w, h } = cv;
      const cx = w / 2, cy = h / 2 - 10;
      const r = Math.min(w, h) / 2 - 30;
      const total = Object.values(confCounts).reduce((a, b) => a + b, 0);
      const colors = ['#00c9a7', '#f59e0b', '#ef4444', '#94a3b8'];
      let angle = -Math.PI / 2;
      const entries = Object.entries(confCounts);
      entries.forEach(([label, val], i) => {
        const slice = (val / total) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, r, angle, angle + slice);
        ctx.closePath();
        ctx.fillStyle = colors[i % colors.length];
        ctx.fill();
        // Label
        const mid = angle + slice / 2;
        const lx = cx + Math.cos(mid) * r * 0.65;
        const ly = cy + Math.sin(mid) * r * 0.65;
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px Inter, sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(val/total*100)}%`, lx, ly);
        angle += slice;
      });
      // Center hole
      ctx.beginPath(); ctx.arc(cx, cy, r * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = '#fff'; ctx.fill();
      ctx.fillStyle = '#1a202c'; ctx.font = 'bold 18px Inter, sans-serif';
      ctx.fillText(total, cx, cy - 6);
      ctx.fillStyle = '#64748b'; ctx.font = '10px Inter, sans-serif';
      ctx.fillText('Total', cx, cy + 10);
      // Legend
      let ly = h - 16;
      let lx = 10;
      entries.forEach(([label, val], i) => {
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillRect(lx, ly - 6, 10, 10);
        ctx.fillStyle = '#64748b'; ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(`${label} (${val})`, lx + 14, ly + 2);
        lx += ctx.measureText(`${label} (${val})`).width + 30;
      });
    }
  }

  // ── 3. Year Distribution (Bar) ──
  const yearCounts = {};
  allCases.forEach(c => { yearCounts[c.year] = (yearCounts[c.year] || 0) + 1; });
  {
    const cv = getCanvas('year-chart');
    if (cv) {
      const { ctx, w, h } = cv;
      const pad = { top: 15, right: 10, bottom: 28, left: 35 };
      const cw = w - pad.left - pad.right;
      const ch = h - pad.top - pad.bottom;
      const entries = Object.entries(yearCounts).sort((a, b) => a[0] - b[0]);
      const maxVal = Math.max(...entries.map(e => e[1]), 1);
      const barW = cw / entries.length * 0.65;
      const gap = cw / entries.length;

      // Grid
      ctx.strokeStyle = '#f1f5f9'; ctx.lineWidth = 1;
      ctx.fillStyle = '#94a3b8'; ctx.font = '10px Inter, sans-serif';
      for (let i = 0; i <= 4; i++) {
        const y = pad.top + ch - (ch * i / 4);
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
        ctx.textAlign = 'right';
        ctx.fillText(Math.round(maxVal * i / 4), pad.left - 5, y + 3);
      }
      // Bars
      entries.forEach(([yr, cnt], i) => {
        const x = pad.left + gap * i + (gap - barW) / 2;
        const barH = (cnt / maxVal) * ch;
        const y = pad.top + ch - barH;
        ctx.fillStyle = '#0f4c81';
        ctx.beginPath();
        ctx.roundRect(x, y, barW, barH, [4, 4, 0, 0]);
        ctx.fill();
        // Value on top
        ctx.fillStyle = '#1a202c'; ctx.font = '9px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(cnt, x + barW / 2, y - 4);
        // X label
        ctx.fillStyle = '#64748b';
        ctx.fillText(yr, x + barW / 2, h - 8);
      });
    }
  }

  // ── 4. Top Tags (Horizontal Bar) ──
  const tagCounts = {};
  allCases.forEach(c => (c.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
  const sortedTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  {
    const cv = getCanvas('tags-chart');
    if (cv) {
      const { ctx, w, h } = cv;
      const pad = { top: 8, right: 35, bottom: 8, left: 80 };
      const cw = w - pad.left - pad.right;
      const ch = h - pad.top - pad.bottom;
      const maxVal = Math.max(...sortedTags.map(e => e[1]), 1);
      const barH = ch / sortedTags.length * 0.6;
      const gap = ch / sortedTags.length;

      sortedTags.forEach(([tag, cnt], i) => {
        const y = pad.top + gap * i + (gap - barH) / 2;
        const barW = (cnt / maxVal) * cw;
        // Tag label
        ctx.fillStyle = '#64748b'; ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(tag, pad.left - 8, y + barH / 2 + 3);
        // Bar
        ctx.fillStyle = '#00c9a7';
        ctx.beginPath();
        ctx.roundRect(pad.left, y, barW, barH, [0, 4, 4, 0]);
        ctx.fill();
        // Value
        ctx.fillStyle = '#1a202c'; ctx.font = '9px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(cnt, pad.left + barW + 5, y + barH / 2 + 3);
      });
    }
  }
}
