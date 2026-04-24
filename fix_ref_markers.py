#!/usr/bin/env python3
"""Fix inline ref markers to have proper newlines."""
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

ok = 0
for topic in TOPICS:
    encoded = urllib.parse.quote(topic)
    r = subprocess.run(['curl', '-sk', f'https://localhost/api.php?action=parse&page={encoded}&prop=wikitext&format=json'], capture_output=True, text=True)
    d = json.loads(r.stdout)
    wt = d['parse']['wikitext']['*']

    # Fix: replace marker immediately before == with marker\n\n
    # Pattern: [[#ref1|<sup>[1]</sup>]]== some_heading ==
    fixed = re.sub(r'(\[\[#ref1\|\<sup\>\[1\]\<\/sup\>\]\])(\=\= )', r'\1\n\n\2', wt)

    with open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt', 'w') as f:
        f.write(fixed)
    r2 = subprocess.run(
        ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Fixed ref marker spacing', topic],
        stdin=open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt'),
        capture_output=True, text=True
    )
    if r2.returncode == 0 and 'done' in r2.stdout:
        ok += 1
    else:
        print(f'FAIL: {topic}')

print(f'Done: {ok}/{len(TOPICS)}')
