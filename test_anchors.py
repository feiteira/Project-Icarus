#!/usr/bin/env python3
"""Test different reference approaches on this MW install."""
import subprocess

content = """'''Test References'''

Some text with a reference[[#ref1|<sup>1</sup>]] and another[[#ref2|<sup>2</sup>]].

== References ==

<div id="ref1">1. [[Predictive History]] YouTube channel by [[Professor Jiang Xueqin]], 2025 (First source)</div>

<div id="ref2">2. [[Predictive History]] YouTube channel by [[Professor Jiang Xueqin]], 2025 (Second source)</div>

[[Category:test]]
"""

with open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt', 'w') as f:
    f.write(content)
r = subprocess.run(
    ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Test anchor refs', 'TestAnchors'],
    stdin=open('/home/feiteira/.openclaw/workspace/wiki_page_content.txt'),
    capture_output=True, text=True
)
print("Push:", r.returncode)

# Check rendered
r2 = subprocess.run(['curl', '-sk', 'https://localhost/api.php?action=parse&page=TestAnchors&prop=text&format=json'], capture_output=True, text=True)
import json
d = json.loads(r2.stdout)
html = d['parse']['text']['*']
# Show the relevant part
idx = html.find('ref1')
print("Around ref1:", html[max(0,idx-100):idx+200])
