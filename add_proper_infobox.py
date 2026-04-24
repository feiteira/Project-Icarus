#!/usr/bin/env python3
import subprocess, json, urllib.parse

API = "https://localhost/api.php"

def api_get(params):
    query = "?" + urllib.parse.urlencode(params)
    cmd = ["curl", "-skL", API + query]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return None

def get_page(title):
    d = api_get({"action": "parse", "page": title, "prop": "wikitext", "format": "json"})
    if d and "parse" in d:
        return d["parse"]["wikitext"]["*"]
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

# All pages needing proper infobox at top
PAGES = [
    "China", "Russia", "Iran", "Japan", "India", "Israel",
    "Europe", "United States", "Ukraine", "Taiwan",
    "Saudi Arabia", "South China Sea",
    "NATO", "Cold War", "Roman Empire", "Holy Roman Empire",
    "Civilization", "Strategy", "Bitcoin",
    "Federal Reserve", "BRICS", "Islam", "Christianity",
    "Democracy", "Constitution", "Trump",
    "World Economic Forum", "Game Theory",
    "NeoCon", "Collapse", "Secession", "Woke", "Nuclear", "Silk Road", "Epstein",
]

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

TRIVIA = {
    "China":         {"Population": "~1.4 billion", "Area": "9.6M km2", "GDP": "$18T (nominal)", "Capital": "Beijing"},
    "Russia":        {"Population": "~144 million", "Area": "17.1M km2", "GDP": "$2.2T (nominal)", "Capital": "Moscow"},
    "Iran":          {"Population": "~88 million", "Area": "1.6M km2", "GDP": "$388B (nominal)", "Capital": "Tehran"},
    "Japan":         {"Population": "~125 million", "Area": "378K km2", "GDP": "$4.2T (nominal)", "Capital": "Tokyo"},
    "India":         {"Population": "~1.4 billion", "Area": "3.3M km2", "GDP": "$3.7T (nominal)", "Capital": "New Delhi"},
    "Israel":        {"Population": "~9.8 million", "Area": "22K km2", "GDP": "$525B (nominal)", "Capital": "Jerusalem"},
    "Europe":        {"Population": "~748 million", "Area": "10.2M km2", "GDP": "$17T (combined)", "Capital": "Brussels (EU)"},
    "United States": {"Population": "~335 million", "Area": "9.8M km2", "GDP": "$27T (nominal)", "Capital": "Washington D.C."},
    "Ukraine":        {"Population": "~37 million", "Area": "604K km2", "GDP": "$186B (nominal)", "Capital": "Kyiv"},
    "Taiwan":        {"Population": "~23 million", "Area": "36K km2", "GDP": "$756B (nominal)", "Capital": "Taipei"},
    "Saudi Arabia":  {"Population": "~36 million", "Area": "2.1M km2", "GDP": "$1.1T (nominal)", "Capital": "Riyadh"},
    "South China Sea": {"Area": "3.5M km2", "Key_Claimants": "China, Vietnam, Philippines, Malaysia", "Trade_Value": ">$3T annually"},
    "NATO":          {"Members": "32 member states", "Founded": "1949 (Washington Treaty)", "Defense": "Article 5 collective defense"},
    "Cold War":      {"Period": "1947-1991", "Parties": "United States vs Soviet Union", "End": "Dissolution of USSR (Dec 1991)"},
    "Roman Empire":  {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
    "Holy Roman Empire": {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
    "Civilization":  {"Earliest": "Sumer (~4500 BCE)", "Key_Indicators": "Cities, writing, agriculture, governance"},
    "Strategy":      {"Oldest": "Sun Tzu: Art of War (~500 BCE)", "Modern_Theorists": "Clausewitz, Jomini, Boyd"},
    "Bitcoin":       {"Created": "January 3, 2009", "Market_Cap": "~$1.3T (2024)", "Max_Supply": "21 million BTC"},
    "Federal Reserve": {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance_Sheet": "~$7.5T (2024)"},
    "BRICS":         {"Members": "10 nations (2024 expansion)", "Founded": "2009 (BRIC), expanded 2024"},
    "Islam":         {"Followers": "~1.9 billion", "Holy_Book": "Quran", "Origin": "7th century CE, Arabia"},
    "Christianity":  {"Followers": "~2.4 billion", "Holy_Book": "Bible", "Origin": "1st century CE, Roman Empire"},
    "Democracy":     {"Ancient_Origin": "Athens, 507 BCE", "Full_Democracies": "28 (2024 Democracy Index)"},
    "Constitution":  {"US_Signed": "September 17, 1787", "Amendments": "27", "Signatories": "39 delegates"},
    "Trump":         {"Name": "Donald John Trump (born 1946)", "President": "45th (2017-2021)", "Net_Worth": "~$2.6B (Forbes 2024)"},
    "World Economic Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
    "Game Theory":   {"Origin": "John von Neumann, 1928", "Key_Concept": "Nash equilibrium", "Applications": "Economics, military, politics"},
    "NeoCon":        {"Origin": "1960s-70s New York intellectuals", "Think_Tank": "Project for the New American Century (PNAC)"},
    "Collapse":      {"Roman_Collapse": "476 CE (Western Roman Empire)", "Key_Factors": "Economic, military, political, environmental"},
    "Secession":     {"US_Historical": "Confederate States (1861-1865)", "Legal_Status": "Not permitted (Texas v. White, 1869)"},
    "Woke":          {"Origin": "African American Vernacular (1930s)", "Meaning": "Awareness of systemic social injustice"},
    "Nuclear":       {"First_Use": "Hiroshima and Nagasaki, August 1945", "Total_Warheads": "~12,000 globally (2024)"},
    "Silk Road":     {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
    "Epstein":       {"Jeffrey_Epstein": "1954-2019", "Network": "Linked to hundreds of elite individuals", "Files_Released": "2024 (court-ordered)"},
}

def make_infobox(topic_key, image_file):
    trivia = TRIVIA.get(topic_key, {})
    img_block = "[[File:" + image_file + "|thumb|right|280px]]\n\n"

    if not trivia:
        return img_block

    table = (
        '{| class="infobox" style="font-size:90%; width:280px; float:right; margin:0 0 1em 1em;"\n'
        "|+ Quick Facts\n"
        "! colspan=\"2\" style=\"background:#f0f0f0;\" | " + topic_key.replace("_", " ") + "\n"
    )
    for k, v in trivia.items():
        label = k.replace("_", " ")
        table += "| " + label + "\n"
        table += "| " + v + "\n"
    table += "|}\n\n"

    return img_block + table

def fix_page(wiki_title, topic_key, image_file):
    content = get_page(wiki_title)
    if content is None:
        return False

    if content.startswith("#REDIRECT"):
        return False

    # Check if infobox already exists at top and is correct
    first_line = content.split("\n")[0] if content else ""
    has_infobox = "[[File:" + image_file in content and 'class="infobox"' in content

    if has_infobox:
        return False  # already correct

    # Build correct infobox
    infobox = make_infobox(topic_key, image_file)

    # Find insertion point: after any first line title/paragraph
    lines = content.split("\n")
    insert_idx = 0

    # Skip past the article title line ('''Title''')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("[[") and not stripped.startswith("==") and not stripped.startswith("#"):
            insert_idx = i
            break

    # Insert infobox at the top
    new_lines = [infobox] + lines[insert_idx:]
    new_content = "\n".join(new_lines)

    return save_page(wiki_title, new_content, "Adding proper Wikipedia-style infobox at top of article")

count = 0
for page in PAGES:
    topic_key = page.replace(" ", "_")
    image = IMAGES.get(page, "")
    if not image:
        print(f"  No image: {page}")
        continue
    if topic_key not in TRIVIA and image:
        print(f"  No trivia but has image: {page}")

print("\nAdding infoboxes to " + str(len(PAGES)) + " pages...")
for page in PAGES:
    topic_key = page.replace(" ", "_")
    image = IMAGES.get(page, "")
    if not image:
        continue
    print("Processing: " + page + "...")
    if fix_page(page, topic_key, image):
        print("  Added: " + page)
        count += 1
    else:
        print("  SKIP/FAIL: " + page)

print("\nDone! Added " + str(count) + " infoboxes.")