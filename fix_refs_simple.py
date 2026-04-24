#!/usr/bin/env python3
"""Fix references by using a simple Sources section instead of <ref> tags."""
import subprocess, json, urllib.parse, re

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

ok = 0
for topic in topics:
    encoded = urllib.parse.quote(topic)
    r = subprocess.run(['curl', '-sk', f'https://localhost/api.php?action=parse&page={encoded}&prop=wikitext&format=json'], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        wt = d['parse']['wikitext']['*']
    except:
        continue

    # Replace <ref>...</ref> with citation number inline
    ref_map = {}
    ref_list = []
    counter = [0]

    def repl(m):
        content = m.group(1).strip()
        if content not in ref_map:
            counter[0] += 1
            ref_map[content] = counter[0]
            ref_list.append(content)
        return f'[{ref_map[content]}]'

    new_wt = re.sub(r'<ref>([^<]+)</ref>', repl, wt)

    # Remove old refs section and related markup
    new_wt = re.sub(r'==\s*References\s*==.*?(?====\s|$)', '', new_wt, flags=re.DOTALL)
    new_wt = re.sub(r'<references\s*/?>', '', new_wt)
    new_wt = re.sub(r'\{\{Refbegin\}\}.*?\{\{Refend\}\}', '', new_wt, flags=re.DOTALL)

    # Build sources section
    if ref_list:
        sources = []
        for i, ref in enumerate(ref_list, 1):
            year = re.search(r'(20\d\d)', ref)
            yr = year.group(1) if year else 'n.d.'
            sources.append(f'{i}. {ref} (''Predictive History Channel, {yr}'')')

        src_block = '\n\n== Sources ==\n' + '\n'.join(sources) + '\n\n'
        new_wt = re.sub(r'(\[\[Category:)', src_block + r'\1', new_wt)

    with open('/tmp/wiki_fix.txt', 'w') as f:
        f.write(new_wt)
    r2 = subprocess.run(
        ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Replaced with simple numbered sources section', topic],
        stdin=open('/tmp/wiki_fix.txt'),
        capture_output=True, text=True
    )
    if r2.returncode == 0 and 'done' in r2.stdout:
        ok += 1
    else:
        print(f'FAIL: {topic}: {r2.stderr[:60]}')

print(f'Done: {ok}/41')
