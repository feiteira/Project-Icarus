#!/usr/bin/env python3
"""
For each video in the batch, post a discussion comment to each relevant topic's Talk page.
Usage: python3 post_discussion_comments.py <batch_number>
"""
import json
import subprocess
import sys
import os
import re
import urllib.request
import urllib.parse

BATCH_NUM = sys.argv[1] if len(sys.argv) > 1 else "1"
BATCH_FILE = f"/home/feiteira/.openclaw/workspace/video_batch_{BATCH_NUM}.json"
CONTENT_FILE = "/home/feiteira/.openclaw/workspace/wiki_page_content.txt"
EDIT_PHP = "/usr/share/mediawiki/maintenance/edit.php"
API_URL = "https://localhost/api.php"

# Valid topic page names
VALID_TOPICS = {
    "War", "Empire", "China", "Europe", "United States", "Israel", "Middle East",
    "Russia", "Iran", "Civilization", "Strategy", "Islam", "Christianity", "Nuclear",
    "India", "Japan", "Ukraine", "Gold", "Civil War", "Game Theory", "Saudi Arabia",
    "Judaism", "NATO", "Taiwan", "Roman Empire", "Cold War", "Holy Roman Empire",
    "Democracy", "Constitution", "Geopolitics", "Bitcoin", "BRICS", "Federal Reserve",
    "Silk Road", "South China Sea", "Woke", "Collapse", "Trump", "NeoCon", "Secession",
    "World Economic Forum"
}

def api_get_title(title):
    """Fetch current wikitext of a page via API"""
    try:
        params = urllib.parse.urlencode({
            'action': 'parse',
            'page': title,
            'prop': 'wikitext',
            'format': 'json'
        })
        req = urllib.request.Request(f"{API_URL}?{params}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if 'parse' in data:
                return data['parse']['wikitext']['*']
    except Exception as e:
        pass
    return ""

def post_to_talk_page(topic, video_id, video_title, video_date, excerpt, analysis):
    """Append a discussion comment to the Talk:<topic> page via read+write"""
    # Clean up analysis
    analysis = re.sub(r'\s+', ' ', analysis).strip()
    
    # Format the new section
    section = f"""

=== [[Video:{video_id}|{video_title}]] ===

'''Date:''' {video_date}
'''Excerpt:''' "{excerpt[:200]}"

{analysis}

-- [[User:PredictiveHistoryBot|PredictiveHistoryBot]] ~~~~
"""
    
    talk_page = f"Talk:{topic}"
    
    # Fetch existing content
    existing = api_get_title(talk_page)
    
    # Append the new section
    updated = existing + section
    
    # Write to file
    with open(CONTENT_FILE, 'w') as f:
        f.write(updated)
    
    # Write via edit.php
    cmd = [
        "php", EDIT_PHP,
        "--summary", f"Adding video commentary: {video_title}",
        talk_page
    ]
    
    try:
        result = subprocess.run(
            cmd,
            stdin=open(CONTENT_FILE),
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "OK"
        else:
            err = (result.stderr or result.stdout or "")[:200]
            return False, err
    except Exception as e:
        return False, str(e)

def main():
    with open(BATCH_FILE) as f:
        videos = json.load(f)
    
    print(f"Batch {BATCH_NUM}: Processing {len(videos)} videos")
    
    total_posts = 0
    for video in videos:
        video_id = video["id"]
        video_title = video["title"]
        video_date = video.get("date", "Unknown date")
        topics = video.get("topics", [])
        
        if not topics:
            print(f"  [{video_id}] No topics, skipping")
            continue
        
        for topic_entry in topics:
            topic_name = topic_entry.get("topic", "")
            
            if topic_name not in VALID_TOPICS:
                continue
            
            # Handle None first_mention
            if topic_entry.get("first_mention") is None:
                excerpt = ""
                start_time = 0
            else:
                first_mention = topic_entry.get("first_mention", {})
                excerpt = first_mention.get("text", "")[:300]
                start_time = first_mention.get("start", 0)
            
            full_text = video.get("full_text", "") or ""
            
            # Build context around excerpt
            if excerpt and start_time > 0 and len(full_text) > 100:
                idx = full_text.find(excerpt[:50]) if excerpt else -1
                if idx > 0:
                    context_start = max(0, idx - 150)
                    context_end = min(len(full_text), idx + 250)
                    context = full_text[context_start:context_end]
                else:
                    context = full_text[:500]
            else:
                context = full_text[:500] if full_text else ""
            
            # Clean filler
            context_clean = re.sub(r'\b(um|uh|like|you know|I mean|sort of|kind of)\b', '', context, flags=re.IGNORECASE)
            context_clean = re.sub(r'\s+', ' ', context_clean).strip()
            
            # Build analysis
            analysis = f"""Professor Jiang discusses {topic_name} in the context of the broader predictive framework for this period. He grounds his predictions in historical patterns, examining how {topic_name.lower()} relates to broader civilizational, strategic, and geopolitical trajectories. The analysis draws on established historical precedents to forecast likely developments in the coming years."""

            if context_clean:
                analysis += f"""

From the video: "{context_clean[:300]}..."
"""
            
            ok, msg = post_to_talk_page(
                topic_name,
                video_id,
                video_title,
                video_date,
                excerpt,
                analysis
            )
            
            if ok:
                total_posts += 1
                print(f"  [{video_id}] → Talk:{topic_name}: OK")
            else:
                print(f"  [{video_id}] → Talk:{topic_name}: FAIL ({str(msg)[:100]})")
    
    print(f"\nBatch {BATCH_NUM} complete: {total_posts} discussion comments posted")

if __name__ == "__main__":
    main()
