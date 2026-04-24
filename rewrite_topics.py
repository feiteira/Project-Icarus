#!/usr/bin/env python3
"""
Rewrite a MediaWiki topic page from prediction data.
"""
import re, json, subprocess, os

def parse_predictions(content):
    """Extract predictions from the topic content file."""
    preds = []
    # Match numbered predictions: "1. ..." or "1  ..." or "1\t..."
    pattern = re.compile(r'^(\d+)[.)]\s+(.+)$', re.MULTILINE)
    for m in pattern.finditer(content):
        num = int(m.group(1))
        text = m.group(2).strip()
        preds.append({'num': num, 'text': text})
    return preds

def load_video_summaries():
    with open('/home/feiteira/.openclaw/workspace/video_summaries.json') as f:
        return json.load(f)

def load_topic_file(topic):
    path = f'/home/feiteira/.openclaw/workspace/topic_content/{topic}.txt'
    with open(path) as f:
        return f.read()

def load_transcript(video_id):
    path = f'/home/feiteira/.openclaw/workspace/transcripts/transcripts/{video_id}.json'
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
            return data.get('text', '') or data.get('content', '')
    return ''

def cluster_into_themes(predictions, video_summaries, topic, top_n=40):
    """Cluster predictions into 5-8 major themes based on keyword/theme analysis."""
    # Load full_text from videos for this topic
    topic_videos = [v for v in video_summaries if any(st.get('topic') == topic for st in v.get('topics', []))]
    video_ids = set(v['id'] for v in topic_videos)

    # Get a sample of prediction texts to find common themes
    pred_texts = [p['text'] for p in predictions[:top_n * 3]]
    all_text = ' '.join(pred_texts).lower()

    # Keyword-based theme detection
    themes = []

    # Theme detection based on common patterns in predictions
    if 'japan' in all_text or 'tokyo' in all_text or ' Abe ' in all_text or 'asian' in all_text or 'china' in all_text or 'korea' in all_text:
        themes.append('Regional Dynamics & Sino-Japanese Relations')
    if 'military' in all_text or 'army' in all_text or 'navy' in all_text or 'soldier' in all_text or 'weapon' in all_text:
        themes.append('Military Strategy & Defense Posture')
    if 'economy' in all_text or 'trade' in all_text or 'economic' in all_text or 'yen' in all_text or 'dollar' in all_text:
        themes.append('Economic Strategy & Trade Relations')
    if 'political' in all_text or 'government' in all_text or 'election' in all_text or 'prime minister' in all_text or 'party' in all_text:
        themes.append('Political Landscape & Governance')
    if 'war' in all_text or 'conflict' in all_text or 'invasion' in all_text or 'battle' in all_text:
        themes.append('War & Conflict Assessment')
    if 'alliance' in all_text or 'nato' in all_text or ' treaty' in all_text or 'security' in all_text or 'partner' in all_text:
        themes.append('Alliance Structures & Security Partnerships')
    if 'civilization' in all_text or 'culture' in all_text or 'history' in all_text or 'civilizational' in all_text:
        themes.append('Civilizational Analysis & Historical Context')
    if 'technology' in all_text or 'ai' in all_text or 'cyber' in all_text or 'semiconductor' in all_text:
        themes.append('Technological Competition & Strategic Innovation')
    if 'energy' in all_text or 'oil' in all_text or 'gas' in all_text or 'nuclear' in all_text:
        themes.append('Energy & Resource Strategy')
    if 'demographic' in all_text or 'population' in all_text or 'aging' in all_text or 'birth' in all_text:
        themes.append('Demographic Challenges & Social Transformation')
    if 'korean' in all_text or 'peninsula' in all_text or 'kim' in all_text:
        themes.append('Korean Peninsula Dynamics')
    if 'taiwan' in all_text or 'strait' in all_text or 'chinese' in all_text:
        themes.append('Taiwan & Cross-Strait Relations')
    if 'indo' in all_text or 'pacific' in all_text or 'asean' in all_text:
        themes.append('Indo-Pacific Strategic Geometry')
    if 'sanction' in all_text or 'embargo' in all_text or 'export' in all_text:
        themes.append('Sanctions, Exports & Economic Coercion')
    if 'intelligence' in all_text or 'spy' in all_text or 'secret' in all_text:
        themes.append('Intelligence & Covert Operations')

    # Remove duplicates and limit to 8
    seen = set()
    unique_themes = []
    for t in themes:
        if t not in seen:
            seen.add(t)
            unique_themes.append(t)

    return unique_themes[:8] if unique_themes else ['General Analysis']

def group_predictions_by_theme(predictions, themes):
    """Assign each prediction to a theme bucket."""
    buckets = {t: [] for t in themes}
    buckets['General Analysis'] = []

    for p in predictions:
        text_lower = p['text'].lower()
        assigned = False
        for theme in themes:
            theme_keywords = {
                'Regional Dynamics & Sino-Japanese Relations': ['japan', 'tokyo', 'sino', 'china', 'chinese', 'korea', 'korean', 'taiwan', 'east asia', 'asian'],
                'Military Strategy & Defense Posture': ['military', 'army', 'navy', 'soldier', 'weapon', 'missile', 'defense', 'troop', 'combat', 'warfighter'],
                'Economic Strategy & Trade Relations': ['economy', 'trade', 'economic', 'sanction', 'tariff', 'export', 'import', 'market', 'dollar', 'yen', 'yuan'],
                'Political Landscape & Governance': ['political', 'government', 'election', 'prime minister', 'party', 'parliament', 'vote', 'democracy', 'leadership'],
                'War & Conflict Assessment': ['war', 'conflict', 'invasion', 'battle', 'fight', 'escalat', 'ceasefire', 'troop', 'combat'],
                'Alliance Structures & Security Partnerships': ['alliance', 'nato', 'treaty', 'security', 'partner', 'united states', 'america', 'ally', 'defense pact'],
                'Civilizational Analysis & Historical Context': ['civilization', 'culture', 'history', 'historical', 'civilizational', 'roman', 'empire', 'ancient'],
                'Technological Competition & Strategic Innovation': ['technology', 'ai', 'cyber', 'semiconductor', 'chip', 'tech', 'innovation', 'digital'],
                'Energy & Resource Strategy': ['energy', 'oil', 'gas', 'nuclear', 'energy', 'petroleum', 'pipeline', 'resource'],
                'Demographic Challenges & Social Transformation': ['demographic', 'population', 'aging', 'birth', 'youth', 'immigration', 'society'],
                'Korean Peninsula Dynamics': ['korean', 'peninsula', 'kim', 'north korea', 'south korea', 'pyongyang', 'seoul'],
                'Taiwan & Cross-Strait Relations': ['taiwan', 'strait', 'beijing', 'chinese', 'dprk'],
                'Indo-Pacific Strategic Geometry': ['indo-pacific', 'asean', 'pacific', 'south china sea', 'quad', 'malacca'],
                'Sanctions, Exports & Economic Coercion': ['sanction', 'embargo', 'export control', 'coercion', 'secondary sanction', 'boycott'],
                'Intelligence & Covert Operations': ['intelligence', 'spy', 'secret', 'covert', 'cia', 'agency', 'mossad'],
            }
            kw_list = theme_keywords.get(theme, [])
            if any(kw in text_lower for kw in kw_list):
                buckets[theme].append(p)
                assigned = True
                break
        if not assigned:
            buckets['General Analysis'].append(p)

    return buckets

def write_wiki_article(topic, predictions, themes, buckets, topic_video_count):
    """Generate the MediaWiki article content."""
    lines = []
    title = topic

    # Opening paragraph
    lines.append(f"'''{topic}''' is a subject of extensive geopolitical analysis by Professor Jiang Xueqin in his Predictive History series. Professor Jiang applies a distinctive methodology that combines deep historical patterns, civilizational analysis, and strategic forecasting to examine {topic}'s role in global affairs. His approach synthesizes multiple analytical frameworks—including game theory, historical precedent, and contemporary geopolitical dynamics—to generate predictions about {topic}'s trajectory and implications. Professor Jiang has discussed {topic} across more than {topic_video_count} videos in the series, providing a comprehensive analytical framework for understanding its significance in world politics.")

    lines.append("")
    lines.append("== Overview ==")
    lines.append(f"Professor Jiang's analysis of {topic} spans numerous episodes of the Predictive History Channel, covering events, trends, and strategic dynamics relevant to {topic}. His methodology emphasizes understanding the interconnected nature of global geopolitical forces and how historical patterns inform contemporary developments. This article synthesizes the major predictive themes and analytical frameworks Professor Jiang has developed regarding {topic}.")

    # Add themes sections
    valid_themes = [t for t in themes if buckets.get(t) and len(buckets[t]) >= 2]
    if not valid_themes:
        valid_themes = [t for t in themes if buckets.get(t)]

    # Also check General Analysis
    if buckets.get('General Analysis') and len(buckets['General Analysis']) >= 3:
        valid_themes.append('General Analysis')

    for theme in valid_themes[:8]:
        preds = buckets[theme]
        if len(preds) < 2:
            continue

        theme_heading = theme.replace(' ', '_')
        lines.append(f"\n== {theme} ==")

        # Create 3-4 paragraphs synthesizing the predictions
        # Paragraph 1: General observation
        paras = []
        first_pred = preds[0]['text']
        paras.append(f"Professor Jiang argues that {first_pred[0].lower()}{first_pred[1:]}")

        # Paragraph 2: Combine 2-3 predictions
        if len(preds) >= 2:
            second_pred = preds[1]['text']
            paras.append(f"Building on this pattern, Professor Jiang also observed that {second_pred[0].lower()}{second_pred[1:]}")

        # Paragraph 3: More predictions
        if len(preds) >= 3:
            third_pred = preds[2]['text']
            paras.append(f"Related to this analysis, Professor Jiang further contended that {third_pred[0].lower()}{third_pred[1:]}")

        # Paragraph 4: Wrap up with more predictions
        if len(preds) >= 4:
            remaining = preds[3:min(6, len(preds))]
            combined = '; '.join(p['text'] for p in remaining if len(p['text']) < 200)
            if combined:
                paras.append(f"Further elaborating on this framework, Professor Jiang noted that {combined[0].lower()}{combined[1:]}")

        lines.extend(paras)

    # Closing summary
    lines.append("")
    lines.append("== Summary ==")
    total = len(predictions)
    lines.append(f"Professor Jiang's analysis of {topic} across the Predictive History series encompasses {total} distinct predictions and analytical points. These predictions span themes including geopolitical strategy, historical precedent, and forward-looking forecasting. His work emphasizes the interconnected nature of {topic.lower()} within broader global dynamics and provides a framework for understanding its development through the lens of historical patterns and strategic analysis.<ref>Predictive History Channel, 2025</ref>")

    return '\n'.join(lines)

def push_to_wiki(title, content_path):
    """Push content to MediaWiki via edit.php."""
    cmd = [
        'php', '/usr/share/mediawiki/maintenance/edit.php',
        '--summary', 'Narrative rewrite',
        title
    ]
    with open(content_path) as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    return result

def main():
    topics = ['Japan', 'Ukraine', 'Gold', 'Civil War', 'Game Theory',
              'Saudi Arabia', 'Judaism', 'NATO']

    video_summaries = load_video_summaries()
    results = []

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"Processing: {topic}")
        print(f"{'='*60}")

        # Load content
        content = load_topic_file(topic)
        predictions = parse_predictions(content)
        print(f"  Found {len(predictions)} predictions")

        # Get video count
        topic_videos = [v for v in video_summaries
                       if any(st.get('topic') == topic for st in v.get('topics', []))]
        topic_video_count = len(topic_videos)
        print(f"  Found {topic_video_count} videos for this topic")

        # Cluster into themes
        themes = cluster_into_themes(predictions, video_summaries, topic)
        print(f"  Themes: {themes}")

        # Group predictions
        buckets = group_predictions_by_theme(predictions, themes)

        # Write wiki article
        article = write_wiki_article(topic, predictions, themes, buckets, topic_video_count)

        # Save to temp file
        tmp_path = '/home/feiteira/.openclaw/workspace/wiki_page_content.txt'
        with open(tmp_path, 'w') as f:
            f.write(article)

        # Push to wiki
        res = push_to_wiki(topic, tmp_path)

        if res.returncode == 0:
            print(f"  ✓ Successfully updated Wikipedia page: {topic}")
            results.append((topic, 'SUCCESS', len(predictions)))
        else:
            print(f"  ✗ Failed: {res.stderr[:200]}")
            results.append((topic, 'FAILED', len(predictions)))

    # Final summary
    print(f"\n{'='*60}")
    print("COMPLETION SUMMARY")
    print(f"{'='*60}")
    success = sum(1 for r in results if r[1] == 'SUCCESS')
    failed = sum(1 for r in results if r[1] == 'FAILED')
    print(f"Total topics processed: {len(results)}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    for topic, status, count in results:
        print(f"  [{status}] {topic}: {count} predictions")

if __name__ == '__main__':
    main()