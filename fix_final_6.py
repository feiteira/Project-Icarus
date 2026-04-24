#!/usr/bin/env python3
"""Fix the 6 problem pages: Europe (wikitable→infobox) and 5 IMAGE_ONLY pages."""
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
    return "done" in result.stdout.lower()

TRIVIA = {
    "Europe":             {"Population": "~748 million", "Area": "10.2M km2", "GDP": "$17T (combined)", "Capital": "Brussels (EU)"},
    "Roman Empire":       {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
    "Holy Roman Empire":  {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
    "Federal Reserve":   {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance Sheet": "~$7.5T (2024)"},
    "World Economic Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
    "Silk Road":          {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
}

IMAGES = {
    "Europe": "europe.png",
    "Roman Empire": "roman_empire.png",
    "Holy Roman Empire": "holy_roman_empire.png",
    "Federal Reserve": "federal_reserve.png",
    "World Economic Forum": "world_economic_forum.png",
    "Silk Road": "silk_road.png",
}

def build_infobox(topic_key, image_file):
    img = "[[File:" + image_file + "|thumb|right|280px]]\n"
    trivia = TRIVIA.get(topic_key, {})
    if not trivia:
        return img + "\n"
    table = (
        '{| class="infobox" style="float:right; margin:0 0 1em 1em; font-size:90%; width:280px; border-collapse:collapse;"\n'
        '|+ Quick Facts\n'
        '! colspan="2" style="background:#f0f0f0; text-align:center; font-size:1.1em;" | ' + topic_key + '\n'
    )
    for label, value in trivia.items():
        table += '| ' + label + '\n| ' + value + '\n'
    table += '|}\n'
    return img + '\n' + table + '\n'

def fix_page(wiki_title, topic_key, image_file):
    content = get_page(wiki_title)
    if content is None:
        return False
    if content.startswith("#REDIRECT"):
        return False

    lines = content.split('\n')

    # Find title line (starts with ''')
    title_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("'''"):
            title_idx = i
            break

    if title_idx < 0:
        return False

    title_line = lines[title_idx].strip()

    # Skip past title + blank lines + [[File: lines
    body_start = title_idx + 1
    while body_start < len(lines):
        l = lines[body_start].strip()
        if l and not l.startswith('[[') and not l.startswith('{|'):
            break
        body_start += 1

    body = '\n'.join(lines[body_start:])
    body = re.sub(r'\n{3,}', '\n\n', body, flags=re.DOTALL).strip()

    infobox = build_infobox(topic_key, image_file)
    new_content = title_line + '\n\n' + infobox + body

    # Verify new content has both image and table
    if '[[File:' + image_file not in new_content:
        print(f"  WARNING: image missing from new content!")
    if 'class="infobox"' not in new_content:
        print(f"  WARNING: infobox class missing from new content!")

    # Save
    with open("/tmp/wiki_test_output.txt", "w") as f:
        f.write(new_content)
    result = subprocess.run(
        ["php", "/usr/share/mediawiki/maintenance/edit.php", "--summary", "Rebuild infobox: class=infobox float=right", title_line[3:-3]],
        stdin=open("/tmp/wiki_test_output.txt"),
        capture_output=True, text=True
    )
    return "done" in result.stdout.lower()

# First pass: check what's on Europe (wikitable issue)
print("=== Checking Europe ===")
europe = get_page("Europe")
print(europe[:500] if europe else "FAIL")

print()
for page in ["Europe", "Roman Empire", "Holy Roman Empire", "Federal Reserve", "World Economic Forum", "Silk Road"]:
    topic_key = page
    image_file = IMAGES[page]
    print(f"Fixing: {page}...", end=" ")
    ok = fix_page(page, topic_key, image_file)
    print("OK" if ok else "FAIL")