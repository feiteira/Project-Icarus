#!/usr/bin/env python3
import json
import sys
import subprocess
from collections import defaultdict

# Load video summaries
with open('/home/feiteira/.openclaw/workspace/video_summaries.json') as f:
    videos = json.load(f)

# Collect topics and their video references
topic_data = defaultdict(list)
for video in videos:
    video_id = video['id']
    video_title = video['title']
    video_url = video.get('url', f'https://youtube.com/watch?v={video_id}')
    video_date = video.get('date', 'Unknown')
    
    for topic_info in video.get('topics', []):
        topic = topic_info['topic']
        mention = topic_info.get('first_mention') or {}
        timestamp = mention.get('start', 0) if isinstance(mention, dict) else 0
        text = mention.get('text', '') if isinstance(mention, dict) else ''
        
        topic_data[topic].append({
            'video_id': video_id,
            'title': video_title,
            'url': video_url,
            'date': video_date,
            'timestamp': timestamp,
            'text': text
        })

def generate_topic_page(topic, references):
    references.sort(key=lambda x: x['date'], reverse=True)
    video_count = len(set(r['video_id'] for r in references))
    
    content = """'''{topic}''' is a topic extensively analyzed by Professor Jiang Xueqin in his Predictive History series. Professor Jiang brings unique geopolitical insights, combining deep historical analysis with contemporary strategic forecasting.

== Overview ==

Professor Jiang has discussed {topic} in {video_count} videos, providing analysis that connects historical patterns to current events and future predictions. His approach synthesizes multiple civilizational perspectives, emphasizing the interconnected nature of global geopolitical forces.

""".format(topic=topic, video_count=video_count)

    content += "== Key Analysis ==\n\n"
    
    for ref in references[:10]:
        minutes = int(ref['timestamp'] // 60)
        seconds = int(ref['timestamp'] % 60)
        text_snippet = ref['text'][:200] if len(ref['text']) > 200 else ref['text']
        content += '* "{text}"... — [{url} {title}], {date} (at {mins}:{secs:02d})\n\n'.format(
            text=text_snippet, url=ref['url'], title=ref['title'], 
            date=ref['date'], mins=minutes, secs=seconds)
    
    content += "\n== Video References ==\n\n"
    seen = set()
    for ref in references:
        key = (ref['video_id'], ref['title'], ref['url'], ref['date'])
        if key not in seen:
            seen.add(key)
            content += "* [{url} {title}] — {date}\n".format(url=ref['url'], title=ref['title'], date=ref['date'])
    
    content += """
[[Category:Topics|{{PAGENAME}}]]
"""
    return content

def create_page(title, content):
    with open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt', 'w') as f:
        f.write(content)
    
    cmd = ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Created page with PredictiveHistory content', title]
    with open('/tmp/wiki_page_content.txt', 'r') as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    
    if result.returncode == 0 and 'done' in result.stdout:
        print("Created: {title}".format(title=title))
        return True
    else:
        print("Failed: {title} - {err}".format(title=title, err=result.stderr[:200] if result.stderr else result.stdout[:200]))
        return False

print("Found {count} topics".format(count=len(topic_data)))
created = 0
for topic in sorted(topic_data.keys()):
    content = generate_topic_page(topic, topic_data[topic])
    if create_page(topic, content):
        created += 1


print("Created {count} pages".format(count=created))
