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
    ok = "done" in result.stdout.lower()
    if not ok:
        print(f"  Save error: {result.stdout[:200]}")
    return ok

IMAGES = {
    "China": "china.png", "Russia": "russia.png", "Iran": "iran.png",
    "Japan": "japan.png", "India": "india.png", "Israel": "israel.png",
    "Europe": "europe.png", "United_States": "united_states.png",
    "Ukraine": "ukraine.png", "Taiwan": "taiwan.png",
    "Saudi_Arabia": "saudi_arabia.png", "South_China_Sea": "south_china_sea.png",
    "NATO": "nato.png", "Cold_War": "cold_war.png",
    "Roman_Empire": "roman_empire.png", "Holy_Roman_Empire": "holy_roman_empire.png",
    "Empire": "empire.png", "Civilization": "civilization.png", "War": "war.png",
    "Strategy": "strategy.png", "Gold": "gold.png", "Bitcoin": "bitcoin.png",
    "Federal_Reserve": "federal_reserve.png", "BRICS": "brics.png",
    "Islam": "islam.png", "Christianity": "christianity.png", "Judaism": "judaism.png",
    "Democracy": "democracy.png", "Constitution": "constitution.png",
    "Trump": "trump.png", "World_Economic_Forum": "world_economic_forum.png",
    "Game_Theory": "game_theory.png", "NeoCon": "neocon.png", "Collapse": "collapse.png",
    "Secession": "secession.png", "Woke": "woke.png", "Nuclear": "nuclear.png",
    "Silk_Road": "silk_road.png", "Epstein": "epstein.png", "Civil_War": "war.png",
}

TRIVIA = {
    "China":         {"Population": "~1.4 billion", "Area": "9.6M km2", "GDP": "$18T (nominal)", "Capital": "Beijing"},
    "Russia":        {"Population": "~144 million", "Area": "17.1M km2", "GDP": "$2.2T (nominal)", "Capital": "Moscow"},
    "Iran":          {"Population": "~88 million", "Area": "1.6M km2", "GDP": "$388B (nominal)", "Capital": "Tehran"},
    "Japan":         {"Population": "~125 million", "Area": "378K km2", "GDP": "$4.2T (nominal)", "Capital": "Tokyo"},
    "India":         {"Population": "~1.4 billion", "Area": "3.3M km2", "GDP": "$3.7T (nominal)", "Capital": "New Delhi"},
    "Israel":        {"Population": "~9.8 million", "Area": "22K km2", "GDP": "$525B (nominal)", "Capital": "Jerusalem"},
    "Europe":        {"Population": "~748 million", "Area": "10.2M km2", "GDP": "$17T (combined)", "Capital": "Brussels (EU)"},
    "United_States": {"Population": "~335 million", "Area": "9.8M km2", "GDP": "$27T (nominal)", "Capital": "Washington D.C."},
    "Ukraine":        {"Population": "~37 million", "Area": "604K km2", "GDP": "$186B (nominal)", "Capital": "Kyiv"},
    "Taiwan":        {"Population": "~23 million", "Area": "36K km2", "GDP": "$756B (nominal)", "Capital": "Taipei"},
    "Saudi_Arabia":  {"Population": "~36 million", "Area": "2.1M km2", "GDP": "$1.1T (nominal)", "Capital": "Riyadh"},
    "South_China_Sea": {"Area": "3.5M km2", "Key_Claimants": "China, Vietnam, Philippines, Malaysia", "Trade_Value": ">$3T annually"},
    "NATO":          {"Members": "32 member states", "Founded": "1949 (Washington Treaty)", "Defense": "Article 5 collective defense"},
    "Cold_War":      {"Period": "1947-1991", "Parties": "United States vs Soviet Union", "End": "Dissolution of USSR (Dec 1991)"},
    "Roman_Empire":  {"Founded": "27 BCE (Augustus)", "Dissolved": "476 CE (Western)", "Capital": "Rome (later Constantinople)"},
    "Holy_Roman_Empire": {"Founded": "962 CE (Otto I)", "Dissolved": "1806 (Napoleon)", "Capital": "Aachen / Vienna"},
    "Empire":        {"Largest_Area": "British Empire (35.5M km2)", "Longest_Lived": "Roman Empire (~1,500 years)"},
    "Civilization":  {"Earliest": "Sumer (~4500 BCE)", "Key_Indicators": "Cities, writing, agriculture, governance"},
    "War":           {"Deadliest": "World War II (70-85M deaths)", "Top_Spender": "United States ($886B in 2023)"},
    "Strategy":      {"Oldest": "Sun Tzu: Art of War (~500 BCE)", "Modern_Theorists": "Clausewitz, Jomini, Boyd"},
    "Gold":          {"Production_Annual": "~3,600 tonnes (2023)", "Top_Holder": "US (8,133 tonnes)", "Price_Range": "$1,900-2,100/oz (2024)"},
    "Bitcoin":       {"Created": "January 3, 2009", "Market_Cap": "~$1.3T (2024)", "Max_Supply": "21 million BTC"},
    "Federal_Reserve": {"Founded": "December 23, 1913", "Chair": "Jerome Powell", "Balance_Sheet": "~$7.5T (2024)"},
    "BRICS":         {"Members": "10 nations (2024 expansion)", "Founded": "2009 (BRIC), expanded 2024"},
    "Islam":         {"Followers": "~1.9 billion", "Holy_Book": "Quran", "Origin": "7th century CE, Arabia"},
    "Christianity":  {"Followers": "~2.4 billion", "Holy_Book": "Bible", "Origin": "1st century CE, Roman Empire"},
    "Judaism":       {"Followers": "~15 million", "Holy_Book": "Torah (Tanakh)", "Origin": "~1300 BCE, Levant"},
    "Democracy":     {"Ancient_Origin": "Athens, 507 BCE", "Full_Democracies": "28 (2024 Democracy Index)"},
    "Constitution":  {"US_Signed": "September 17, 1787", "Amendments": "27", "Signatories": "39 delegates"},
    "Trump":         {"Name": "Donald John Trump (born 1946)", "President": "45th (2017-2021)", "Net_Worth": "~$2.6B (Forbes 2024)"},
    "World_Economic_Forum": {"Founded": "1971 (Klaus Schwab)", "Event": "Davos Summit, Switzerland", "Members": "1,000+ global leaders"},
    "Game_Theory":   {"Origin": "John von Neumann, 1928", "Key_Concept": "Nash equilibrium", "Applications": "Economics, military, politics"},
    "NeoCon":        {"Origin": "1960s-70s New York intellectuals", "Think_Tank": "Project for the New American Century (PNAC)"},
    "Collapse":      {"Roman_Collapse": "476 CE (Western Roman Empire)", "Key_Factors": "Economic, military, political, environmental"},
    "Secession":     {"US_Historical": "Confederate States (1861-1865)", "Legal_Status": "Not permitted (Texas v. White, 1869)"},
    "Woke":          {"Origin": "African American Vernacular (1930s)", "Meaning": "Awareness of systemic social injustice"},
    "Nuclear":       {"First_Use": "Hiroshima and Nagasaki, August 1945", "Total_Warheads": "~12,000 globally (2024)"},
    "Silk_Road":     {"Origin": "130s BCE (Han Dynasty)", "Routes": "Land + Maritime Silk Road", "Modern": "Belt and Road Initiative (2013)"},
    "Epstein":       {"Jeffrey_Epstein": "1954-2019", "Network": "Linked to hundreds of elite individuals", "Files_Released": "2024 (court-ordered)"},
}

def make_infobox(topic_key, image_file):
    trivia = TRIVIA.get(topic_key, {})
    img_block = "[[File:" + image_file + "|thumb|right|280px]]\n\n"

    if not trivia:
        return img_block

    table = (
        '{| class="wikitable" style="font-size:90%; width:280px; margin-left:1em;"\n'
        "|+ Quick Facts\n"
        "! colspan=\"2\" style=\"background:#f0f0f0;\" | " + topic_key.replace("_", " ") + "\n"
    )
    for k, v in trivia.items():
        label = k.replace("_", " ")
        table += "| " + label + "\n"
        table += "| " + v + "\n"
    table += "|}\n\n"

    return img_block + table

def update_page(wiki_title, topic_key, image_file):
    content = get_page(wiki_title)
    if content is None:
        print("  Could not fetch " + wiki_title)
        return

    if content.startswith("#REDIRECT"):
        print("  SKIP (redirect): " + wiki_title)
        return

    infobox = make_infobox(topic_key, image_file)

    # Always insert at beginning (idx=0), before any content
    # This ensures infobox appears right after the title
    lines = content.split("\n")

    # Skip initial empty lines / templates at very top
    insert_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Stop at first real content or heading
        if stripped and not stripped.startswith("[["):
            insert_idx = i
            break
        insert_idx = i + 1

    new_lines = lines[:insert_idx] + [infobox] + lines[insert_idx:]
    new_content = "\n".join(new_lines)

    if save_page(wiki_title, new_content, "Moving infobox to top of article"):
        print("  Fixed: " + wiki_title)
    else:
        print("  FAILED: " + wiki_title)

# Pages that need fixing (infobox appeared in wrong place or missing at top)
BAD_PAGES = [
    ("Saudi Arabia", "Saudi_Arabia", "saudi_arabia.png"),
    ("South China Sea", "South_China_Sea", "south_china_sea.png"),
    ("NATO", "NATO", "nato.png"),
    ("Cold War", "Cold_War", "cold_war.png"),
    ("Roman Empire", "Roman_Empire", "roman_empire.png"),
    ("Holy Roman Empire", "Holy_Roman_Empire", "holy_roman_empire.png"),
    ("Empire", "Empire", "empire.png"),
    ("Civilization", "Civilization", "civilization.png"),
    ("Gold", "Gold", "gold.png"),
    ("Bitcoin", "Bitcoin", "bitcoin.png"),
    ("BRICS", "BRICS", "brics.png"),
    ("Islam", "Islam", "islam.png"),
    ("Judaism", "Judaism", "judaism.png"),
    ("Democracy", "Democracy", "democracy.png"),
    ("Woke", "Woke", "woke.png"),
    ("Nuclear", "Nuclear", "nuclear.png"),
    ("Silk Road", "Silk_Road", "silk_road.png"),
    ("Epstein", "Epstein", "epstein.png"),
]

print("Fixing infobox placement for " + str(len(BAD_PAGES)) + " pages...")
for wiki_title, topic_key, image_file in BAD_PAGES:
    print("Fixing: " + wiki_title + "...")
    update_page(wiki_title, topic_key, image_file)

print("Done!")