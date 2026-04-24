#!/usr/bin/env python3
"""Fix infoboxes: rebuild with image INSIDE the table, handle pages with/without explicit title line."""
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

def build_infobox(topic_key, image_file):
    trivia = TRIVIA.get(topic_key, {})
    table = (
        '{| class="infobox" style="float:right; margin:0 0 1em 1em; font-size:90%; width:280px; border-collapse:collapse; border:1px solid #aaa; background:#f9f9f9;"\n'
        '|+ <big>' + topic_key.replace("_", " ") + '</big>\n'
    )
    table += '|- style="text-align:center;"\n'
    table += '| colspan="2" | [[File:' + image_file + '|280px]]\n'
    for label, value in trivia.items():
        table += '| ' + label + '\n| ' + value + '\n'
    table += '|}\n'
    return table

TRIVIA = {
    "China":         {"Population": "~1.4 billion", "Area": "9.6M km²", "GDP": "$18T (nominal)", "Capital": "Beijing"},
    "Russia":        {"Population": "~144 million", "Area": "17.1M km²", "GDP": "$2.2T (nominal)", "Capital": "Moscow"},
    "Iran":          {"Population": "~88 million", "Area": "1.6M km²", "GDP": "$388B (nominal)", "Capital": "Tehran"},
    "Japan":         {"Population": "~125 million", "Area": "378K km²", "GDP": "$4.2T (nominal)", "Capital": "Tokyo"},
    "India":         {"Population": "~1.4 billion", "Area": "3.3M km²", "GDP": "$3.7T (nominal)", "Capital": "New Delhi"},
    "Israel":        {"Population": "~9.8 million", "Area": "22K km²", "GDP": "$525B (nominal)", "Capital": "Jerusalem"},
    "Europe":        {"Population": "~748 million", "Area": "10.2M km²", "GDP": "$17T (combined)", "Capital": "Brussels (EU)"},
    "United States": {"Population": "~335 million", "Area": "9.8M km²", "GDP": "$27T (nominal)", "Capital": "Washington D.C."},
    "Ukraine":        {"Population": "~37 million", "Area": "604K km²", "GDP": "$186B (nominal)", "Capital": "Kyiv"},
    "Taiwan":        {"Population": "~23 million", "Area": "36K km²", "GDP": "$756B (nominal)", "Capital": "Taipei"},
    "Saudi Arabia":  {"Population": "~36 million", "Area": "2.1M km²", "GDP": "$1.1T (nominal)", "Capital": "Riyadh"},
    "South_China_Sea": {"Area": "3.5M km²", "Key Claimants": "China, Vietnam, Philippines, Malaysia", "Trade Value": ">$3T annually"},
    "NATO":          {"Members": "32 member states", "Founded": "1949 (Washington Treaty)", "Defense": "Article 5 collective defense"},
    "Cold War":      {"Period": "1947-1991", "Parties": "United States vs Soviet Union", "End": "Dissolution of USSR (Dec 1991)"},
    "Roman Empire":  {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
    "Holy Roman Empire": {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
    "Civilization":  {"Earliest": "Sumer (~4500 BCE)", "Key Indicators": "Cities, writing, agriculture, governance"},
    "Strategy":      {"Oldest": "Sun Tzu: Art of War (~500 BCE)", "Modern Theorists": "Clausewitz, Jomini, Boyd"},
    "Bitcoin":       {"Created": "January 3, 2009", "Market Cap": "~$1.3T (2024)", "Max Supply": "21 million BTC"},
    "Federal Reserve": {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance Sheet": "~$7.5T (2024)"},
    "BRICS":         {"Members": "10 nations (2024 expansion)", "Founded": "2009 (BRIC), expanded 2024"},
    "Islam":         {"Followers": "~1.9 billion", "Holy Book": "Quran", "Origin": "7th century CE, Arabia"},
    "Christianity":  {"Followers": "~2.4 billion", "Holy Book": "Bible", "Origin": "1st century CE, Roman Empire"},
    "Democracy":     {"Ancient Origin": "Athens, 507 BCE", "Full Democracies": "28 (2024 Democracy Index)"},
    "Constitution":  {"US Signed": "September 17, 1787", "Amendments": "27", "Signatories": "39 delegates"},
    "Trump":         {"Name": "Donald John Trump (born 1946)", "President": "45th (2017-2021)", "Net Worth": "~$2.6B (Forbes 2024)"},
    "World Economic Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
    "Game Theory":   {"Origin": "John von Neumann, 1928", "Key Concept": "Nash equilibrium", "Applications": "Economics, military, politics"},
    "NeoCon":        {"Origin": "1960s-70s New York intellectuals", "Think Tank": "Project for the New American Century (PNAC)"},
    "Collapse":      {"Roman Collapse": "476 CE (Western Roman Empire)", "Key Factors": "Economic, military, political, environmental"},
    "Secession":     {"US Historical": "Confederate States (1861-1865)", "Legal Status": "Not permitted (Texas v. White, 1869)"},
    "Woke":          {"Origin": "African American Vernacular (1930s)", "Meaning": "Awareness of systemic social injustice"},
    "Nuclear":       {"First Use": "Hiroshima and Nagasaki, August 1945", "Total Warheads": "~12,000 globally (2024)"},
    "Silk Road":     {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
    "Epstein":       {"Jeffrey Epstein": "1954-2019", "Network": "Linked to hundreds of elite individuals", "Files Released": "2024 (court-ordered)"},
}

IMAGES = {
    "China": "china.png", "Russia": "russia.png", "Iran": "iran.png",
    "Japan": "japan.png", "India": "india.png", "Israel": "israel.png",
    "Europe": "europe.png", "United States": "united_states.png",
    "Ukraine": "ukraine.png", "Taiwan": "taiwan.png",
    "Saudi Arabia": "saudi_arabia.png",
    "South China Sea": "south_china_sea.png",
    "NATO": "nato.png", "Cold War": "cold_war.png",
    "Roman Empire": "roman_empire.png",
    "Holy Roman Empire": "holy_roman_empire.png",
    "Civilization": "civilization.png", "Strategy": "strategy.png",
    "Bitcoin": "bitcoin.png", "Federal Reserve": "federal_reserve.png",
    "BRICS": "brics.png", "Islam": "islam.png", "Christianity": "christianity.png",
    "Democracy": "democracy.png", "Constitution": "constitution.png",
    "Trump": "trump.png",
    "World Economic Forum": "world_economic_forum.png",
    "Game Theory": "game_theory.png",
    "NeoCon": "neocon.png", "Collapse": "collapse.png",
    "Secession": "secession.png", "Woke": "woke.png",
    "Nuclear": "nuclear.png", "Silk Road": "silk_road.png",
    "Epstein": "epstein.png",
}

def fix_page(wiki_title):
    topic_key = wiki_title.replace(" ", "_")
    image_file = IMAGES.get(wiki_title, "")
    if not image_file:
        return False

    content = get_page(wiki_title)
    if content is None or content.startswith("#REDIRECT"):
        return False

    lines = content.split('\n')
    n = len(lines)

    # Find title_idx: first non-empty line that starts with '''
    title_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("'''"):
            title_idx = i
            break

    # Build the title line
    if title_idx >= 0:
        title_line = lines[title_idx].strip()
    else:
        title_line = "'''" + wiki_title + "'''"

    # Skip past title (if exists) + blank lines + image lines + infobox table
    # Strategy: scan from after title (or from 0 if no title), skip:
    #   - blank lines
    #   - [[File:...]] lines
    #   - {| ... |} table blocks
    # Stop at first line that is non-blank and not an image/table line

    if title_idx >= 0:
        scan_start = title_idx + 1
    else:
        scan_start = 0

    body_start = scan_start
    in_table = False
    for i in range(scan_start, n):
        l = lines[i].strip()

        if l.startswith('{|'):
            in_table = True
            body_start = i + 1
            continue

        if in_table:
            if l == '|}':
                in_table = False
                body_start = i + 1
                continue
            body_start = i + 1
            continue

        if l.startswith('[[') and 'File:' in l:
            body_start = i + 1
            continue

        if not l:
            body_start = i + 1
            continue

        # First non-blank, non-image, non-table content
        break

    body = '\n'.join(lines[body_start:])
    body = re.sub(r'\n{3,}', '\n\n', body, flags=re.DOTALL).strip()

    infobox = build_infobox(topic_key, image_file)
    new_content = title_line + '\n\n' + infobox + '\n' + body

    return save_page(wiki_title, new_content, "Rebuild infobox with image inside table")

PAGES = [
    "China", "Russia", "Iran", "Japan", "India", "Israel",
    "United States", "Ukraine", "Taiwan", "Saudi Arabia", "South China Sea",
    "NATO", "Cold War", "Roman Empire", "Holy Roman Empire",
    "Civilization", "Strategy", "Bitcoin", "Federal Reserve",
    "BRICS", "Islam", "Christianity", "Democracy", "Constitution",
    "Trump", "World Economic Forum", "Game Theory",
    "NeoCon", "Collapse", "Secession", "Woke", "Nuclear", "Silk Road", "Epstein"
]

fixed = failed = 0
for page in PAGES:
    ok = fix_page(page)
    print(f"{page}: {'OK' if ok else 'FAIL'}")
    if ok:
        fixed += 1
    else:
        failed += 1

print(f"\nFixed: {fixed}, Failed: {failed}")