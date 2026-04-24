import subprocess, json, urllib.parse, re

API = "https://localhost/api.php"

def get_page(title):
    params = {"action": "parse", "page": title, "prop": "wikitext", "format": "json"}
    query = "?" + urllib.parse.urlencode(params)
    result = subprocess.run(["curl", "-skL", API + query], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)["parse"]["wikitext"]["*"]
    except:
        return None

def save_page(title, content, summary):
    with open("/tmp/wiki_page_content.txt", "w") as f:
        f.write(content)
    result = subprocess.run(
        ["php", "/usr/share/mediawiki/maintenance/edit.php", "--summary", summary, title],
        stdin=open("/tmp/wiki_page_content.txt", "r"),
        capture_output=True, text=True
    )
    return result

# Try to fix Cold War specifically - first read and print what we get
print("=== Getting Cold War ===")
wt = get_page("Cold War")
print(f"Content length: {len(wt) if wt else 0}")
print(f"Starts with redirect: {wt.startswith('#REDIRECT') if wt else 'None'}")
print(f"Has class=infobox: {'class=\"infobox\"' in wt if wt else False}")
print(f"Has Quick Facts: {'Quick Facts' in wt if wt else False}")
print(f"Has cold_war.png: {'cold_war.png' in wt if wt else False}")
print(f"First 500 chars: {wt[:500] if wt else 'None'}")

print("\n=== Building new content ===")
TRIVIA_COLD = {"Period": "1947-1991", "Parties": "United States vs Soviet Union", "End": "Dissolution of USSR (Dec 1991)"}
lines = wt.split('\n')

# Find title
title_idx = -1
for i, line in enumerate(lines):
    if line.strip().startswith("'''"):
        title_idx = i
        break

if title_idx >= 0:
    title_line = lines[title_idx].strip()
else:
    title_line = "'''Cold War'''"

# Body start
body_start = title_idx + 1
while body_start < len(lines):
    l = lines[body_start].strip()
    if l and not l.startswith('[['):
        break
    body_start += 1

body = '\n'.join(lines[body_start:])
body = body.lstrip('\n')
# Remove duplicate image lines
body_lines = []
for line in body.split('\n'):
    if 'cold_war.png' not in line:
        body_lines.append(line)
body = '\n'.join(body_lines)
body = re.sub(r'\n{3,}', '\n\n', body).strip('\n')

# Build infobox
img = "[[File:cold_war.png|thumb|right|280px]]\n"
table = '{| class="infobox" style="float:right; margin:0 0 1em 1em; font-size:90%; width:280px; border-collapse:collapse;"\n'
table += '|+ Quick Facts\n'
table += '! colspan="2" style="background:#f0f0f0; text-align:center; font-size:1.1em;" | Cold War\n'
for label, value in TRIVIA_COLD.items():
    table += '| ' + label + '\n| ' + value + '\n'
table += '|}\n'

infobox = img + '\n' + table + '\n'
new_content = title_line + '\n\n' + infobox + body

print(f"New content length: {len(new_content)}")
print(f"Has class=infobox: {'class=\"infobox\"' in new_content}")
print(f"First 300: {new_content[:300]}")

# Write to file first to verify
with open("/tmp/wiki_test_coldwar.txt", "w") as f:
    f.write(new_content)
print("Written to /tmp/wiki_test_coldwar.txt")

# Now try to save
print("\n=== Saving ===")
result = save_page("Cold War", new_content, "Fix infobox: Wikipedia-style float right, class=infobox")
print("STDOUT:", result.stdout[:200])
print("STDERR:", result.stderr[:200])