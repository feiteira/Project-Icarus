#!/usr/bin/env python3
"""Test if <references/> works without Cite extension."""
import subprocess, json

test_page = 'TestRefPage'
test_content = """'''Test Reference Page'''

This is a test with two references.<ref>First source</ref> And another.<ref>Second source</ref>

== References ==

<references/>

[[Category:test]]
"""

# Push test page
with open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt', 'w') as f:
    f.write(test_content)
r = subprocess.run(
    ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Testing references', test_page],
    stdin=open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt'),
    capture_output=True, text=True
)
print("Push:", r.returncode, r.stdout[-100:] if r.stdout else '')

# Check wikitext
r2 = subprocess.run(['curl', '-sk', 'https://localhost/api.php?action=parse&page=TestRefPage&prop=wikitext&format=json'], capture_output=True, text=True)
d = json.loads(r2.stdout)
wt = d['parse']['wikitext']['*']
print("Wikitext <ref>:", wt.count('<ref>'))
print("Wikitext <references/>:", wt.count('<references/>'))

# Check rendered
r3 = subprocess.run(['curl', '-sk', 'https://localhost/api.php?action=parse&page=TestRefPage&prop=text&format=json'], capture_output=True, text=True)
d3 = json.loads(r3.stdout)
html = d3['parse']['text']['*']
print("HTML <ref count:", html.count('<ref'))
print("First source in HTML:", 'First source' in html)
idx = html.find('First source')
if idx >= 0:
    print("Found it!")
else:
    idx2 = html.find('>reference<')
    print("Around ref tag:", html[max(0,idx2-50):idx2+150] if idx2 >= 0 else 'Not found')
