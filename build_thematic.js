const fs = require('fs');
const path = require('path');

// Load data
const predictions = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/predictions.json', 'utf8'));
const lopVideos = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/lop_videos.json', 'utf8'));
const eschVideos = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/eschatology_videos.json', 'utf8'));
const extraTopics = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/extra_topics.json', 'utf8'));
const summaries = JSON.parse(fs.readFileSync('/home/feiteira/.openclaw/workspace/video_summaries.json', 'utf8'));

const ROOT = '/home/feiteira/.openclaw/workspace';

// Reuse CSS (inline for these pages)
const CSS = fs.readFileSync(path.join(ROOT, 'styles/wiki.css'), 'utf8');

function slugify(text) {
  return text.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
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
  return `<a href="topics/${slugify(topic)}.html" class="topic-badge" style="background:#666">${topic}</a>`;
}

// ====================
// PREDICTIONS PAGE
// ====================
function buildPredictionsPage() {
  const predictionsByYear = {};
  
  // Sort predictions by date
  const sorted = [...predictions].sort((a, b) => b.date.localeCompare(a.date));
  
  const predCards = sorted.map(p => {
    const predList = p.predictions.map(pred => `
      <div style="margin-bottom:0.5rem;padding:0.5rem;background:#f8f9fa;border-radius:4px">
        <span style="font-family:monospace;color:#3498db;font-size:0.8rem">@ ${formatTimestamp(pred.start)}</span>
        <div style="margin-top:0.25rem">"${pred.text.slice(0,200)}${pred.text.length > 200 ? '...' : ''}"</div>
      </div>
    `).join('');
    
    return `
    <div class="video-card">
      <h2><a href="videos/${p.video_id}.html">${p.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(p.date)}</span>
        <span>🔗 <a href="${p.url}" target="_blank">YouTube</a></span>
      </div>
      <div style="margin-top:0.75rem">
        ${predList}
      </div>
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Predictions | Predictive History Wiki</title>
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
      </ul>
      <h3>Topics</h3>
      <ul>
        <li><a href="topics/iran.html">Iran</a></li>
        <li><a href="topics/china.html">China</a></li>
        <li><a href="topics/empire.html">Empire</a></li>
        <li><a href="topics/game_theory.html">Game Theory</a></li>
        <li><a href="topics/civilization.html">Civilization</a></li>
        <li><a href="topics/collapse.html">Collapse</a></li>
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="index.html">← Wiki Home</a> | <a href="predictions.html">Predictions</a> | <a href="law_of_proximity.html">Law of Proximity</a> | <a href="eschatology.html">Eschatology</a> | <a href="strategic_concepts.html">Strategic Concepts</a>
      </div>
      
      <div style="background:linear-gradient(135deg,#8e44ad,#9b59b6);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">📌 Predictions</h1>
        <p style="opacity:0.9">Forward-looking statements, forecasts, and prognostications from Prof. Jiang Xueqin across <strong>${predictions.length} videos</strong>.</p>
        <div style="margin-top:1rem;font-size:0.85rem;opacity:0.8">
          Pattern: "will", "is going to", "predict", "forecast", "by 20XX", "within X years"
        </div>
      </div>

      <h2 class="section-title">All Predictions (${predictions.length} videos)</h2>
      <div class="grid">${predCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// ====================
// LAW OF PROXIMITY PAGE
// ====================
function buildLoPPage() {
  // Get the Game Theory #14 video specifically
  const g14 = summaries.find(v => v.title.includes('Game Theory #14') || v.title.includes('Law of Proximity'));
  
  const lopCards = lopVideos.map(v => {
    return `
    <div class="video-card">
      <h2><a href="videos/${v.video_id}.html">${v.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(v.date)}</span>
        <span>🔗 <a href="${v.url}" target="_blank">YouTube</a></span>
      </div>
      ${v.first_ts ? `
      <div style="margin-top:0.75rem;padding:0.75rem;background:#f8f9fa;border-radius:4px;border-left:3px solid #9b59b6">
        <span style="font-family:monospace;color:#9b59b6;font-size:0.8rem">@ ${formatTimestamp(v.first_ts)}</span>
        <div style="margin-top:0.5rem;color:#555">"${v.first_text.slice(0,300)}${v.first_text.length > 300 ? '...' : ''}"</div>
      </div>` : ''}
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Law of Proximity | Predictive History Wiki</title>
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
      </ul>
      <h3>Topics</h3>
      <ul>
        <li><a href="topics/iran.html">Iran</a></li>
        <li><a href="topics/china.html">China</a></li>
        <li><a href="topics/empire.html">Empire</a></li>
        <li><a href="topics/game_theory.html">Game Theory</a></li>
        <li><a href="topics/civilization.html">Civilization</a></li>
        <li><a href="topics/collapse.html">Collapse</a></li>
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="index.html">← Wiki Home</a> | <a href="predictions.html">Predictions</a> | <a href="law_of_proximity.html">Law of Proximity</a> | <a href="eschatology.html">Eschatology</a> | <a href="strategic_concepts.html">Strategic Concepts</a>
      </div>
      
      <div style="background:linear-gradient(135deg,#8e44ad,#3498db);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">📐 Law of Proximity</h1>
        <p style="opacity:0.9">Prof. Jiang Xueqin's proprietary analytical framework. "Things that are close to each other in strategic space will affect each other disproportionately." Found in <strong>${lopVideos.length} videos</strong>.</p>
      </div>

      <h2 class="section-title">Core Video (Game Theory #14)</h2>
      ${g14 ? `
      <div class="video-card" style="border-left:4px solid #8e44ad">
        <h2><a href="videos/${g14.id}.html">${g14.title}</a></h2>
        <div class="video-meta">
          <span>📅 ${formatDate(g14.date)}</span>
          <span>⏱ ${Math.round(g14.duration/60)} min</span>
          <span>🔗 <a href="${g14.url}" target="_blank">YouTube</a></span>
        </div>
        <div class="topic-list">
          ${(g14.topics||[]).map(t => topicBadge(t.topic)).join('')}
        </div>
      </div>` : ''}

      <h2 class="section-title">All Videos Mentioning Law of Proximity (${lopVideos.length})</h2>
      <div class="grid">${lopCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// ====================
// ESCHATOLOGY PAGE
// ====================
function buildEschPage() {
  // Eschatology topics from extra_topics
  const eschTopics = ['Eschatology', 'Apocalypse', 'Millennium', 'Prophecy', 'End Times', 'Judgement Day'];
  
  const eschCards = eschVideos.map(v => {
    // Determine which esch keyword is mentioned
    const keywords = [];
    if (v.first_text) {
      const lower = v.first_text.toLowerCase();
      if (lower.includes('eschatology')) keywords.push('Eschatology');
      if (lower.includes('end times')) keywords.push('End Times');
      if (lower.includes('apocalypse')) keywords.push('Apocalypse');
      if (lower.includes('prophecy')) keywords.push('Prophecy');
      if (lower.includes('millennium')) keywords.push('Millennium');
    }
    
    return `
    <div class="video-card">
      <h2><a href="videos/${v.video_id}.html">${v.title}</a></h2>
      <div class="video-meta">
        <span>📅 ${formatDate(v.date)}</span>
        <span>🔗 <a href="${v.url}" target="_blank">YouTube</a></span>
      </div>
      ${keywords.length > 0 ? `
      <div style="margin-top:0.5rem">${keywords.map(k => `<span class="topic-badge" style="background:#8e44ad">${k}</span>`).join('')}</div>
      ` : ''}
      ${v.first_ts ? `
      <div style="margin-top:0.75rem;padding:0.75rem;background:#f8f9fa;border-radius:4px;border-left:3px solid #8e44ad">
        <span style="font-family:monospace;color:#8e44ad;font-size:0.8rem">@ ${formatTimestamp(v.first_ts)}</span>
        <div style="margin-top:0.5rem;color:#555">"${v.first_text.slice(0,250)}${v.first_text.length > 250 ? '...' : ''}"</div>
      </div>` : ''}
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Eschatology & End Times | Predictive History Wiki</title>
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
      </ul>
      <h3>Topics</h3>
      <ul>
        <li><a href="topics/iran.html">Iran</a></li>
        <li><a href="topics/china.html">China</a></li>
        <li><a href="topics/empire.html">Empire</a></li>
        <li><a href="topics/game_theory.html">Game Theory</a></li>
        <li><a href="topics/civilization.html">Civilization</a></li>
        <li><a href="topics/collapse.html">Collapse</a></li>
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="index.html">← Wiki Home</a> | <a href="predictions.html">Predictions</a> | <a href="law_of_proximity.html">Law of Proximity</a> | <a href="eschatology.html">Eschatology</a> | <a href="strategic_concepts.html">Strategic Concepts</a>
      </div>
      
      <div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">🔮 Eschatology & End Times</h1>
        <p style="opacity:0.9">Prof. Jiang's use of eschatological frameworks, apocalyptic reasoning, and prophetic analysis. Found in <strong>${eschVideos.length} videos</strong> across categories like eschatology, apocalypse, prophecy, end times, and millennium.</p>
        <div style="margin-top:1rem;font-size:0.85rem;opacity:0.8">
          Related: <span style="background:rgba(255,255,255,0.2);padding:0.2rem 0.5rem;border-radius:4px;margin-right:0.5rem">Islam</span>
          <span style="background:rgba(255,255,255,0.2);padding:0.2rem 0.5rem;border-radius:4px;margin-right:0.5rem">Christianity</span>
          <span style="background:rgba(255,255,255,0.2);padding:0.2rem 0.5rem;border-radius:4px;margin-right:0.5rem">Judaism</span>
          <span style="background:rgba(255,255,255,0.2);padding:0.2rem 0.5rem;border-radius:4px">Game Theory</span>
        </div>
      </div>

      <h2 class="section-title">Videos with Eschatological Content (${eschVideos.length})</h2>
      <div class="grid">${eschCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// ====================
// STRATEGIC CONCEPTS PAGE
// ====================
function buildStrategicPage() {
  // Key strategic concepts from the videos
  const concepts = [
    { name: 'Game Theory', desc: 'Strategic interaction analysis, Nash equilibrium, zero-sum vs non-zero-sum games', videos: extraTopics['Game Theory'] || [] },
    { name: 'Law of Proximity', desc: '"Things close in strategic space affect each other disproportionately"', videos: lopVideos },
    { name: 'Grand Strategy', desc: 'Long-term national strategy, great power competition', videos: extraTopics['Grand Strategy'] || [] },
    { name: 'Strategy Matrix', desc: 'Framework for analyzing strategic options across multiple dimensions', videos: extraTopics['Strategy Matrix'] || [] },
    { name: 'Hegemony', desc: 'Global dominance, unipolar moment, hegemonic decline', videos: extraTopics['Hegemony'] || [] },
    { name: 'Red Lines', desc: 'Critical thresholds that trigger major consequences if crossed', videos: extraTopics['Red Lines'] || [] },
    { name: 'Trigger', desc: 'Events that cascade into larger strategic outcomes', videos: extraTopics['Trigger'] || [] },
    { name: 'Threshold', desc: 'Tipping points in civilizational and strategic dynamics', videos: extraTopics['Threshold'] || [] },
  ];
  
  const conceptCards = concepts.map(c => {
    const videoCards = c.videos.slice(0, 5).map(v => `
      <div style="margin-bottom:0.5rem">
        <a href="videos/${v.video_id || v.id || v}.html" style="font-size:0.85rem">${v.title || v}</a>
      </div>
    `).join('');
    
    return `
    <div class="video-card" style="border-top:3px solid #2c3e50">
      <h2 style="color:#2c3e50">${c.name}</h2>
      <p style="color:#666;font-size:0.9rem;margin:0.5rem 0">${c.desc}</p>
      <div style="font-size:0.8rem;color:#888;margin-bottom:0.5rem">Appears in ${c.videos.length} videos</div>
      ${videoCards}
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Strategic Concepts | Predictive History Wiki</title>
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
      </ul>
      <h3>Topics</h3>
      <ul>
        <li><a href="topics/iran.html">Iran</a></li>
        <li><a href="topics/china.html">China</a></li>
        <li><a href="topics/empire.html">Empire</a></li>
        <li><a href="topics/game_theory.html">Game Theory</a></li>
        <li><a href="topics/civilization.html">Civilization</a></li>
        <li><a href="topics/collapse.html">Collapse</a></li>
      </ul>
    </div>
    <div class="main">
      <div class="wiki-nav">
        <a href="index.html">← Wiki Home</a> | <a href="predictions.html">Predictions</a> | <a href="law_of_proximity.html">Law of Proximity</a> | <a href="eschatology.html">Eschatology</a> | <a href="strategic_concepts.html">Strategic Concepts</a>
      </div>
      
      <div style="background:linear-gradient(135deg,#2c3e50,#34495e);color:white;border-radius:12px;padding:2rem;margin-bottom:2rem">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">⚔️ Strategic Concepts</h1>
        <p style="opacity:0.9">The core analytical frameworks and key concepts Prof. Jiang Xueqin uses to analyze geopolitics and civilizational dynamics.</p>
      </div>

      <div class="grid">${conceptCards}</div>
    </div>
  </div>
</body>
</html>`;
}

// Build all thematic pages
console.log('Building thematic pages...');
fs.writeFileSync(path.join(ROOT, 'predictions.html'), buildPredictionsPage());
fs.writeFileSync(path.join(ROOT, 'law_of_proximity.html'), buildLoPPage());
fs.writeFileSync(path.join(ROOT, 'eschatology.html'), buildEschPage());
fs.writeFileSync(path.join(ROOT, 'strategic_concepts.html'), buildStrategicPage());
console.log('✓ predictions.html');
console.log('✓ law_of_proximity.html');
console.log('✓ eschatology.html');
console.log('✓ strategic_concepts.html');
console.log('\n✅ Thematic pages complete!');