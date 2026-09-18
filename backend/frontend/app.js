/**
 * LaunchLens Frontend Application Logic
 * Integrates with FastAPI Backend, WebSocket/Polling, and Callback Simulator
 */

const API_BASE = '/api';

// Global State
const state = {
  products: [],
  researchRuns: [],
  leads: [],
  segments: [],
  health: null,
  activeFilter: {
    minScore: 0.0,
    source: '',
    segment: '',
  },
};

// ── DOM Helpers ───────────────────────────────────────────────────
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ── Toast Notification System ─────────────────────────────────────
function showToast(message, type = 'info') {
  const container = $('#toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button style="background:none;border:none;color:inherit;cursor:pointer;opacity:0.6">&times;</button>
  `;
  toast.querySelector('button').onclick = () => toast.remove();
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ── API Fetch Client ──────────────────────────────────────────────
async function api(path, options = {}) {
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: { ...defaultHeaders, ...options.headers },
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP error ${res.status}`);
    }
    if (res.status === 204) return null;
    return await res.json();
  } catch (error) {
    console.error(`API Error on ${path}:`, error);
    throw error;
  }
}

// ── System Health & Stats ─────────────────────────────────────────
async function fetchHealth() {
  try {
    const data = await api('/health');
    state.health = data;
    const badge = $('#system-status-badge');
    const dot = badge.querySelector('.status-dot');
    const text = badge.querySelector('.status-text');

    if (data.status === 'healthy') {
      dot.className = 'status-dot healthy';
      text.textContent = 'Backend Healthy';
    } else {
      dot.className = 'status-dot degraded';
      text.textContent = 'Degraded';
    }
  } catch (e) {
    const badge = $('#system-status-badge');
    badge.querySelector('.status-dot').className = 'status-dot error';
    badge.querySelector('.status-text').textContent = 'Disconnected';
  }
}

async function fetchOpenClawStatus() {
  try {
    const data = await api('/openclaw/status');
    const badge = $('#openclaw-status-badge');
    if (!badge) return;
    const dot = badge.querySelector('.status-dot');
    const text = badge.querySelector('.status-text');

    if (data.installed) {
      dot.className = 'status-dot healthy';
      dot.style.background = '#06b6d4';
      dot.style.boxShadow = '0 0 10px #06b6d4';
      text.textContent = data.version && data.version.includes('OpenClaw') ? data.version.split('\n')[0] : 'OpenClaw Ready';
    } else {
      dot.className = 'status-dot error';
      text.textContent = 'OpenClaw Offline';
    }
  } catch (e) {
    const badge = $('#openclaw-status-badge');
    if (badge) {
      badge.querySelector('.status-dot').className = 'status-dot error';
      badge.querySelector('.status-text').textContent = 'OpenClaw Offline';
    }
  }
}

function updateHeroStats() {
  $('#stat-products-count').textContent = state.products.length;
  $('#stat-research-count').textContent = state.researchRuns.length;
  $('#stat-leads-count').textContent = state.leads.length;
  $('#stat-segments-count').textContent = state.segments.length;

  const activeRuns = state.researchRuns.filter((r) => r.status === 'running' || r.status === 'queued');
  $('#stat-research-queued').textContent = `${activeRuns.length} active`;

  if (state.leads.length > 0) {
    const validScores = state.leads.map((l) => l.overall_score).filter((s) => typeof s === 'number');
    if (validScores.length > 0) {
      const avg = validScores.reduce((a, b) => a + b, 0) / validScores.length;
      $('#stat-avg-score').textContent = `${Math.round(avg * 100)}%`;
    }
  } else {
    $('#stat-avg-score').textContent = '—';
  }
}

// ── Data Fetching ─────────────────────────────────────────────────
async function fetchAllData() {
  try {
    const [products, runs, leads, segments] = await Promise.all([
      api('/products/'),
      api('/research/'),
      api('/leads/'),
      api('/segments/'),
    ]);

    state.products = products;
    state.researchRuns = runs;
    state.leads = leads;
    state.segments = segments;

    updateHeroStats();
    renderProducts();
    renderResearchRuns();
    renderLeads();
    renderSegments();
    populateSelectDropdowns();
  } catch (err) {
    showToast(`Failed to load data: ${err.message}`, 'error');
  }
}

// ── Dropdowns Populator ───────────────────────────────────────────
function populateSelectDropdowns() {
  // Product selects
  const researchProdFilter = $('#select-research-product-filter');
  const triggerResearchProd = $('#tr-product-id');
  const curFilter = researchProdFilter.value;

  const prodOpts = state.products.map((p) => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('');
  researchProdFilter.innerHTML = `<option value="">All Products</option>${prodOpts}`;
  researchProdFilter.value = curFilter;
  triggerResearchProd.innerHTML = prodOpts || '<option value="">No products yet</option>';

  // Research Run selects
  const runOpts = state.researchRuns
    .map((r) => {
      const p = state.products.find((prod) => prod.id === r.product_id);
      const prodName = p ? p.name : `Product #${r.product_id}`;
      return `<option value="${r.id}">Run #${r.id} (${escapeHtml(prodName)} - ${r.status})</option>`;
    })
    .join('');

  $('#l-run-id').innerHTML = runOpts || '<option value="">Create a research run first</option>';
  $('#seg-run-id').innerHTML = runOpts || '<option value="">Create a research run first</option>';
  $('#cb-run-id').innerHTML = runOpts || '<option value="">No research runs available</option>';
}

// ── Render: Products ──────────────────────────────────────────────
function renderProducts() {
  const container = $('#products-list');
  if (state.products.length === 0) {
    container.innerHTML = `
      <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
        <h3 style="margin-bottom: 8px;">No Products Found</h3>
        <p class="text-muted" style="margin-bottom: 20px;">Add your first startup idea or click "Quick Seed Data" to populate a sample workspace.</p>
        <div>
          <button class="btn btn-primary" onclick="openModal('#modal-product')">+ Add First Product</button>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = state.products
    .map((p) => {
      const runsCount = state.researchRuns.filter((r) => r.product_id === p.id).length;
      return `
      <div class="card" data-product-id="${p.id}">
        <div class="card-header">
          <div>
            <h3 class="card-title">${escapeHtml(p.name)}</h3>
            <div class="card-subtitle">Created ${formatDate(p.created_at)}</div>
          </div>
          <span class="badge badge-accent">${runsCount} runs</span>
        </div>
        <div class="card-body">
          <p style="margin-bottom: 8px;">${escapeHtml(p.description || 'No description provided.')}</p>
          ${p.target_users ? `<p style="font-size: 0.8rem; color: var(--text-muted);"><strong>Target:</strong> ${escapeHtml(p.target_users)}</p>` : ''}
          ${p.problem ? `<p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;"><strong>Problem:</strong> ${escapeHtml(p.problem)}</p>` : ''}
        </div>
        <div class="card-footer">
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button class="btn btn-primary btn-sm" onclick="triggerRunForProduct(${p.id})">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              Discovery
            </button>
            <button class="btn btn-secondary btn-sm" style="border-color:#06b6d4; color:#38bdf8;" onclick="triggerOpenClawForProduct(${p.id})" title="Launch autonomous discovery with OpenClaw">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="12 8 8 12 12 16 16 12 12 8"></polygon></svg>
              OpenClaw Agent
            </button>
          </div>
          <button class="btn btn-ghost btn-sm text-danger" onclick="deleteProduct(${p.id})">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
          </button>
        </div>
      </div>
    `;
    })
    .join('');
}

// ── Render: Research Runs ─────────────────────────────────────────
function renderResearchRuns() {
  const tbody = $('#research-tbody');
  const filterProdId = $('#select-research-product-filter').value;

  let runs = state.researchRuns;
  if (filterProdId) {
    runs = runs.filter((r) => r.product_id === parseInt(filterProdId, 10));
  }

  if (runs.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" style="text-align: center; padding: 32px; color: var(--text-muted);">
          No research pipelines found. Launch a run from the Products tab.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = runs
    .map((r) => {
      const product = state.products.find((p) => p.id === r.product_id);
      const prodName = product ? product.name : `Product #${r.product_id}`;
      const statusBadge = getStatusBadge(r.status);
      const progressPct = r.progress != null ? Math.round(r.progress * 100) : r.status === 'completed' ? 100 : 15;

      return `
      <tr>
        <td><strong>#${r.id}</strong></td>
        <td><strong>${escapeHtml(prodName)}</strong></td>
        <td>${statusBadge}</td>
        <td>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: ${progressPct}%"></div>
          </div>
          <span style="font-size:0.75rem; font-family:var(--font-mono);">${progressPct}%</span>
        </td>
        <td><span class="font-mono">${r.sources_analyzed || 0}</span> sources</td>
        <td><span class="font-mono">${r.leads_found || 0}</span> leads</td>
        <td style="font-size:0.8rem; color:var(--text-muted);">${formatDate(r.created_at)}</td>
        <td>
          <div style="display:flex; gap:6px;">
            ${
              r.status !== 'completed'
                ? `<button class="btn btn-secondary btn-sm" onclick="openCallbackWithRun(${r.id})" title="Simulate n8n callback">Webhook</button>`
                : `<button class="btn btn-ghost btn-sm" onclick="viewReport(${r.id})" title="View Executive Summary">Report</button>`
            }
          </div>
        </td>
      </tr>
    `;
    })
    .join('');
}

// ── Render: Leads ─────────────────────────────────────────────────
function renderLeads() {
  const container = $('#leads-list');
  let leads = [...state.leads];

  // Apply filters
  if (state.activeFilter.minScore > 0) {
    leads = leads.filter((l) => (l.overall_score || 0) >= state.activeFilter.minScore);
  }
  if (state.activeFilter.source) {
    leads = leads.filter((l) => (l.source || '').toLowerCase() === state.activeFilter.source.toLowerCase());
  }
  if (state.activeFilter.segment) {
    const q = state.activeFilter.segment.toLowerCase();
    leads = leads.filter((l) => (l.customer_segment || '').toLowerCase().includes(q));
  }

  if (leads.length === 0) {
    container.innerHTML = `
      <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
        <h3 style="margin-bottom: 8px;">No Leads Matching Filters</h3>
        <p class="text-muted">Adjust your filter sliders or add a lead manually.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = leads
    .map((lead) => {
      const score = lead.overall_score != null ? Math.round(lead.overall_score * 100) : 0;
      const scoreClass = score >= 80 ? 'high' : score >= 50 ? 'mid' : 'low';

      return `
      <div class="card lead-card" data-lead-id="${lead.id}">
        <div class="card-header">
          <div>
            <div class="card-title">${escapeHtml(lead.author || 'Anonymous Prospect')}</div>
            <div class="card-subtitle">
              <span class="badge badge-info">${escapeHtml(lead.source || 'web')}</span>
              ${lead.customer_segment ? `<span class="badge badge-accent" style="margin-left:4px;">${escapeHtml(lead.customer_segment)}</span>` : ''}
            </div>
          </div>
          <div class="lead-score-badge">
            <span class="lead-score-val ${scoreClass}">${score}%</span>
            <span style="font-size:0.68rem; text-transform:uppercase; color:var(--text-muted);">Match Score</span>
          </div>
        </div>

        <div class="card-body">
          <p style="font-size:0.85rem; margin-bottom: 10px;">${escapeHtml(lead.problem_detected || 'Problem not specified')}</p>

          <!-- Deterministic Scoring Breakdown -->
          <div class="signals-breakdown">
            <div class="signal-item">
              <span>Problem Fit (35%)</span>
              <span>${fmtPct(lead.problem_fit)}</span>
            </div>
            <div class="signal-item">
              <span>Intent (30%)</span>
              <span>${fmtPct(lead.intent_level)}</span>
            </div>
            <div class="signal-item">
              <span>Persona (20%)</span>
              <span>${fmtPct(lead.persona_fit)}</span>
            </div>
            <div class="signal-item">
              <span>Evidence (15%)</span>
              <span>${fmtPct(lead.evidence_strength)}</span>
            </div>
          </div>

          ${
            lead.outreach_angle
              ? `<div class="outreach-box">
                  <strong>Angle:</strong> ${escapeHtml(lead.outreach_angle)}
                </div>`
              : ''
          }

          ${
            lead.source_url
              ? `<div style="margin-top:10px;">
                  <a href="${escapeHtml(lead.source_url)}" target="_blank" class="btn-ghost" style="font-size:0.75rem; text-decoration:underline;">
                    View Source Thread &rarr;
                  </a>
                </div>`
              : ''
          }
        </div>

        <div class="card-footer">
          <button class="btn btn-secondary btn-sm" onclick="openAddEvidenceModal(${lead.id})">
            + Attach Quote
          </button>
          <button class="btn btn-ghost btn-sm" onclick="viewLeadDetail(${lead.id})">
            View Evidence &rarr;
          </button>
        </div>
      </div>
    `;
    })
    .join('');
}

// ── Render: Segments ──────────────────────────────────────────────
function renderSegments() {
  const container = $('#segments-list');
  if (state.segments.length === 0) {
    container.innerHTML = `
      <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
        <h3 style="margin-bottom: 8px;">No Customer Segments Yet</h3>
        <p class="text-muted">Segments are synthesized by OpenClaw or can be created manually.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = state.segments
    .map((seg) => {
      const priorityBadge =
        seg.priority_level === 'high'
          ? '<span class="badge badge-danger">High Priority</span>'
          : seg.priority_level === 'medium'
          ? '<span class="badge badge-warning">Medium Priority</span>'
          : '<span class="badge badge-accent">Low Priority</span>';

      return `
      <div class="card">
        <div class="card-header">
          <div>
            <h3 class="card-title">${escapeHtml(seg.name)}</h3>
            <div class="card-subtitle">Run #${seg.research_run_id}</div>
          </div>
          ${priorityBadge}
        </div>
        <div class="card-body">
          <p style="margin-bottom: 12px;">${escapeHtml(seg.description || 'No description.')}</p>
          ${seg.estimated_size ? `<p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:4px;"><strong>Est. Market Pool:</strong> ~${seg.estimated_size.toLocaleString()} prospects</p>` : ''}
          ${
            seg.market_language
              ? `<div class="outreach-box" style="margin-top:8px;">
                  <strong>Customer Language:</strong> "${escapeHtml(seg.market_language)}"
                </div>`
              : ''
          }
        </div>
        <div class="card-footer">
          <span style="font-size:0.75rem; color:var(--text-muted);">Added ${formatDate(seg.created_at)}</span>
        </div>
      </div>
    `;
    })
    .join('');
}

// ── Lead Detail / Evidence Viewer ─────────────────────────────────
async function viewLeadDetail(leadId) {
  try {
    const lead = await api(`/leads/${leadId}`);
    const modal = $('#modal-report');
    $('#report-title').textContent = `Evidence Quotes: ${lead.author || 'Lead #' + lead.id}`;

    const evidenceList =
      lead.evidence && lead.evidence.length > 0
        ? lead.evidence
            .map(
              (ev) => `
          <div style="background:var(--bg-surface-elevated); padding:14px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); margin-bottom:10px;">
            <p style="font-style:italic; margin-bottom:8px;">"${escapeHtml(ev.content)}"</p>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted);">
              <span>Type: <strong>${escapeHtml(ev.signal_type || 'signal')}</strong></span>
              <span>Strength: <strong>${ev.strength != null ? Math.round(ev.strength * 100) + '%' : '—'}</strong></span>
              ${ev.source_url ? `<a href="${escapeHtml(ev.source_url)}" target="_blank" style="color:var(--accent-cyan)">Source</a>` : ''}
            </div>
          </div>
        `
            )
            .join('')
        : '<p class="text-muted">No evidence quotes attached to this lead yet. Click "+ Attach Quote" to add one.</p>';

    $('#report-body').innerHTML = `
      <div style="margin-bottom:16px;">
        <h4 style="margin-bottom:4px;">Problem Detected:</h4>
        <p>${escapeHtml(lead.problem_detected || 'None recorded')}</p>
      </div>
      <div>
        <h4 style="margin-bottom:8px;">Verified Quotes:</h4>
        ${evidenceList}
      </div>
    `;
    openModal('#modal-report');
  } catch (err) {
    showToast(`Could not load lead detail: ${err.message}`, 'error');
  }
}

// ── Research Run Report View ──────────────────────────────────────
async function viewReport(runId) {
  try {
    const run = await api(`/research/${runId}`);
    $('#report-title').textContent = `Executive Discovery Report — Run #${runId}`;
    const report = run.report;

    if (!report) {
      $('#report-body').innerHTML = `
        <div class="alert alert-info">
          No structured report generated for this run yet. Run stats: ${run.sources_analyzed || 0} sources analyzed, ${run.leads_found || 0} leads discovered.
        </div>
      `;
    } else {
      $('#report-body').innerHTML = `
        <div style="margin-bottom:20px;">
          <h4 style="margin-bottom:6px; color:var(--accent-cyan);">Executive Summary</h4>
          <p style="line-height:1.6;">${escapeHtml(report.summary || 'Summary not available')}</p>
        </div>
        ${
          report.key_findings && report.key_findings.length > 0
            ? `<div style="margin-bottom:20px;">
                <h4 style="margin-bottom:6px;">Key Findings</h4>
                <ul style="padding-left:20px; color:var(--text-secondary); line-height:1.6;">
                  ${report.key_findings.map((f) => `<li>${escapeHtml(f)}</li>`).join('')}
                </ul>
              </div>`
            : ''
        }
        ${
          report.recommended_actions && report.recommended_actions.length > 0
            ? `<div>
                <h4 style="margin-bottom:6px;">Recommended Actions</h4>
                <ul style="padding-left:20px; color:var(--text-secondary); line-height:1.6;">
                  ${report.recommended_actions.map((a) => `<li>${escapeHtml(a)}</li>`).join('')}
                </ul>
              </div>`
            : ''
        }
      `;
    }
    openModal('#modal-report');
  } catch (err) {
    showToast(`Failed to load report: ${err.message}`, 'error');
  }
}

// ── Trigger Actions ───────────────────────────────────────────────
async function triggerRunForProduct(productId) {
  try {
    const res = await api('/research/', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    });
    showToast(`Research run #${res.id} queued successfully!`, 'success');
    await fetchAllData();
    switchTab('research');
  } catch (err) {
    showToast(`Failed to trigger research: ${err.message}`, 'error');
  }
}

async function triggerOpenClawForProduct(productId) {
  try {
    showToast('Dispatching OpenClaw autonomous discovery agent...', 'info');
    const res = await api('/openclaw/run', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    });
    showToast('OpenClaw completed discovery! Ingested leads & segments.', 'success');
    await fetchAllData();
    switchTab('leads');
  } catch (err) {
    showToast(`OpenClaw error: ${err.message}`, 'error');
  }
}

async function deleteProduct(productId) {
  if (!confirm('Are you sure you want to delete this product? All associated runs and leads will also be removed.')) return;
  try {
    await api(`/products/${productId}`, { method: 'DELETE' });
    showToast('Product deleted.', 'info');
    await fetchAllData();
  } catch (err) {
    showToast(`Failed to delete product: ${err.message}`, 'error');
  }
}

// ── Seed Demo Data ────────────────────────────────────────────────
async function seedDemoData() {
  const btn = $('#btn-demo-seed');
  btn.disabled = true;
  btn.textContent = 'Seeding...';

  try {
    // 1. Create Product
    const product = await api('/products/', {
      method: 'POST',
      body: JSON.stringify({
        name: 'EchoLaunch AI',
        description: 'Autonomous customer discovery agent that listens to Reddit, GitHub, and Discord discussions to find early adopters before coding.',
        target_users: 'B2B SaaS Founders & Product Engineers',
        problem: 'Spending 6 months building an MVP only to launch to total silence and zero user interest.',
      }),
    });

    // 2. Trigger Research Run
    const run = await api('/research/', {
      method: 'POST',
      body: JSON.stringify({ product_id: product.id }),
    });

    // 3. Complete Callback Simulation (idempotent with event_id)
    const eventId = `seed-demo-${Date.now()}`;
    await api('/research/callback', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer test-callback-secret',
      },
      body: JSON.stringify({
        research_run_id: run.id,
        event_id: eventId,
        status: 'completed',
        progress: 1.0,
        sources_analyzed: 48,
        leads_found: 3,
        leads: [
          {
            author: 'u/saas_builder_99',
            source: 'reddit',
            source_url: 'https://reddit.com/r/startups/comments/mock1',
            customer_segment: 'Solo Technical Founders',
            problem_detected: 'Desperately need someone to tell me if this developer analytics tool is worth building before I quit my job.',
            problem_fit: 0.95,
            intent_level: 0.90,
            persona_fit: 0.85,
            evidence_strength: 0.90,
            reason: 'Explicitly looking for pre-launch validation and asking for user feedback.',
            outreach_angle: 'Offer early access to AI competitor research and pain-point analysis.',
          },
          {
            author: 'mabor_dev',
            source: 'github',
            source_url: 'https://github.com/topics/startup-tools/issues/42',
            customer_segment: 'Open Source Maintainers',
            problem_detected: 'Hard to know which features users actually will pay for vs just demand in issues.',
            problem_fit: 0.80,
            intent_level: 0.70,
            persona_fit: 0.85,
            evidence_strength: 0.75,
            reason: 'High activity on monetization discussions.',
            outreach_angle: 'Share insights on feature monetization validation.',
          },
          {
            author: 'clara_tech',
            source: 'hackernews',
            source_url: 'https://news.ycombinator.com/item?id=883921',
            customer_segment: 'Agency Founders',
            problem_detected: 'Client wants us to validate product-market fit before investing $50k in custom app development.',
            problem_fit: 0.90,
            intent_level: 0.85,
            persona_fit: 0.80,
            evidence_strength: 0.85,
            reason: 'High budget authority seeking customer validation automation.',
            outreach_angle: 'Offer white-label customer discovery reports for their client deliverables.',
          },
        ],
        segments: [
          {
            name: 'Solo Technical Founders',
            description: 'Engineers building SaaS products on evenings and weekends with strong technical skills but zero distribution.',
            estimated_size: 12000,
            priority_level: 'high',
            market_language: 'idea validation, building in public, first 10 paying customers',
          },
          {
            name: 'Digital Agency Innovators',
            description: 'Boutique software agencies tasked by clients to perform feasibility and market research.',
            estimated_size: 4500,
            priority_level: 'medium',
            market_language: 'client validation, proof of concept, discovery phase',
          },
        ],
        report: {
          summary: 'High demand detected across Reddit (r/startups, r/SaaS) and HackerNews for automated pre-launch customer discovery. The primary friction is fear of wasting engineering effort on unvalidated propositions.',
          key_findings: [
            'Founders spend an average of 4.2 months building before talking to potential users.',
            '82% of surveyed complaints mention lack of distribution channels as primary failure mode.',
            'Target audience is actively hanging out in r/startups and Ask HN searching for validation techniques.',
          ],
          recommended_actions: [
            'Focus positioning on "Find early adopters before you write a single line of code".',
            'Provide 1-click Reddit/HN thread sentiment exports.',
            'Reach out to the 3 identified high-intent prospects with complimentary validation teardowns.',
          ],
        },
      }),
    });

    showToast('Demo data seeded successfully!', 'success');
    await fetchAllData();
  } catch (err) {
    showToast(`Seeding error: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
      Quick Seed Data
    `;
  }
}

// ── Modals Management ─────────────────────────────────────────────
function openModal(sel) {
  const m = $(sel);
  if (m) m.classList.add('active');
}

function closeModal(sel) {
  const m = typeof sel === 'string' ? $(sel) : sel.closest('.modal-overlay');
  if (m) m.classList.remove('active');
}

function openAddEvidenceModal(leadId) {
  $('#ev-lead-id').value = leadId;
  $('#form-add-evidence').reset();
  $('#ev-lead-id').value = leadId;
  openModal('#modal-evidence');
}

function openCallbackWithRun(runId) {
  switchTab('callback');
  $('#cb-run-id').value = runId;
  $('#cb-event-id').value = `evt-${Date.now()}`;
  loadSampleCallbackPayload(runId);
}

function loadSampleCallbackPayload(runId) {
  const rId = runId || $('#cb-run-id').value || 1;
  const sample = {
    research_run_id: parseInt(rId, 10),
    event_id: `evt-${Date.now()}`,
    status: 'completed',
    progress: 1.0,
    sources_analyzed: 35,
    leads_found: 2,
    leads: [
      {
        author: 'u/founder_demo',
        source: 'reddit',
        source_url: 'https://reddit.com/r/startups',
        customer_segment: 'Solo Founders',
        problem_detected: 'Tired of building tools that no one purchases',
        problem_fit: 0.9,
        intent_level: 0.85,
        persona_fit: 0.8,
        evidence_strength: 0.9,
        outreach_angle: 'Share automated customer interview script',
      },
    ],
    segments: [
      {
        name: 'Bootstrapped Founders',
        description: 'Solo SaaS builders needing fast validation',
        estimated_size: 8000,
        priority_level: 'high',
        market_language: 'market validation, early adopters',
      },
    ],
    report: {
      summary: 'Verified strong willingness to pay for pre-launch audience targeting.',
      key_findings: ['Founders prefer actionable lead links over abstract market reports.'],
      recommended_actions: ['Initiate direct outreach with cold DM framework.'],
    },
  };
  $('#cb-payload').value = JSON.stringify(sample, null, 2);
}

// ── Tabs Navigation ──────────────────────────────────────────────
function switchTab(tabId) {
  $$('.nav-tab').forEach((t) => t.classList.remove('active'));
  $$('.tab-panel').forEach((p) => p.classList.remove('active'));

  const btn = $(`[data-tab="${tabId}"]`);
  const panel = $(`#tab-${tabId}`);
  if (btn) btn.classList.add('active');
  if (panel) panel.classList.add('active');
}

// ── Formatters ────────────────────────────────────────────────────
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatDate(isoStr) {
  if (!isoStr) return '—';
  try {
    const d = new Date(isoStr);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch (e) {
    return isoStr;
  }
}

function fmtPct(val) {
  return val != null ? `${Math.round(val * 100)}%` : '—';
}

function getStatusBadge(status) {
  switch (status) {
    case 'completed':
      return '<span class="badge badge-success">Completed</span>';
    case 'running':
      return '<span class="badge badge-info">Running</span>';
    case 'failed':
      return '<span class="badge badge-danger">Failed</span>';
    case 'queued':
    default:
      return '<span class="badge badge-warning">Queued</span>';
  }
}

// ── Event Listeners Setup ─────────────────────────────────────────
function setupEventListeners() {
  // Tab click
  $$('.nav-tab').forEach((tab) => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  // Modal open buttons
  $('#btn-open-create-product').addEventListener('click', () => openModal('#modal-product'));
  $('#btn-open-trigger-research').addEventListener('click', () => openModal('#modal-trigger-research'));
  $('#btn-open-create-lead').addEventListener('click', () => openModal('#modal-lead'));
  $('#btn-open-create-segment').addEventListener('click', () => openModal('#modal-segment'));

  // Close modals
  $$('[data-close-modal]').forEach((btn) => {
    btn.addEventListener('click', (e) => closeModal(e.target));
  });
  $$('.modal-overlay').forEach((overlay) => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal(overlay);
    });
  });

  // Theme toggle
  $('#theme-toggle-btn').addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('launchlens-theme', next);
  });

  // Quick Seed Data
  $('#btn-demo-seed').addEventListener('click', seedDemoData);
  $('#btn-refresh-all').addEventListener('click', () => {
    fetchAllData();
    fetchHealth();
    fetchOpenClawStatus();
    showToast('Refreshed data from backend.', 'info');
  });

  // Product Filter on Research Runs Tab
  $('#select-research-product-filter').addEventListener('change', renderResearchRuns);

  // Filters on Leads Tab
  $('#filter-min-score').addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    $('#label-score-val').textContent = val.toFixed(2);
    state.activeFilter.minScore = val;
    renderLeads();
  });
  $('#filter-source').addEventListener('change', (e) => {
    state.activeFilter.source = e.target.value;
    renderLeads();
  });
  $('#filter-segment').addEventListener('input', (e) => {
    state.activeFilter.segment = e.target.value;
    renderLeads();
  });
  $('#btn-reset-filters').addEventListener('click', () => {
    $('#filter-min-score').value = 0.0;
    $('#label-score-val').textContent = '0.0';
    $('#filter-source').value = '';
    $('#filter-segment').value = '';
    state.activeFilter = { minScore: 0.0, source: '', segment: '' };
    renderLeads();
  });

  // FORM: Create Product
  $('#form-create-product').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      await api('/products/', {
        method: 'POST',
        body: JSON.stringify({
          name: $('#p-name').value,
          description: $('#p-desc').value || null,
          target_users: $('#p-target').value || null,
          problem: $('#p-problem').value || null,
        }),
      });
      showToast('Product created successfully!', 'success');
      closeModal('#modal-product');
      e.target.reset();
      await fetchAllData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // FORM: Trigger Research
  $('#form-trigger-research').addEventListener('submit', async (e) => {
    e.preventDefault();
    const productId = parseInt($('#tr-product-id').value, 10);
    try {
      const res = await api('/research/', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId }),
      });
      showToast(`Research run #${res.id} queued!`, 'success');
      closeModal('#modal-trigger-research');
      await fetchAllData();
      switchTab('research');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // FORM: Create Lead Manually
  $('#form-create-lead').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      await api('/leads/', {
        method: 'POST',
        body: JSON.stringify({
          research_run_id: parseInt($('#l-run-id').value, 10),
          author: $('#l-author').value || null,
          source: $('#l-source').value || null,
          source_url: $('#l-source-url').value || null,
          customer_segment: $('#l-segment').value || null,
          problem_detected: $('#l-problem').value || null,
          problem_fit: parseFloat($('#l-fit').value),
          intent_level: parseFloat($('#l-intent').value),
          persona_fit: parseFloat($('#l-persona').value),
          evidence_strength: parseFloat($('#l-strength').value),
          outreach_angle: $('#l-angle').value || null,
        }),
      });
      showToast('Lead added with calculated score!', 'success');
      closeModal('#modal-lead');
      e.target.reset();
      await fetchAllData();
      switchTab('leads');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // FORM: Add Evidence
  $('#form-add-evidence').addEventListener('submit', async (e) => {
    e.preventDefault();
    const leadId = parseInt($('#ev-lead-id').value, 10);
    try {
      await api(`/leads/${leadId}/evidence`, {
        method: 'POST',
        body: JSON.stringify({
          content: $('#ev-content').value,
          signal_type: $('#ev-signal').value || null,
          strength: parseFloat($('#ev-strength').value) || null,
          source_url: $('#ev-url').value || null,
        }),
      });
      showToast('Evidence quote attached!', 'success');
      closeModal('#modal-evidence');
      e.target.reset();
      await fetchAllData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // FORM: Create Segment
  $('#form-create-segment').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      await api('/segments/', {
        method: 'POST',
        body: JSON.stringify({
          research_run_id: parseInt($('#seg-run-id').value, 10),
          name: $('#seg-name').value,
          description: $('#seg-desc').value || null,
          estimated_size: $('#seg-size').value ? parseInt($('#seg-size').value, 10) : null,
          priority_level: $('#seg-priority').value,
          market_language: $('#seg-lang').value || null,
        }),
      });
      showToast('Customer segment created!', 'success');
      closeModal('#modal-segment');
      e.target.reset();
      await fetchAllData();
      switchTab('segments');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Callback Simulator Buttons & Form
  $('#btn-load-sample-callback').addEventListener('click', () => loadSampleCallbackPayload());
  $('#form-simulate-callback').addEventListener('submit', async (e) => {
    e.preventDefault();
    let payload;
    try {
      payload = JSON.parse($('#cb-payload').value);
    } catch (err) {
      showToast('Invalid JSON in payload textarea', 'error');
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/research/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer test-callback-secret',
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      $('#callback-response-preview').classList.remove('hidden');
      $('#callback-response-json').textContent = JSON.stringify(data, null, 2);

      if (res.ok) {
        showToast('Callback processed successfully!', 'success');
        await fetchAllData();
      } else {
        showToast(`Callback error: ${data.detail || res.statusText}`, 'error');
      }
    } catch (err) {
      showToast(`Network error: ${err.message}`, 'error');
    }
  });
}

// ── Periodic Auto-poll ────────────────────────────────────────────
function startPolling() {
  setInterval(() => {
    // Only poll if there are active runs or every 10 seconds
    const hasActive = state.researchRuns.some((r) => r.status === 'running' || r.status === 'queued');
    if (hasActive) {
      fetchAllData();
    }
  }, 4000);
}

// ── Application Init ──────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  fetchHealth();
  fetchOpenClawStatus();
  fetchAllData();
  startPolling();
});
