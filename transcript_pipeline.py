#!/usr/bin/env python3
"""
Predictive History Wiki Pipeline
3-Agent system to extract predictions from transcripts, enrich with context,
and generate MediaWiki pages.
"""
import json
import re
import subprocess
import os
from datetime import datetime

TRANSCRIPTS_DIR = '/home/feiteira/.openclaw/workspace/transcripts/transcripts'
SUMMARIES_FILE = '/home/feiteira/.openclaw/workspace/video_summaries.json'
OUTPUT_DIR = '/home/feiteira/.openclaw/workspace/wiki_content'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prediction indicator patterns
PREDICTION_PATTERNS = [
    r'will\s+(?:be|become|have|get|see|face|experience|launch|initiate|attack|invade)',
    r'is\s+going\s+to\s+\w',
    r'is\s+about\s+to\s+\w',
    r'can\s+expect\s+',
    r'predict(?:s|ed)?\s+that\s+',
    r'forecast(?:s|ed)?\s+',
    r'warn(?:s|ed)?\s+(?:that\s+)?',
    r'the\s+\w+\s+will\s+\w',
    r'within\s+\d+\s+(?:years?|months?|weeks?)\s+',
    r'by\s+\d{4}\s+',
    r'china\'?s?\s+(?:will\s+)?(?:will\s+)?(?:attack|invade|threat|challenge)',
    r'the\s+us\s+(?:will|is\s+going\s+to|is\s+about\s+to)',
    r'russia\s+(?:will|is\s+going\s+to|is\s+about\s+to|intend)',
    r'iran\s+(?:will|is\s+going\s+to|is\s+about\s+to)',
    r'north\s+korea\s+(?:will|is\s+going\s+to|is\s+about\s+to)',
    r'is\s+the\s+(?:next|final)\s+(?:target|war|battle)',
    r'there\s+will\s+be\s+(?:a\s+)?',
    r'in\s+(?:the\s+)?(?:next|coming|upcoming)\s+\w+',
    r'before\s+the\s+end\s+of\s+(?:the\s+)?(?:year|decade|century)',
    r'imminent(?:ly)?\s+',
    r'impending\s+',
    r'within\s+(?:the\s+)?(?:next\s+)?(?:few\s+)?(?:months|weeks|years)',
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

def extract_predictions(full_text, title, date):
    """Extract sentences that look like predictions."""
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    predictions = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 30 or len(sent) > 500:
            continue
        for pat in PREDICTION_PATTERNS:
            if re.search(pat, sent, re.IGNORECASE):
                predictions.append({
                    'text': sent,
                    'date': date,
                    'matched_pattern': pat
                })
                break
    return predictions[:5]  # Max 5 per video

def extract_entity_sentences(full_text, entity):
    """Extract sentences mentioning an entity."""
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    mentions = []
    for sent in sentences:
        if entity.lower() in sent.lower() and len(sent) > 40 and len(sent) < 600:
            mentions.append(sent.strip())
    return mentions[:3]

def generate_country_context(country):
    """Generate factual context for a country."""
    facts = {
        'Iran': {
            'population': '~88 million (2024)',
            'capital': 'Tehran',
            'area': '1,648,195 km²',
            'gdp': '~$388 billion (2023)',
            'exports': 'Oil, petrochemicals, carpets, foodstuffs',
            'major_partners': 'China, Iraq, UAE, Turkey',
            'government': 'Islamic Republic',
            'leader': 'Supreme Leader Ayatollah Khamenei, President Pezeshkian'
        },
        'China': {
            'population': '~1.4 billion (2024)',
            'capital': 'Beijing',
            'area': '9,596,960 km²',
            'gdp': '~$17.7 trillion (2023)',
            'exports': 'Electronics, machinery, textiles, steel',
            'major_partners': 'USA, ASEAN, EU, Japan, South Korea',
            'government': 'Communist Party-led state',
            'leader': 'President Xi Jinping'
        },
        'Russia': {
            'population': '~144 million (2024)',
            'capital': 'Moscow',
            'area': '17,098,242 km²',
            'gdp': '~$1.9 trillion (2023)',
            'exports': 'Energy, metals, weapons, grain',
            'major_partners': 'China, India, Turkey, EU (historically)',
            'government': 'Federal semi-presidential republic',
            'leader': 'President Vladimir Putin'
        },
        'Israel': {
            'population': '~9.8 million (2024)',
            'capital': 'Jerusalem (disputed)',
            'area': '22,072 km²',
            'gdp': '~$525 billion (2023)',
            'exports': 'Technology, diamonds, pharmaceuticals, military equipment',
            'major_partners': 'USA, EU, China, India',
            'government': 'Parliamentary democracy',
            'leader': 'Prime Minister Netanyahu'
        },
        'United States': {
            'population': '~335 million (2024)',
            'capital': 'Washington D.C.',
            'area': '9,833,520 km²',
            'gdp': '~$27.4 trillion (2023)',
            'exports': 'Machinery, aircraft, vehicles, electronics',
            'major_partners': 'Canada, Mexico, China, Japan, EU',
            'government': 'Federal presidential republic',
            'leader': 'President Joe Biden'
        },
        'Ukraine': {
            'population': '~37 million (2024, pre-war)',
            'capital': 'Kyiv',
            'area': '603,500 km²',
            'gdp': '~$160 billion (2022)',
            'exports': 'Grain, iron, steel, sunflower oil',
            'major_partners': 'EU, China, Turkey, Egypt',
            'government': 'Unitary semi-presidential republic',
            'leader': 'President Volodymyr Zelenskyy'
        },
        'Saudi Arabia': {
            'population': '~34 million (2024)',
            'capital': 'Riyadh',
            'area': '2,149,690 km²',
            'gdp': '~$1.1 trillion (2023)',
            'exports': 'Oil, petrochemicals, plastics',
            'major_partners': 'China, USA, Japan, India, EU',
            'government': 'Absolute monarchy',
            'leader': 'King Salman bin Abdulaziz Al Saud, Crown Prince Mohammed bin Salman'
        },
        'Japan': {
            'population': '~124 million (2024)',
            'capital': 'Tokyo',
            'area': '377,975 km²',
            'gdp': '~$4.2 trillion (2023)',
            'exports': 'Vehicles, machinery, electronics, optical equipment',
            'major_partners': 'USA, China, South Korea, Taiwan, EU',
            'government': 'Constitutional monarchy',
            'leader': 'Prime Minister Fumio Kishida'
        },
        'India': {
            'population': '~1.44 billion (2024)',
            'capital': 'New Delhi',
            'area': '3,287,263 km²',
            'gdp': '~$3.7 trillion (2023)',
            'exports': 'Petroleum products, pharmaceutical goods, IT services',
            'major_partners': 'USA, UAE, Saudi Arabia, China, Indonesia',
            'government': 'Federal parliamentary democratic republic',
            'leader': 'Prime Minister Narendra Modi'
        },
        'Taiwan': {
            'population': '~23.5 million (2024)',
            'capital': 'Taipei',
            'area': '36,193 km²',
            'gdp': '~$753 billion (2023)',
            'exports': 'Electronics, machinery, plastics, metals',
            'major_partners': 'USA, China, Japan, Hong Kong, Singapore',
            'government': 'Semi-presidential republic',
            'leader': 'President Lai Ching-te'
        },
    }
    return facts.get(country, None)

def format_context_table(country, context):
    """Format country context as a Wikitext table."""
    if not context:
        return ""
    table = f"""{{| class="wikitable"
! colspan="2" | {country}
|- 
| '''Population''' || {context['population']}
|- 
| '''Capital''' || {context['capital']}
|- 
| '''Total Area''' || {context['area']}
|- 
| '''GDP''' || {context['gdp']}
|- 
| '''Major Exports''' || {context['exports']}
|- 
| '''Major Trading Partners''' || {context['major_partners']}
|- 
| '''Government''' || {context['government']}
|- 
| '''Current Leader''' || {context['leader']}
}}
"""
    return table

def build_prediction_wikitext(video_id, summary, predictions, transcript):
    """Build full Wikitext for a video analysis page."""
    title = summary['title'].replace('|', '-')
    date = summary.get('date', 'Unknown')
    url = summary.get('url', f'https://youtube.com/watch?v={video_id}')
    countries = summary.get('countries', [])
    leaders = summary.get('leaders', [])
    categories = summary.get('categories', [])
    full_text = transcript.get('full_text', '') if transcript else summary.get('full_text', '')

    # Get entity sentences
    all_mentions = {}
    for c in countries[:8]:
        mentions = extract_entity_sentences(full_text, c)
        if mentions:
            all_mentions[c] = mentions

    wikitext = f"""'''{title}''' is a video in the Predictive History series by Professor Jiang Xueqin, uploaded on {date}.

== Video Information ==

* '''Title:''' {title}
* '''Upload Date:''' {date}
* '''Duration:''' {summary.get('duration', 'N/A')} seconds
* '''YouTube:''' [{url} Link]
* '''Categories:''' {', '.join(categories)}

== Overview ==

{full_text[:1000]}...

== Countries Mentioned ==

"""
    # Per-country sections with context tables
    for country in countries[:8]:
        context = generate_country_context(country)
        mentions = all_mentions.get(country, [])
        wikitext += f"""=== {country} ===

{format_context_table(country, context)}

"""
        if mentions:
            wikitext += f"""'''Analysis by Professor Jiang:'''

"""
            for m in mentions:
                wikitext += f"* \"{m[:300]}...\"\n"
            wikitext += "\n"

    # Predictions section
    wikitext += "== Predictive History Analysis ==\n\n"
    wikitext += "The following predictions and strategic assessments were made in this video:\n\n"

    if predictions:
        for i, pred in enumerate(predictions, 1):
            pred_text = pred['text'][:500]
            wikitext += f"""=== Prediction {i} ===

{''.join(f'"{s.strip()}" ' for s in re.split(r'(?<=[.!?])\s+', pred_text) if s.strip())[:500]}

;Source
: Professor Jiang Xueqin, Predictive History, {pred['date']}

"""
    else:
        wikitext += "//No explicit predictions detected in this transcript.//\n\n"

    wikitext += f"""
== References ==

* [{url} {title}] — Predictive History Channel, {date}

[[Category:Videos|{{PAGENAME}}]]
[[Category:Predictive History|{title}]]
"""
    return wikitext

def push_to_wiki(title, content):
    """Push content to MediaWiki via edit.php."""
    path = '/home/feiteira/.openclaw/workspace/wiki_page_content.txt'
    with open(path, 'w') as f:
        f.write(content)
    cmd = ['php', '/usr/share/mediawiki/maintenance/edit.php',
           '--summary', 'Updated with Predictive History Analysis', title]
    with open(path, 'r') as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    if result.returncode == 0 and 'done' in result.stdout:
        return True, ""
    else:
        return False, result.stderr[:200]

def process_all_videos(batch=10):
    """Process all videos and push to wiki."""
    summaries = load_summaries()
    print(f"Processing {len(summaries)} videos...")

    results = {'success': 0, 'failed': 0, 'skipped': 0}
    for i, summary in enumerate(summaries):
        video_id = summary['id']
        page_title = f"Video:{video_id}"
        date = summary.get('date', 'Unknown')

        # Load transcript
        transcript = load_transcript(video_id)
        if transcript:
            full_text = transcript.get('full_text', '')
        else:
            full_text = summary.get('full_text', '')

        # Extract predictions
        predictions = extract_predictions(full_text, summary['title'], date)

        # Build Wikitext
        wikitext = build_prediction_wikitext(video_id, summary, predictions, transcript)

        # Save locally
        safe_title = video_id.replace('-', '_')
        out_path = os.path.join(OUTPUT_DIR, f'{safe_title}.txt')
        with open(out_path, 'w') as f:
            f.write(wikitext)

        # Push to wiki
        ok, err = push_to_wiki(page_title, wikitext)
        if ok:
            print(f"[{i+1}/{len(summaries)}] ✓ {page_title} ({len(predictions)} predictions)")
            results['success'] += 1
        else:
            print(f"[{i+1}/{len(summaries)}] ✗ {page_title}: {err}")
            results['failed'] += 1

    print(f"\nDone: {results['success']} pushed, {results['failed']} failed")
    return results

if __name__ == '__main__':
    process_all_videos()
