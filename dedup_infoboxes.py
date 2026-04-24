#!/usr/bin/env python3
import subprocess, json, urllib.parse, re

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

# All pages that may have duplicate infoboxes
PAGES = [
    "China", "Russia", "Iran", "Japan", "India", "Israel", "Europe",
    "United States", "Ukraine", "Taiwan", "Saudi Arabia", "South China Sea",
    "NATO", "Cold War", "Roman Empire", "Holy Roman Empire",
    "Civilization", "War", "Strategy", "Gold", "Bitcoin",
    "Federal Reserve", "BRICS", "Islam", "Christianity", "Democracy",
    "Constitution", "Trump", "World Economic Forum", "Game Theory",
    "NeoCon", "Collapse", "Secession", "Woke", "Nuclear", "Silk Road", "Epstein",
]

def clean_infobox(content, page_title):
    """Remove duplicate infoboxes, keeping only the first one at the top."""

    # Pattern: image file line followed by wikitable block
    # We want to KEEP the first occurrence and remove subsequent ones

    img_pattern = r'\n?\n(\{\| class="wikitable".*?\|\})\n\n\[\[File:'
    # This regex matches a wikitable followed immediately by another [[File:... (start of duplicate)

    # Simpler approach: split by [[File:...thumb|right|280px]]
    # Keep first, remove all others
    file_pattern = r'\[\[File:[^\]]+\|thumb\|right\|280px\]\]'

    parts = re.split(file_pattern, content)
    if len(parts) <= 1:
        return content  # no duplication

    # Keep first part (everything up to and including first image)
    # and the rest without the duplicate tables that follow
    first = parts[0]  # includes first image
    rest = '\n\n'.join(parts[1:])  # rest of content without images

    # Remove any orphaned wikitable blocks in the rest
    orphan_table_pattern = r'\n?\{\| class="wikitable".*?\|\}\n?'
    rest = re.sub(orphan_table_pattern, '\n', rest, flags=re.DOTALL)

    # Clean up multiple blank lines
    rest = re.sub(r'\n{3,}', '\n\n', rest)

    return first + '\n\n' + rest

def fix_css(content):
    """Change wikitable class to infobox and fix styling."""
    content = content.replace(
        'class="wikitable"',
        'class="infobox"'
    )
    # Fix infobox float/sizing to match Wikipedia style
    content = content.replace(
        'style="font-size:90%; width:280px; margin-left:1em;"',
        'style="font-size:90%; width:280px;"'
    )
    return content

count_fixed = 0
count_errors = 0

for page in PAGES:
    content = get_page(page)
    if content is None:
        print(f"  Could not fetch: {page}")
        continue
    if content.startswith("#REDIRECT"):
        continue

    original = content

    # Clean duplicates
    content = clean_infobox(content, page)

    # Fix CSS class
    content = fix_css(content)

    if content != original:
        if save_page(page, content, "Deduplicate infobox and fix CSS to infobox class"):
            print(f"  Fixed: {page}")
            count_fixed += 1
        else:
            print(f"  Failed: {page}")
            count_errors += 1
    else:
        print(f"  OK (no change): {page}")

print(f"\nDone! Fixed: {count_fixed}, Errors: {count_errors}")