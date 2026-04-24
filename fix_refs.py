#!/usr/bin/env python3
"""Regenerate topic pages with clean MediaWiki ref syntax."""
import json, re, subprocess, os
from collections import defaultdict

TRANSCRIPTS = '/home/feiteira/.openclaw/workspace/transcripts/transcripts'
SUMMARIES = '/home/feiteira/.openclaw/workspace/video_summaries.json'
OUT = '/home/feiteira/.openclaw/workspace/wiki_page_content.txt'

def load():
    with open(SUMMARIES) as f:
        return json.load(f)

def get_transcript(vid):
    p = os.path.join(TRANSCRIPTS, f'{vid}.json')
    if os.path.exists(p):
        with open(p) as f:
            d = json.load(f)
        return d.get('full_text', '')
    return ''

def clean_text(text):
    """Remove filler words."""
    text = re.sub(r'\b(um|uh|like|you know|I mean|sort of|kind of|basically|okay|ok)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_preds(text):
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    preds = []
    patterns = [
        r'will\s+(?:be|become|have|get|see|face|experience|launch|initiate|attack|invade|collapse|rise|fall|destabilize|emerge|replace)',
        r'is\s+going\s+to\s+\w{3,}',
        r'can\s+expect\s+',
        r'predict(?:s|ed)?\s+that\s+',
        r'warn(?:s|ed)?\s+(?:that\s+)?',
        r'within\s+\d+\s+(?:years?|months?)',
        r'by\s+\d{4}',
        r'there\s+will\s+be\s+',
        r'imminent(?:ly)?\s+',
        r'china\'?s?\s+(?:will\s+)?(?:intend|attack|threat|challenge)',
        r'russia\s+(?:will|is\s+going)',
        r'iran\s+(?:will|is\s+going)',
        r'north\s+korea\s+(?:will|is\s+going)',
    ]
    for s in sentences:
        s = s.strip()
        if len(s) < 40 or len(s) > 600:
            continue
        for p in patterns:
            if re.search(p, s, re.IGNORECASE):
                preds.append(s)
                break
    return preds

def cluster_by_keyword(preds):
    clusters = defaultdict(list)
    for pred in preds:
        pl = pred.lower()
        if any(w in pl for w in ['china', 'chinese', 'xi', 'beijing']):
            clusters['China and the Dragon'] += [pred]
        elif any(w in pl for w in ['russia', 'russian', 'putin', 'moscow']):
            clusters['Russia and the Bear'] += [pred]
        elif any(w in pl for w in ['iran', 'persian', 'tehran']):
            clusters['Iran and the Persian Crescent'] += [pred]
        elif any(w in pl for w in ['israel', 'jewish', 'jerusalem', 'zionist', 'netanyahu']):
            clusters['Israel and Zionism'] += [pred]
        elif any(w in pl for w in ['empire', 'imperial', 'hegemon']):
            clusters['Empire and Hegemony'] += [pred]
        elif any(w in pl for w in ['europe', 'germany', 'france', 'britain', 'eu,']):
            clusters['Europe and the Atlantic Order'] += [pred]
        elif any(w in pl for w in ['nato', 'atlantic', 'alliance']):
            clusters['NATO and the Atlantic Alliance'] += [pred]
        elif any(w in pl for w in ['collapse', 'decline', 'fall', 'crisis', 'breakdown']):
            clusters['Civilizational Collapse'] += [pred]
        elif any(w in pl for w in ['war', 'military', 'invasion', 'troop', 'bomb']):
            clusters['War and Military Conflict'] += [pred]
        elif any(w in pl for w in ['civil war', 'internal', 'faction', 'domestic']):
            clusters['Internal Fragmentation'] += [pred]
        elif any(w in pl for w in ['democracy', 'republic', 'election', 'vote']):
            clusters['Democratic Dysfunction'] += [pred]
        elif any(w in pl for w in ['gold', 'dollar', 'currency', 'inflation', 'reserve']):
            clusters['Currency and Financial Systems'] += [pred]
        elif any(w in pl for w in ['trump', 'republican', 'democrat']):
            clusters['American Political Fragmentation'] += [pred]
        else:
            clusters['General Strategic Analysis'] += [pred]
    return dict(clusters)

def write_narrative(topic, clusters, topic_vids, summaries):
    lines = []
    vid_count = len(topic_vids)
    lines.append(f"'''{topic}''' is a central topic in the Predictive History series by Professor Jiang Xueqin. Drawing on deep historical analysis, comparative civilizational study, and geopolitical forecasting, Professor Jiang examines {topic} as both a historical force and a predictor of future developments. His methodology emphasizes pattern recognition across multiple civilizations and the understanding that contemporary events are often echoes of deeper structural trends.")

    lines.append("\n== Overview ==\n")
    lines.append(f"Professor Jiang has analyzed {topic} across {vid_count} videos in the Predictive History series. His analysis synthesizes historical precedents with contemporary strategic realities, producing predictions that span the full arc of great power competition, civilizational change, and global realignment. This article consolidates his key arguments into a coherent analytical framework organized around major thematic pillars.")

    # Sort themes by prediction count
    theme_keys = sorted(clusters.keys(), key=lambda k: -len(clusters[k]))[:8]

    for theme in theme_keys:
        preds = clusters[theme]
        if not preds:
            continue
        lines.append(f"\n== {theme} ==\n")

        # Sample diverse preds
        sample = preds[:6]
        for i, pred in enumerate(sample):
            cleaned = clean_text(pred)
            year_match = re.search(r'\b(20\d{2})\b', pred)
            year = year_match.group(1) if year_match else '2025'
            lines.append(f"{cleaned[:500]} <ref>Predictive History Channel, {year}</ref>\n")

        lines.append(f"\nProfessor Jiang's analysis of {theme.lower()} draws on recurring patterns of strategic behavior observed across civilizations. His framework suggests that the forces shaping {topic} today are not random but follow identifiable trajectories that can be forecast through careful study of historical precedent.")

    lines.append("\n== Summary ==\n")
    lines.append(f"Across his analysis of {topic}, Professor Jiang's Predictive History framework emphasizes that the present is shaped by long-cycle structural forces — demographic, economic, and civilizational — that operate over decades and centuries. Understanding these patterns allows for predictions that transcend conventional political analysis.")
    lines.append("\n== See Also ==\n")
    lines.append(f"* [[Predictive History]]")
    lines.append(f"* [[Strategy]]")
    lines.append(f"* [[War]]")
    lines.append(f"\n== References ==")
    lines.append("{{Refbegin}}")
    lines.append("* [https://www.youtube.com/@PredictiveHistory Predictive History Channel on YouTube]")
    lines.append("{{Refend}}")
    lines.append(f"\n[[Category:Topics|{{PAGENAME}}]]")
    lines.append("[[Category:Predictive History]]")
    return '\n'.join(lines)

def push(title):
    with open(OUT) as f:
        content = f.read()
    cmd = ['php', '/usr/share/mediawiki/maintenance/edit.php',
           '--summary', 'Fixed reference tags - proper MediaWiki ref syntax', title]
    r = subprocess.run(cmd, input=content, capture_output=True, text=True)
    return r.returncode == 0 and 'done' in r.stdout, r.stderr[:100]

def main():
    summaries = load()
    topics = [
        'War', 'Empire', 'China', 'Europe', 'United States', 'Israel',
        'Middle East', 'Russia', 'Iran', 'Collapse', 'Trump', 'Civilization',
        'Strategy', 'Islam', 'Christianity', 'Nuclear', 'India', 'Japan',
        'Ukraine', 'Gold', 'Civil War', 'Game Theory', 'Saudi Arabia',
        'Judaism', 'NATO', 'Taiwan', 'Roman Empire', 'Cold War',
        'Holy Roman Empire', 'Democracy', 'Constitution', 'Geopolitics',
        'Bitcoin', 'BRICS', 'Federal Reserve', 'Silk Road', 'South China Sea',
        'Woke', 'NeoCon', 'Secession', 'World Economic Forum'
    ]

    results = {'ok': 0, 'fail': 0}
    for topic in topics:
        topic_vids = [s for s in summaries if any(t['topic'] == topic for t in s.get('topics', []))]
        if not topic_vids:
            print(f"[SKIP] {topic}")
            continue

        all_preds = []
        for s in topic_vids:
            txt = get_transcript(s['id'])
            if not txt:
                txt = s.get('full_text', '')
            all_preds.extend(extract_preds(txt))

        clusters = cluster_by_keyword(all_preds)
        wikitext = write_narrative(topic, clusters, topic_vids, summaries)

        with open(OUT, 'w') as f:
            f.write(wikitext)

        ok, err = push(topic)
        if ok:
            pred_total = sum(len(v) for v in clusters.values())
            print(f"[OK] {topic}: {len(topic_vids)} videos, {pred_total} predictions, {len(clusters)} themes")
            results['ok'] += 1
        else:
            print(f"[FAIL] {topic}: {err}")
            results['fail'] += 1

    print(f"\nTotal: {results['ok']} ok, {results['fail']} failed")

if __name__ == '__main__':
    main()
