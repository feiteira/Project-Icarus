const fs = require('fs');
const path = require('path');

// Load all data
const summaries = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/video_summaries.json', 'utf8'));
const topicMap = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/topic_map.json', 'utf8'));
const categoryMap = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/category_map.json', 'utf8'));
const predictions = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/predictions.json', 'utf8'));
const lopVideos = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/lop_videos.json', 'utf8'));
const eschVideos = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/eschatology_videos.json', 'utf8'));

const ROOT = '/home/feiteira/.openclaw/workspace';

// Topic definitions (from earlier)
const TOPIC_DEFINITIONS = {
  'United States': {description: 'US geopolitics, domestic politics, foreign policy', color: '#3498db'},
  'Iran': {description: 'Iranian strategy, nuclear program, regional influence, sanctions', color: '#2ecc71'},
  'Saudi Arabia': {description: 'Saudi-Iran rivalry, OPEC, oil strategy, Yemen, Gulf security', color: '#e67e22'},
  'Israel': {description: 'Israeli strategy, Middle East policy, US-Israel alliance', color: '#9b59b6'},
  'China': {description: 'Chinese rise, Taiwan, South China Sea, trade, Belt and Road', color: '#e74c3c'},
  'Russia': {description: 'Russian strategy, Ukraine war, Putin, Soviet legacy', color: '#1abc9c'},
  'Ukraine': {description: 'Ukraine conflict, NATO, Western aid, proxy war', color: '#34495e'},
  'Empire': {description: 'Imperial decline theory, American empire, historical parallels', color: '#800000'},
  'Civilization': {description: 'Civilizational decline, cycles, cultural rot', color: '#8b4513'},
  'Collapse': {description: 'Civilizational collapse patterns, historical examples', color: '#c0392b'},
  'War': {description: 'War theory, proxy wars, military strategy', color: '#dc143c'},
  'Strategy': {description: 'Strategic theory, game theory applications', color: '#006400'},
  'Nuclear': {description: 'Nuclear weapons, deterrence, proliferation', color: '#8b0000'},
  'Game Theory': {description: 'Game theory in geopolitics, strategic interaction analysis', color: '#4b0082'},
  'Geopolitics': {description: 'Global power dynamics, regional strategy', color: '#4682b4'},
  'Democracy': {description: 'Democratic systems, elections, populism', color: '#4169e1'},
  'Cold War': {description: 'Cold War dynamics, superpower rivalry parallels', color: '#708090'},
  'Middle East': {description: 'Middle Eastern politics, conflicts, regional order', color: '#a0522d'},
  'Bitcoin': {description: 'Bitcoin as monetary phenomenon, store of value', color: '#ff8c00'},
  'Gold': {description: 'Gold as currency reserve, monetary history', color: '#daa520'},
  'Civil War': {description: 'American civil war risk, secession, domestic conflict', color: '#b22222'},
  'Constitution': {description: 'US constitutional crisis, federalism, rights', color: '#00008b'},
  'Federal Reserve': {description: 'Fed monetary policy, dollar dominance', color: '#006400'},
  'World Economic Forum': {description: 'WEF, globalist elite, Great Reset', color: '#800080'},
  'Trump': {description: 'Trump politics, impact on US and world', color: '#ff0000'},
  'Christianity': {description: 'Christian history, theology, cultural influence', color: '#8b0000'},
  'Islam': {description: 'Islamic history, theology, political Islam', color: '#006400'},
  'Judaism': {description: 'Jewish history, Zionism, Israeli politics', color: '#000080'},
  'Roman Empire': {description: 'Roman imperial decline parallels', color: '#8b0000'},
  'Holy Roman Empire': {description: 'Holy Roman Empire history, European imperial structure', color: '#800000'},
  'Europe': {description: 'European politics, EU, NATO, Russia relations', color: '#4682b4'},
  'NATO': {description: 'NATO expansion, Article 5, European security', color: '#00008b'},
  'India': {description: 'Indian strategy, China rivalry, regional role', color: '#ff8c00'},
  'Japan': {description: 'Japanese strategy, economic decline, security', color: '#dc143c'},
  'Taiwan': {description: 'Taiwan strait, Chinese reunification, semiconductor', color: '#008080'},
  'South China Sea': {description: 'SCS disputes, Chinese expansion, maritime', color: '#000080'},
  'Silk Road': {description: 'Belt and Road Initiative, Chinese global strategy', color: '#ff0000'},
  'BRICS': {description: 'BRICS expansion, dedollarization, multipolar world', color: '#daa520'},
  'Woke': {description: 'Woke culture, cultural Marxism, identity politics', color: '#800080'},
  'NeoCon': {description: 'Neoconservative ideology, US interventionism', color: '#8b0000'},
  'Secession': {description: 'State secession, Texas, national divorce', color: '#b22222'},
};

// Category definitions
const CATEGORY_DEFINITIONS = {
  military: {description: 'Military conflict, wars, armed forces, defense strategy', color: '#c0392b'},
  history: {description: 'Historical events, empires, civilizations throughout history', color: '#8b4513'},
  economy: {description: 'Economic systems, monetary policy, trade, resources', color: '#27ae60'},
  culture: {description: 'Cultural trends, societal values, religion, ideology', color: '#9b59b6'},
  politics: {description: 'Political systems, elections, governance, political theory', color: '#2980b9'},
  technology: {description: 'Tech developments, AI, semiconductors, infrastructure', color: '#16a085'},
  geopolitics: {description: 'Geopolitical strategy, great power competition', color: '#2c3e50'},
  intelligence: {description: 'Intelligence agencies, espionage, covert operations', color: '#7f8c8d'},
  protests: {description: 'Social movements, revolutions, civil unrest', color: '#d35400'},
  health: {description: 'Public health, pandemics, medical systems', color: '#1abc9c'},
  refugees: {description: 'Migration, refugee crises, population displacement', color: '#e67e22'},
  climate: {description: 'Climate change, environmental factors, resource scarcity', color: '#3498db'},
};

function slugify(text) {
  return text.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
}

function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m ${s}s`;
}

function formatDate(dateStr) {
  if (!dateStr || dateStr.length !== 8) return dateStr;
  return `${dateStr.slice(0,4)}-${dateStr.slice(4,6)}-${dateStr.slice(6,8)}`;
}

function formatTimestamp(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
  return `${m}:${s.toString().padStart(2,'0')}`;
}

function topicBadge(topic) {
  const def = TOPIC_DEFINITIONS[topic];
  const color = def ? def.color : '#666';
  return `<a href="topics/${slugify(topic)}.html" class="topic-badge" style="background:${color}">${topic}</a>`;
}

function categoryBadge(cat) {
  const def = CATEGORY_DEFINITIONS[cat];
  const color = def ? def.color : '#666';
  const desc = def ? def.description : '';
  return `<span class="topic-badge" style="background:${color}" title="${desc}">${cat}</span>`;
}

// Reuse CSS from earlier
const CSS = `
:root {
  --primary: #2c3e50;
  --accent: #3498db;
  --bg: #fafafa;
  --card-bg: #ffffff;
  --border: #e0e0e0;
  --text: #333;
  --muted: #777;
  --sidebar-width: 260px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.header { background: var(--primary); color: white; padding: 1rem 2rem; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 1.4rem; font-weight: 600; }
.header h1 a { color: white; }
.search-bar { margin-top: 0.5rem; }
.search-bar input { width: 100%; padding: 0.5rem; border: none; border-radius: 4px; font-size: 0.95rem; }
.layout { display: flex; max-width: 1400px; margin: 0 auto; }
.sidebar { width: var(--sidebar-width); background: white; border-right: 1px solid var(--border); height: calc(100vh - 60px); position: sticky; top: 60px; overflow-y: auto; padding: 1rem; }
.sidebar h3 { font-size: 0.75rem; text-transform: uppercase; color: var(--muted); margin: 1rem 0 0.5rem; letter-spacing: 0.05em; }
.sidebar ul { list-style: none; }
.sidebar li { margin-bottom: 0.25rem; }
.sidebar a { display: block; padding: 0.3rem 0.5rem; border-radius: 4px; font-size: 0.9rem; transition: background 0.15s; }
.sidebar a:hover { background: #f0f0f0; text-decoration: none; }
.topic-badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.75rem; color: white; margin: 0.1rem; }
.main { flex: 1; padding: 2rem; min-width: 0; }
.video-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; transition: box-shadow 0.2s; }
.video-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.video-card h2 { font-size: 1.15rem; margin-bottom: 0.5rem; }
.video-card h2 a { color: var(--primary); }
.video-meta { font-size: 0.8rem; color: var(--muted); margin-bottom: 0.75rem; }
.video-meta span { margin-right: 1rem; }
.topic-list { margin: 0.75rem 0; }
.intro-block { background: #f8f9fa; border-left: 3px solid var(--accent); padding: 0.75rem 1rem; margin-top: 0.75rem; font-size: 0.9rem; color: #555; border-radius: 0 4px 4px 0; }
.intro-block .timestamp { font-family: monospace; color: var(--accent); font-size: 0.8rem; }
.wiki-nav { margin-bottom: 2rem; }
.wiki-nav a { margin-right: 1rem; font-size: 0.9rem; }
.section-title { font-size: 1.5rem; color: var(--primary); margin: 2rem 0 1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
.topic-header { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
.topic-header h1 { color: var(--primary); margin-bottom: 0.5rem; }
.cross-refs { background: #f0f4f8; border-radius: 8px; padding: 1rem; margin-top: 1rem; }
.cross-refs h4 { font-size: 0.85rem; margin-bottom: 0.5rem; color: var(--muted); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.timestamp-link { font-family: monospace; font-size: 0.8rem; color: var(--accent); background: #e8f4fc; padding: 0.1rem 0.4rem; border-radius: 3px; margin: 0 0.25rem; }
.footer { text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 3rem; }
.cat-section { margin-top: 0.5rem; }
.cat-badge { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.7rem; color: white; margin: 0.1rem; }
.entities { font-size: 0.8rem; color: #888; margin-top: 0.5rem; }
.entities span { background: #f0f0f0; padding: 0.1rem 0.3rem; border-radius: 3px; margin: 0 0.15rem; }
`;

console.log(`Loaded ${summaries.length} videos, ${Object.keys(topicMap).length} topics, ${Object.keys(categoryMap).length} categories`);

// Ensure directories
['topics', 'videos', 'styles'].forEach(d => {
  const dir = path.join(ROOT, d);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// =====================
// BUILD HOME PAGE
// =====================
function buildHomePage() {
  const topicCounts = Object.entries(topicMap)
    .filter(([t]) => TOPIC_DEFINITIONS[t])
    .sort((a, b) => b[1].length - a[1].length);

  const topicGrid = topicCounts.map(([topic, ids]) => {
    const def = TOPIC_DEFINITIONS[topic];
    return `<a href="topics/${slugify(topic)}.html" style="background:white;border:1px solid var(--border);border-radius:8px;padding:1rem;display:block;text-decoration:none;color:inherit">
      <div style="display:flex;align-items:center;margin-bottom:0.5rem">
        <span style="display:inline-block;width:10px;height:10px;background:${def.color};border-radius:50%;margin-right:0.5rem"></span>
        <strong style="color:var(--primary)">${topic}</strong>
      </div>
      <div style="font-size:0.8rem;color:var(--muted)">${def.description}</div>
      <div style="font-size:0.75rem;color:var(--accent);margin-top:0.5rem">${ids.length} videos</div>
    </a>`;
  }).join('');

  const catGrid = Object.entries(CATEGORY_DEFINITIONS).map(([cat, def]) => {
    const count = categoryMap[cat] ? categoryMap[cat].length : 0;
    return `<span class="cat-badge" style="background:${def.color}" title="${def.description}">${cat} (${count})</span>`;
  }).join(' ');

  const recentVideos = summaries.sort((a,b) => b.date.localeCompare(a.date)).slice(0, 12);
  const recentHTML = recentVideos.map(v => `
    <div class="video-card">
      <h2><a href="videos/${v.id}.html">${v.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(v.date)}</span>
        <span>⏱ ${formatDuration(v.duration)}</span>
      </div>
      <div class="topic-list">
        ${(v.topics || []).map(t => topicBadge(t.topic)).join('')}
      </div>
      <div class="cat-section">
        ${(v.categories || []).map(c => categoryBadge(c)).join('')}
      </div>
    </div>`).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Predictive History Wiki | Prof. Jiang Xueqin</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="header">
    <h1><a href="index.html">📚 Predictive History Wiki</a></h1>
    <div class="search-bar">
      <input type="text" placeholder="Search wiki..." onkeydown="if(event.key==='Enter') window.location.search='?q='+encodeURIComponent(this.value)">
    </div>
  </div>
  <div class="layout">
    <div class="sidebar">
      <h3>Thematic Pages</h3>
      <ul>
        <li><a href="predictions.html">📌 Predictions</a></li>
        <li><a href="law_of_proximity.html">📐 Law of Proximity</a></li>
        <li><a href="eschatology.html">🔮 Eschatology</a></li>
        <li><a href="strategic_concepts.html">⚔️ Strategic Concepts</a></li>
        <li><a href="categories.html">📂 Categories</a></li>
      </ul>
      <h3>Topics</h3>
      <ul>
        ${Object.keys(TOPIC_DEFINITIONS).sort().map(t => `<li><a href="topics/${slugify(t)}.html">${t}</a></li>`).join('\n')}
      </ul>
    </div>
    <div class="main">
      <div style="background:linear-gradient(135deg,#2c3e50,#3498db);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">Predictive History Wiki</h1>
        <p style="opacity:0.9">Comprehensive knowledge base of Prof. Jiang Xueqin's geopolitical framework, game theory analysis, and civilizational outlook.</p>
        <div style="margin-top:0.75rem;font-size:0.85rem;opacity:0.8">
          <strong>${summaries.length} videos</strong> indexed · ${formatDate(summaries.sort((a,b)=>a.date.localeCompare(b.date))[0].date)} → ${formatDate(summaries.sort((a,b)=>b.date.localeCompare(a.date))[0].date)}
        </div>
      </div>

      <h2 class="section-title">Categories</h2>
      <div style="margin-bottom:1.5rem">${catGrid}</div>

      <h2 class="section-title">Topics (${topicCounts.length})</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;margin-bottom:2rem">
        ${topicGrid}
      </div>

      <h2 class="section-title">Recent Videos</h2>
      <div class="grid">${recentHTML}</div>
    </div>
  </div>
  <div class="footer">
    Predictive History Wiki · ${summaries.length} videos · Built from Prof. Jiang Xueqin's content<br>
    <a href="https://www.youtube.com/@PredictiveHistory" target="_blank">YouTube</a> · 
    <a href="https://predictivehistory.substack.com/" target="_blank">Substack</a>
  </div>
</body>
</html>`;
}

// =====================
// BUILD VIDEO PAGE
// =====================
function buildVideoPage(v) {
  const topics = v.topics || [];
  const cats = v.categories || [];
  const countries = v.countries || [];
  const topicBadges = topics.map(t => topicBadge(t.topic)).join('');
  const catBadges = cats.map(c => categoryBadge(c)).join('');

  // Find related videos
  const related = [];
  const topicSet = new Set(topics.map(t => t.topic));
  const catSet = new Set(cats);
  for (const other of summaries) {
    if (other.id === v.id) continue;
    const otherTopics = new Set((other.topics || []).map(t => t.topic));
    const otherCats = new Set(other.categories || []);
    const topicOverlap = [...topicSet].filter(t => otherTopics.has(t)).length;
    const catOverlap = [...catSet].filter(c => otherCats.has(c)).length;
    if (topicOverlap + catOverlap >= 3) {
      related.push({ video: other, overlap: topicOverlap + catOverlap });
    }
  }
  related.sort((a, b) => b.overlap - a.overlap);
  related = related.slice(0, 6);

  const relatedHTML = related.map(r => `
    <div class="video-card">
      <h2><a href="../videos/${r.video.id}.html">${r.video.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(r.video.date)}</span>
        <span>⏱ ${formatDuration(r.video.duration)}</span>
      </div>
      <div class="topic-list">${(r.video.topics||[]).map(t => topicBadge(t.topic)).join('')}</div>
      <div class="cat-section">${(r.video.categories||[]).map(c => categoryBadge(c)).join('')}</div>
      <div style="font-size:0.8rem;color:#888;margin-top:0.5rem">Shared: ${r.overlap}</div>
    </div>`).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${v.title} | Predictive History Wiki</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="header">
    <h1><a href="../index.html">📚 Predictive History Wiki</a></h1>
    <div class="search-bar">
      <input type="text" placeholder="Search wiki..." onkeydown="if(event.key==='Enter') window.location.search='?q='+encodeURIComponent(this.value)">
    </div>
  </div>
  <div class="layout">
    <div class="sidebar">
      <h3>Thematic Pages</h3>
      <ul>
        <li><a href="../predictions.html">📌 Predictions</a></li>
        <li><a href="../law_of_proximity.html">📐 Law of Proximity</a></li>
        <li><a href="../eschatology.html">🔮 Eschatology</a></li>
        <li><a href="../strategic_concepts.html">⚔️ Strategic Concepts</a></li>
        <li><a href="../categories.html">📂 Categories</a></li>
      </ul>
      <h3>Topics</h3>
      <ul>
        ${Object.keys(TOPIC_DEFINITIONS).sort().map(t => `<li><a href="../topics/${slugify(t)}.html">${t}</a></li>`).join('\n')}
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="../index.html">← Wiki Home</a>
      </div>
      <div class="video-card">
        <h2>${v.title}</h2>
        <div class="video-meta">
          <span>📅 <a href="${v.url}" target="_blank">${formatDate(v.date)}</a></span>
          <span>⏱ ${formatDuration(v.duration)}</span>
          <span>🔗 <a href="${v.url}" target="_blank">Watch on YouTube ↗</a></span>
        </div>
        <div class="topic-list">${topicBadges || '<em>No topics tagged</em>'}</div>
        <div class="cat-section">${catBadges ? 'Categories: ' + catBadges : ''}</div>
        ${countries.length > 0 ? `<div class="entities">Countries: ${countries.map(c => `<span>${c}</span>`).join('')}</div>` : ''}
        
        ${topics.length > 0 ? `
        <div class="intro-block">
          <h4 style="margin-bottom:0.5rem;color:var(--primary)">Topics (first mentions):</h4>
          ${topics.map(t => {
            const intro = t.first_mention;
            if (!intro) return `<div><strong>${t.topic}</strong></div>`;
            return `<div style="margin-bottom:0.5rem">
              <strong>${t.topic}</strong>
              <span class="timestamp">@ ${formatTimestamp(intro.start)}</span>
              <div style="color:#555;font-size:0.85rem">${intro.text}</div>
            </div>`;
          }).join('')}
        </div>` : ''}
      </div>

      ${related.length > 0 ? `
      <h2 class="section-title">Related Videos</h2>
      <div class="grid">${relatedHTML}</div>` : ''}

      <h2 class="section-title">Transcript</h2>
      <div style="background:white;border:1px solid var(--border);border-radius:8px;padding:1.5rem;font-size:0.9rem;line-height:1.8;white-space:pre-wrap;max-height:80vh;overflow-y:auto">
        ${(v.full_text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')}
      </div>
    </div>
  </div>
</body>
</html>`;
}

// =====================
// BUILD CATEGORIES PAGE
// =====================
function buildCategoriesPage() {
  const catCards = Object.entries(CATEGORY_DEFINITIONS).map(([cat, def]) => {
    const videoIds = categoryMap[cat] || [];
    const videos = videoIds.map(id => summaries.find(v => v.id === id)).filter(Boolean).slice(0, 5);
    const videoCards = videos.map(v => `
      <div style="margin-bottom:0.5rem">
        <a href="videos/${v.id}.html" style="font-size:0.85rem">${v.title}</a>
        <span style="font-size:0.75rem;color:#888">${formatDate(v.date)}</span>
      </div>`).join('');
    
    return `
    <div class="video-card" style="border-top:3px solid ${def.color}">
      <h2 style="color:${def.color}">${cat}</h2>
      <p style="color:#666;font-size:0.9rem;margin:0.5rem 0">${def.description}</p>
      <div style="font-size:0.8rem;color:#888;margin-bottom:0.75rem">${videoIds.length} videos</div>
      ${videoCards}
      ${videoIds.length > 5 ? `<div style="margin-top:0.5rem"><a href="categories/${cat}.html" style="font-size:0.8rem">View all ${videoIds.length} →</a></div>` : ''}
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Categories | Predictive History Wiki</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="header">
    <h1><a href="index.html">📚 Predictive History Wiki</a></h1>
    <div class="search-bar">
      <input type="text" placeholder="Search wiki..." onkeydown="if(event.key==='Enter') window.location.search='?q='+encodeURIComponent(this.value)">
    </div>
  </div>
  <div class="layout">
    <div class="sidebar">
      <h3>Thematic Pages</h3>
      <ul>
        <li><a href="predictions.html">📌 Predictions</a></li>
        <li><a href="law_of_proximity.html">📐 Law of Proximity</a></li>
        <li><a href="eschatology.html">🔮 Eschatology</a></li>
        <li><a href="strategic_concepts.html">⚔️ Strategic Concepts</a></li>
        <li><a href="categories.html">📂 Categories</a></li>
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="index.html">← Wiki Home</a>
      </div>
      <div style="background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">📂 Categories</h1>
        <p style="opacity:0.9">Videos organized by <strong>${Object.keys(CATEGORY_DEFINITIONS).length} content categories</strong>: ${Object.keys(CATEGORY_DEFINITIONS).join(', ')}.</p>
      </div>
      <div class="grid">${catCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// =====================
// BUILD TOPIC PAGE
// =====================
function buildTopicPage(topic) {
  const def = TOPIC_DEFINITIONS[topic] || { description: '', color: '#666' };
  const color = def.color;
  
  const relevantVideos = summaries.filter(v => 
    (v.topics || []).some(t => t.topic === topic)
  ).sort((a, b) => b.date.localeCompare(a.date));

  const topicCount = {};
  for (const v of relevantVideos) {
    for (const t of (v.topics || [])) {
      if (t.topic !== topic) topicCount[t.topic] = (topicCount[t.topic] || 0) + 1;
    }
  }
  const relatedTopics = Object.entries(topicCount)
    .filter(([t, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([t]) => t);

  const videoCards = relevantVideos.map(v => {
    const otherTopics = (v.topics || []).filter(t => t.topic !== topic).map(t => t.topic);
    return `
    <div class="video-card">
      <h2><a href="../videos/${v.id}.html">${v.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(v.date)}</span>
        <span>⏱ ${formatDuration(v.duration)}</span>
      </div>
      <div class="topic-list">${(v.topics || []).map(t => topicBadge(t.topic)).join('')}</div>
      <div class="cat-section">${(v.categories||[]).map(c => categoryBadge(c)).join('')}</div>
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${topic} | Predictive History Wiki</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="header">
    <h1><a href="../index.html">📚 Predictive History Wiki</a></h1>
    <div class="search-bar">
      <input type="text" placeholder="Search wiki..." onkeydown="if(event.key==='Enter') window.location.search='?q='+encodeURIComponent(this.value)">
    </div>
  </div>
  <div class="layout">
    <div class="sidebar">
      <h3>Thematic Pages</h3>
      <ul>
        <li><a href="../predictions.html">📌 Predictions</a></li>
        <li><a href="../law_of_proximity.html">📐 Law of Proximity</a></li>
        <li><a href="../eschatology.html">🔮 Eschatology</a></li>
        <li><a href="../strategic_concepts.html">⚔️ Strategic Concepts</a></li>
        <li><a href="../categories.html">📂 Categories</a></li>
      </ul>
      <h3>Topics</h3>
      <ul>
        ${Object.keys(TOPIC_DEFINITIONS).sort().map(t => `<li><a href="${slugify(t)}.html">${t}</a></li>`).join('\n')}
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="../index.html">← Wiki Home</a>
      </div>
      <div class="topic-header">
        <h1><span style="display:inline-block;width:12px;height:12px;background:${color};border-radius:50%;margin-right:0.5rem"></span>${topic}</h1>
        <p>${def.description}</p>
        <div style="margin-top:0.75rem;font-size:0.85rem;color:var(--muted)">
          Appears in <strong>${relevantVideos.length}</strong> videos
        </div>
        ${relatedTopics.length > 0 ? `
        <div class="cross-refs">
          <h4>Related Topics</h4>
          ${relatedTopics.map(t => topicBadge(t)).join('')}
        </div>` : ''}
      </div>
      <h2 class="section-title">Videos (${relevantVideos.length})</h2>
      <div class="grid">${videoCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// =====================
// BUILD ALL
// =====================
console.log('Building home page...');
fs.writeFileSync(path.join(ROOT, 'index.html'), buildHomePage());
console.log('✓ index.html');

console.log('Building categories page...');
fs.writeFileSync(path.join(ROOT, 'categories.html'), buildCategoriesPage());
console.log('✓ categories.html');

console.log('Building 41 topic pages...');
for (const topic of Object.keys(TOPIC_DEFINITIONS)) {
  const html = buildTopicPage(topic);
  fs.writeFileSync(path.join(ROOT, 'topics', `${slugify(topic)}.html`), html);
}
console.log('✓ 41 topic pages');

console.log('Building 288 video pages...');
let built = 0;
let errors = 0;
for (const video of summaries) {
  try {
    const html = buildVideoPage(video);
    fs.writeFileSync(path.join(ROOT, 'videos', `${video.id}.html`), html);
    built++;
    if (built % 50 === 0) console.log(`  ✓ ${built}/288`);
  } catch(e) {
    errors++;
  }
}
console.log(`✓ ${built} video pages, ${errors} errors`);

console.log('\n✅ Full wiki rebuild complete!');