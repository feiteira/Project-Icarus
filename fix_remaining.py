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
    return "done" in result.stdout.lower()

TRIVIA = {
    "Silk Road":     {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
    "Roman Empire":  {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
    "Holy Roman Empire": {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
    "Federal Reserve": {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance Sheet": "~$7.5T (2024)"},
    "World Economic Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
}

IMAGES = {
    "Silk Road": "silk_road.png",
    "Roman Empire": "roman_empire.png",
    "Holy Roman Empire": "holy_roman_empire.png",
    "Federal Reserve": "federal_reserve.png",
    "World Economic Forum": "world_economic_forum.png",
}

for page in ["Silk Road", "Roman Empire", "Holy Roman Empire", "Federal Reserve", "World Economic Forum"]:
    topic_key = page.replace(" ", "_")
    image = IMAGES[page]
    print(f"\n=== {page} ===")
    wt = get_page(page)
    if not wt:
        print("  FETCH FAIL")
        continue

    lines = wt.split('\n')

    # Find title line
    title_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("'''") and title_idx < 0:
            title_idx = i
            break

    if title_idx < 0:
        first_few = []
        for i in range(min(5, len(lines))):
            first_few.append(lines[i][:50])
        print("  NO TITLE FOUND, first lines:", first_few)
        title_line = "'''" + page + "'''"
        body_start = 0
    else:
        title_line = lines[title_idx].strip()
        body_start = title_idx + 1
        while body_start < len(lines):
            l = lines[body_start].strip()
            if l and not l.startswith('[['):
                break
            body_start += 1

    print("  title_line:", title_line[:80])

    body = '\n'.join(lines[body_start:])
    body = body.lstrip('\n')

    # Remove duplicate image lines
    body_lines = []
    for line in body.split('\n'):
        if image in line:
            print("  REMOVING line:", line[:80])
            continue
        body_lines.append(line)
    body = '\n'.join(body_lines)
    body = re.sub(r'\n{3,}', '\n\n', body).strip('\n')

    # Build infobox
    trivia = TRIVIA.get(topic_key, {})
    img = "[[File:" + image + "|thumb|right|280px]]\n"
    if trivia:
        table = '{| class="infobox" style="float:right; margin:0 0 1em 1em; font-size:90%; width:280px; border-collapse:collapse;"\n'
        table += '|+ Quick Facts\n'
        table += '! colspan="2" style="background:#f0f0f0; text-align:center; font-size:1.1em;" | ' + topic_key.replace("_", " ") + '\n'
        for label, value in trivia.items():
            table += '| ' + label + '\n| ' + value + '\n'
        table += '|}\n'
        infobox = img + '\n' + table + '\n'
    else:
        infobox = img + '\n'

    new_content = title_line + '\n\n' + infobox + body

    ok = save_page(page, new_content, "Add proper infobox table to article")
    print("  result:", "OK" if ok else "FAIL")