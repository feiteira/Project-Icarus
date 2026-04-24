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
        stdin=open("/tmp/wiki_page_content.txt"),
        capture_output=True, text=True
    )
    print("  result:", result.stdout.strip()[:100])
    return "done" in result.stdout.lower()

def fix_page(wiki_title, topic_key, image_file):
    content = get_page(wiki_title)
    if content is None:
        print("  cannot fetch")
        return False
    if content.startswith("#REDIRECT"):
        print("  is redirect")
        return False

    lines = content.split('\n')

    # Try to find title line
    title_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("'''") and title_idx < 0:
            title_idx = i
            break

    if title_idx >= 0:
        title_line = lines[title_idx].strip()
    else:
        # No title line found - use the page name as title
        title_line = "'''" + wiki_title + "'''"
        title_idx = -1  # will insert at position 0

    # Body start: skip blank lines and [[File: lines after the title
    if title_idx >= 0:
        body_start = title_idx + 1
    else:
        body_start = 0

    while body_start < len(lines):
        l = lines[body_start].strip()
        if l and not l.startswith('[['):
            break
        body_start += 1

    body = '\n'.join(lines[body_start:])
    body = body.lstrip('\n')

    # Remove duplicate [[File: lines from body
    body_lines = []
    for line in body.split('\n'):
        if re.match(r'\[\[File:.*\.png\|thumb\|right\|280px\]\]', line.strip()):
            continue
        body_lines.append(line)
    body = '\n'.join(body_lines)
    body = re.sub(r'\n{3,}', '\n\n', body).strip('\n')

    # Build infobox
    img = "[[File:" + image_file + "|thumb|right|280px]]\n"

    trivia_map = {
        "United States": {"Population": "~335 million", "Area": "9.8M km2", "GDP": "$27T (nominal)", "Capital": "Washington D.C."},
        "Saudi Arabia": {"Population": "~36 million", "Area": "2.1M km2", "GDP": "$1.1T (nominal)", "Capital": "Riyadh"},
        "Cold War": {"Period": "1947-1991", "Parties": "United States vs Soviet Union", "End": "Dissolution of USSR (Dec 1991)"},
        "Roman Empire": {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
        "Holy Roman Empire": {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
        "Federal Reserve": {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance Sheet": "~$7.5T (2024)"},
        "World Economic Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
        "Game Theory": {"Origin": "John von Neumann, 1928", "Key Concept": "Nash equilibrium", "Applications": "Economics, military, politics"},
        "Silk Road": {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
    }
    trivia = trivia_map.get(topic_key, {})
    table = (
        '{| class="infobox" style="float:right; margin:0 0 1em 1em; font-size:90%; width:280px; border-collapse:collapse;"\n'
        '|+ Quick Facts\n'
        '! colspan="2" style="background:#f0f0f0; text-align:center; font-size:1.1em;" | ' + topic_key.replace("_", " ") + '\n'
    )
    for label, value in trivia.items():
        table += '| ' + label + '\n| ' + value + '\n'
    table += '|}\n'

    infobox = img + '\n' + table + '\n'
    new_content = title_line + '\n\n' + infobox + body

    return save_page(wiki_title, new_content, "Add infobox table to article")

print("Testing fixes individually...")
for page, topic_key, image in [
    ("United States", "United States", "united_states.png"),
    ("Saudi Arabia", "Saudi Arabia", "saudi_arabia.png"),
    ("Game Theory", "Game Theory", "game_theory.png"),
]:
    print(f"\nFixing {page}...")
    fix_page(page, topic_key, image)