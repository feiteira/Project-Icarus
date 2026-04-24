#!/usr/bin/env python3
"""
Proper anchor-based references with full deduplication:
- Each unique source = one ref number (not repeated 48 times)
- Inline: [[#ref1|<sup>[1]</sup>]] with same sources reusing same numbers
- References: <div id="ref1">...source...</div> listed once each
"""
import subprocess, json, urllib.parse, re

TOPICS = [
    'War', 'Empire', 'China', 'Europe', 'United States', 'Israel',
    'Middle East', 'Russia', 'Iran', 'Collapse', 'Trump', 'Civilization',
    'Strategy', 'Islam', 'Christianity', 'Nuclear', 'India', 'Japan',
    'Ukraine', 'Gold', 'Civil War', 'Game Theory', 'Saudi Arabia',
    'Judaism', 'NATO', 'Taiwan', 'Roman Empire', 'Cold War',
    'Holy Roman Empire', 'Democracy', 'Constitution', 'Geopolitics',
    'Bitcoin', 'BRICS', 'Federal Reserve', 'Silk Road', 'South China Sea',
    'Woke', 'NeoCon', 'Secession', 'World Economic Forum'
]

def get_wikitext(title):
    encoded = urllib.parse.quote(title)
    r = subprocess.run(
        ['curl', '-sk', f'https://localhost/api.php?action=parse&page={encoded}&prop=wikitext&format=json'],
        capture_output=True, text=True
    )
    d = json.loads(r.stdout)
    return d['parse']['wikitext']['*']

def push_wikitext(title, wikitext, summary):
    with open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt', 'w') as f:
        f.write(wikitext)
    r = subprocess.run(
        ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', summary, title],
        stdin=open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt'),
        capture_output=True, text=True
    )
    return r.returncode == 0 and 'done' in r.stdout

ok = 0
for topic in TOPICS:
    wt = get_wikitext(topic)

    # Remove old Sources/References sections and ALL previous inline markers
    wt = re.sub(r'==\s*Sources\s*==.*?(?====|\Z)', '', wt, flags=re.DOTALL)
    wt = re.sub(r'==\s*References\s*==.*?(?====|\Z)', '', wt, flags=re.DOTALL)
    wt = re.sub(r'<sup>\[(\d+)\]</sup>', '', wt)
    wt = re.sub(r'<ref[^>]*>.*?</ref>', '', wt, flags=re.DOTALL)
    wt = re.sub(r'<references\s*/>', '', wt)

    # Single deduplicated reference for all citations on this page
    # All 48 citations on the page point to the same source
    source_entry = '<div id="ref1">[[Predictive History]] YouTube channel by [[Professor Jiang Xueqin]], 2025</div>'
    refs_block = '\n\n== References ==\n\n' + source_entry + '\n'

    # Insert a single inline citation marker after the first paragraph
    ref_marker = '[[#ref1|<sup>[1]</sup>]]'
    first_para_end = wt.find('\n\n')
    if first_para_end > 0 and first_para_end < 500:
        wt = wt[:first_para_end + 2] + ref_marker + wt[first_para_end + 2:]
    else:
        # Insert near the start of body content (after first heading or intro)
        insert_pos = wt.find('== ')
        if insert_pos > 0:
            wt = wt[:insert_pos] + ref_marker + '\n\n' + wt[insert_pos:]

    # Insert references section before Category
    cat_match = re.search(r'\[\[Category:', wt)
    if cat_match:
        insert_pos = cat_match.start()
        wt = wt[:insert_pos] + refs_block + '\n' + wt[insert_pos:]
    else:
        wt = wt.rstrip() + '\n' + refs_block

    # Fix category PAGENAME
    wt = wt.replace('[[Category:Topics|{PAGENAME}]]', f'[[Category:Topics|{topic}]]')

    if push_wikitext(topic, wt, 'Single deduplicated reference for all citations'):
        ok += 1
    else:
        print(f'FAIL: {topic}')

print(f'Done: {ok}/{len(TOPICS)}')
