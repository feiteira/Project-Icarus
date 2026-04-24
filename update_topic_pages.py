#!/usr/bin/env python3
"""
Update topic pages with enriched prediction data from all related videos.
"""
import json
import re
import subprocess
import os
from collections import defaultdict

TRANSCRIPTS_DIR = '/home/feiteira/.openclaw/workspace/transcripts/transcripts'
SUMMARIES_FILE = '/home/feiteira/.openclaw/workspace/video_summaries.json'
OUTPUT_DIR = '/home/feiteira/.openclaw/workspace/topic_content'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prediction patterns
PREDICTION_PATTERNS = [
    r'will\s+(?:be|become|have|get|see|face|experience|launch|initiate|attack|invade|collapse|rise|fall|destabilize)',
    r'is\s+going\s+to\s+\w{3,}',
    r'is\s+about\s+to\s+\w{3,}',
    r'can\s+expect\s+',
    r'predict(?:s|ed)?\s+that\s+',
    r'forecast(?:s|ed)?\s+',
    r'warn(?:s|ed)?\s+(?:that\s+)?',
    r'the\s+\w+\s+will\s+\w{3,}',
    r'within\s+\d+\s+(?:years?|months?|weeks?)\s+',
    r'by\s+\d{4}\s+',
    r'there\s+will\s+be\s+(?:a\s+)?',
    r'in\s+(?:the\s+)?(?:next|coming|upcoming)\s+\w+\s+',
    r'before\s+the\s+end\s+of\s+(?:the\s+)?(?:year|decade|century)',
    r'imminent(?:ly)?\s+',
    r'impending\s+',
    r'china\'?s?\s+(?:will\s+)?(?:intend|attack|threat|challenge|plan)',
    r'russia\s+(?:will|is\s+going\s+to|intend)',
    r'iran\s+(?:will|is\s+going\s+to|is\s+about\s+to)',
    r'north\s+korea\s+(?:will|is\s+going\s+to|is\s+about\s+to)',
    r'is\s+(?:the\s+)?(?:next|final)\s+(?:target|war|battle)',
    r'within\s+(?:the\s+)?(?:next\s+)?(?:few\s+)?(?:months|weeks|years)',
    r'come\s+to\s+power\s+',
    r'take\s+over\s+',
    r'break\s+up\s+',
    r'fall\s+(?:of|to)',
    r'be\s+(?:the\s+)?(?:end|beginning)\s+of',
]

def load_summaries():
    with open(SUMMARIES_FILE) as f:
        return json.load(f)

def load_transcript(video_id):
    path = os.path.join(TRANSCRIPTS_DIR, f'{video_id}.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def extract_predictions(full_text, date):
    """Extract prediction sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    predictions = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 40 or len(sent) > 600:
            continue
        for pat in PREDICTION_PATTERNS:
            if re.search(pat, sent, re.IGNORECASE):
                predictions.append({'text': sent, 'date': date})
                break
    return predictions

def get_topic_video_predictions(topic, summaries):
    """Collect all predictions and analysis for a given topic."""
    results = []
    for s in summaries:
        # Check if this video covers this topic
        topic_names = [t['topic'] for t in s.get('topics', [])]
        if topic not in topic_names:
            continue

        video_id = s['id']
        date = s.get('date', 'Unknown')
        url = s.get('url', f'https://youtube.com/watch?v={video_id}')
        title = s.get('title', 'Unknown')

        transcript = load_transcript(video_id)
        if transcript:
            full_text = transcript.get('full_text', '')
        else:
            full_text = s.get('full_text', '')

        predictions = extract_predictions(full_text, date)

        # Get topic-relevant text snippets
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        snippets = []
        for sent in sentences:
            if topic.lower() in sent.lower() and 50 < len(sent) < 500:
                snippets.append(sent.strip())

        results.append({
            'video_id': video_id,
            'title': title,
            'url': url,
            'date': date,
            'predictions': predictions,
            'snippets': snippets[:4],
            'full_text': full_text
        })

    return results

# Country context data
COUNTRY_CONTEXTS = {
    'Iran': {
        'population': '~88 million (2024)', 'capital': 'Tehran', 'area': '1,648,195 km²',
        'gdp': '~$388 billion (2023)', 'exports': 'Oil, petrochemicals, carpets, foodstuffs',
        'partners': 'China, Iraq, UAE, Turkey', 'government': 'Islamic Republic',
        'leader': 'Supreme Leader Khamenei, President Pezeshkian'
    },
    'China': {
        'population': '~1.4 billion (2024)', 'capital': 'Beijing', 'area': '9,596,960 km²',
        'gdp': '~$17.7 trillion (2023)', 'exports': 'Electronics, machinery, textiles, steel',
        'partners': 'USA, ASEAN, EU, Japan, South Korea', 'government': 'Communist Party-led state',
        'leader': 'President Xi Jinping'
    },
    'Russia': {
        'population': '~144 million (2024)', 'capital': 'Moscow', 'area': '17,098,242 km²',
        'gdp': '~$1.9 trillion (2023)', 'exports': 'Energy, metals, weapons, grain',
        'partners': 'China, India, Turkey', 'government': 'Federal semi-presidential republic',
        'leader': 'President Vladimir Putin'
    },
    'Israel': {
        'population': '~9.8 million (2024)', 'capital': 'Jerusalem (disputed)', 'area': '22,072 km²',
        'gdp': '~$525 billion (2023)', 'exports': 'Technology, diamonds, pharmaceuticals, military',
        'partners': 'USA, EU, China, India', 'government': 'Parliamentary democracy',
        'leader': 'Prime Minister Netanyahu'
    },
    'United States': {
        'population': '~335 million (2024)', 'capital': 'Washington D.C.', 'area': '9,833,520 km²',
        'gdp': '~$27.4 trillion (2023)', 'exports': 'Machinery, aircraft, vehicles, electronics',
        'partners': 'Canada, Mexico, China, Japan, EU', 'government': 'Federal presidential republic',
        'leader': 'President Joe Biden'
    },
    'Ukraine': {
        'population': '~37 million (2024, pre-war)', 'capital': 'Kyiv', 'area': '603,500 km²',
        'gdp': '~$160 billion (2022)', 'exports': 'Grain, iron, steel, sunflower oil',
        'partners': 'EU, China, Turkey, Egypt', 'government': 'Unitary semi-presidential republic',
        'leader': 'President Volodymyr Zelenskyy'
    },
    'Saudi Arabia': {
        'population': '~34 million (2024)', 'capital': 'Riyadh', 'area': '2,149,690 km²',
        'gdp': '~$1.1 trillion (2023)', 'exports': 'Oil, petrochemicals, plastics',
        'partners': 'China, USA, Japan, India, EU', 'government': 'Absolute monarchy',
        'leader': 'King Salman, Crown Prince MBS'
    },
    'Japan': {
        'population': '~124 million (2024)', 'capital': 'Tokyo', 'area': '377,975 km²',
        'gdp': '~$4.2 trillion (2023)', 'exports': 'Vehicles, machinery, electronics, optical equipment',
        'partners': 'USA, China, South Korea, Taiwan, EU', 'government': 'Constitutional monarchy',
        'leader': 'Prime Minister Fumio Kishida'
    },
    'India': {
        'population': '~1.44 billion (2024)', 'capital': 'New Delhi', 'area': '3,287,263 km²',
        'gdp': '~$3.7 trillion (2023)', 'exports': 'Petroleum products, pharmaceuticals, IT services',
        'partners': 'USA, UAE, Saudi Arabia, China, Indonesia', 'government': 'Federal parliamentary republic',
        'leader': 'Prime Minister Narendra Modi'
    },
    'Taiwan': {
        'population': '~23.5 million (2024)', 'capital': 'Taipei', 'area': '36,193 km²',
        'gdp': '~$753 billion (2023)', 'exports': 'Electronics, machinery, plastics, metals',
        'partners': 'USA, China, Japan, Hong Kong, Singapore', 'government': 'Semi-presidential republic',
        'leader': 'President Lai Ching-te'
    },
    'Europe': {
        'population': '~748 million (2024)', 'capital': 'Brussels (EU HQ)', 'area': '10.18 million km²',
        'gdp': '~$21.8 trillion (EU, 2023)', 'exports': 'Machinery, vehicles, chemicals, pharmaceuticals',
        'partners': 'USA, China, UK, Russia (historically)', 'government': 'Multi-tiered political union',
        'leader': 'European Commission President: Ursula von der Leyen'
    },
    'Middle East': {
        'population': '~411 million (2024)', 'capital': 'Multiple', 'area': '7.2 million km²',
        'gdp': '~$3.8 trillion (2023)', 'exports': 'Oil, gas, petrochemicals',
        'partners': 'USA, China, EU, India', 'government': 'Varied (monarchies, republics, theocracies)',
        'leader': 'Multiple heads of state'
    },
    'NATO': {
        'population': '~950 million (2024)', 'capital': 'Brussels, Belgium', 'area': 'N/A',
        'gdp': '~$40+ trillion (combined)', 'exports': 'Defense equipment, technology',
        'partners': 'Member states: 32 countries', 'government': 'Military alliance',
        'leader': 'Secretary General Mark Rutte'
    },
    'South China Sea': {
        'population': 'N/A (disputed waters)', 'capital': 'N/A', 'area': '~3.5 million km²',
        'gdp': '~$3-5 trillion (surrounding)', 'exports': 'Trade routes, fisheries, energy reserves',
        'partners': 'China, Vietnam, Philippines, Malaysia, Brunei, Taiwan', 'government': 'Disputed territory',
        'leader': 'Multiple claimants'
    },
}

def context_table(country, ctx):
    return f"""{{| class="wikitable"
! colspan="2" | {country}
|- 
| '''Population''' || {ctx['population']}
|- 
| '''Capital''' || {ctx['capital']}
|- 
| '''Total Area''' || {ctx['area']}
|- 
| '''GDP''' || {ctx['gdp']}
|- 
| '''Major Exports''' || {ctx['exports']}
|- 
| '''Major Partners''' || {ctx['partners']}
|- 
| '''Government''' || {ctx['government']}
|- 
| '''Current Leader''' || {ctx['leader']}
|}}
"""

def build_topic_page(topic, video_data, summaries):
    """Build enriched topic page Wikitext."""
    total_videos = len(video_data)
    total_predictions = sum(len(v['predictions']) for v in video_data)

    # Get unique countries mentioned across all videos
    all_countries = set()
    for v in video_data:
        all_countries.update(v.get('countries', []))
    countries = [c for c in ['Iran', 'China', 'Russia', 'Israel', 'United States', 'Ukraine',
                             'Saudi Arabia', 'Japan', 'India', 'Taiwan', 'Europe', 'NATO',
                             'South China Sea'] if c in all_countries]

    wikitext = f"""'''{topic}''' is a topic extensively analyzed by Professor Jiang Xueqin in his Predictive History series. Professor Jiang brings unique geopolitical insights, combining deep historical analysis with contemporary strategic forecasting.

== Overview ==

Professor Jiang has discussed {topic} in {total_videos} videos, providing analysis that connects historical patterns to current events and future predictions. His approach synthesizes multiple civilizational perspectives, emphasizing the interconnected nature of global geopolitical forces.

This page consolidates his key predictions and analysis on {topic} across all videos in the series.

"""

    # Countries section with context tables
    if countries:
        wikitext += "== Countries & Regions ==\n\n"
        for c in countries:
            if c in COUNTRY_CONTEXTS:
                wikitext += f"=== {c} ===\n\n{context_table(c, COUNTRY_CONTEXTS[c])}\n\n"

    # Predictions section
    wikitext += "== Predictive History Analysis ==\n\n"
    wikitext += f"Below are the key predictions and strategic assessments made by Professor Jiang regarding {topic}:\n\n"

    # Group by video
    pred_count = 0
    for v in video_data:
        if not v['predictions']:
            continue
        wikitext += f"""=== {v['title'][:80]} ===

Video uploaded: {v['date']} — [{v['url']} Link]

"""
        for pred in v['predictions'][:3]:
            pred_count += 1
            # Clean and format
            text = pred['text'].strip()[:400]
            wikitext += f"""{pred_count}. {text}... <ref>Predictive History Channel, {pred['date']}</ref>

"""
        wikitext += "\n"

    if pred_count == 0:
        wikitext += "//No explicit predictions detected in the transcripts for this topic.//\n\n"

    # Key themes section
    wikitext += "== Key Themes ==\n\n"
    wikitext += "Based on Professor Jiang's analysis, the following recurring themes emerge:\n\n"
    wikitext += "* Multi-civilizational perspective — analyzing events through Eastern and Western historical lenses\n"
    wikitext += "* Long-cycle thinking — understanding that current events are often culmination of decades-long trends\n"
    wikitext += "* Strategic pattern recognition — identifying repeating geopolitical archetypes\n"

    # Video references
    wikitext += "\n== Video References ==\n\n"
    seen = set()
    for v in video_data:
        key = (v['video_id'], v['date'])
        if key not in seen:
            seen.add(key)
            pred_count = len([p for p in v['predictions']])
            wikitext += f"* [{v['url']} {v['title'][:80]}] — {v['date']} ({pred_count} predictions)\n"

    wikitext += f"""

[[Category:Topics|{{PAGENAME}}]]
[[Category:Predictive History|{topic}]]
"""

    return wikitext

def push_to_wiki(title, content):
    path = '/home/feiteira/.openclaw/workspace/wiki_page_content.txt'
    with open(path, 'w') as f:
        f.write(content)
    cmd = ['php', '/usr/share/mediawiki/maintenance/edit.php',
           '--summary', 'Updated with enriched Predictive History Analysis', title]
    with open(path, 'r') as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    if result.returncode == 0 and 'done' in result.stdout:
        return True, ""
    else:
        return False, result.stderr[:200]

# All known topics (from topic_data keys)
TOPICS = [
    'BRICS', 'Bitcoin', 'China', 'Christianity', 'Civil War', 'Civilization',
    'Cold War', 'Collapse', 'Constitution', 'Democracy', 'Empire', 'Europe',
    'Federal Reserve', 'Game Theory', 'Geopolitics', 'Gold', 'Holy Roman Empire',
    'India', 'Iran', 'Islam', 'Israel', 'Japan', 'Judaism', 'Middle East', 'NATO',
    'NeoCon', 'Nuclear', 'Roman Empire', 'Russia', 'Saudi Arabia', 'Secession',
    'Silk Road', 'South China Sea', 'Strategy', 'Taiwan', 'Trump', 'Ukraine',
    'United States', 'War', 'Woke', 'World Economic Forum'
]

def main():
    summaries = load_summaries()
    print(f"Loaded {len(summaries)} summaries")

    results = {'success': 0, 'failed': 0}
    for topic in TOPICS:
        video_data = get_topic_video_predictions(topic, summaries)
        if not video_data:
            print(f"[SKIP] {topic} — no videos found")
            continue

        wikitext = build_topic_page(topic, video_data, summaries)

        # Save locally
        safe = topic.replace('/', '_')
        with open(f'{OUTPUT_DIR}/{safe}.txt', 'w') as f:
            f.write(wikitext)

        # Push to wiki
        ok, err = push_to_wiki(topic, wikitext)
        if ok:
            pred_count = sum(len(v['predictions']) for v in video_data)
            print(f"[✓] {topic} — {len(video_data)} videos, {pred_count} predictions")
            results['success'] += 1
        else:
            print(f"[✗] {topic}: {err}")
            results['failed'] += 1

    print(f"\nDone: {results['success']} updated, {results['failed']} failed")

if __name__ == '__main__':
    main()
