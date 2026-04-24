#!/usr/bin/env python3
import subprocess

pages = {
    'Law_of_Proximity': """The Law of Proximity is a key concept in Professor Jiang Xueqin's Predictive History framework.

== Definition ==

The Law of Proximity states that entities (countries, civilizations, empires) that are geographically close to each other will inevitably come into conflict over time. This is because proximity creates competition for resources, influence, and strategic advantage.

== Applications ==

=== Historical Examples ===
* Roman Empire and Carthaginian Empire - Punic Wars
* Byzantine Empire and Persian Empire - centuries of warfare
* Chinese Empire and Steppe Nomads - constant border conflicts
* European Colonial Powers - competition in Africa and Asia

=== Modern Applications ===
* China and India - border tensions in Himalayas
* China and Japan - competing influence in East China Sea
* Russia and NATO - expansion tensions in Eastern Europe
* Iran and Gulf States - regional dominance competition

== Key Insight ==

Professor Jiang emphasizes that geographic proximity is one of the STRONGEST predictors of conflict, often more important than ideological differences or cultural ties.

[[Category:Concepts|{{PAGENAME}}]]
""",

    'Eschatology': """Eschatology in the context of Predictive History refers to Professor Jiang Xueqin's analysis of END-GAME scenarios for empires and civilizations.

== The Imperial Cycle ==

According to Professor Jiang, empires follow a predictable cycle:

# Rise - Military conquest and economic expansion
# Peak - Maximum territorial extent and power
# Consolidation - Attempting to maintain position
# Decline - Internal decay and external pressures
# Fall - Complete collapse or transformation

== Signs of Imperial Decline ==

Professor Jiang identifies several key indicators:

* Fiscal Crisis - Empire spending more than it can sustain
* Military Overextension - Fighting too many wars simultaneously
* Internal Division - Political fragmentation and civil conflict
* Loss of Will - Elites prioritizing personal gain over imperial project
* Technological Stagnation - Failure to adapt to changing conditions

== Current Assessments ==

=== American Empire ===
* Showing signs of late-stage decline
* Fiscal deficits becoming unsustainable
* Political polarization weakening decision-making
* Military commitments exceeding capabilities

=== Chinese Ascendancy ===
* In earlier stage of imperial cycle
* Building infrastructure and economic leverage
* Avoiding direct military confrontation
* Waiting for American decline to accelerate

[[Category:Concepts|{{PAGENAME}}]]
""",

    'Strategic_Concepts': """This page collects key strategic concepts used in Professor Jiang Xueqin's Predictive History analysis.

== Game Theory Applications ==

=== Zero-Sum Games ===
* Many international relations are zero-sum
* One nation's gain is another's loss
* Strategic positioning is crucial

=== Commitment Problems ===
* Leaders make promises they cannot keep
* Long-term commitments are often broken
* Credibility is a key strategic resource

=== Information Asymmetry ===
* States often misread each other's intentions
* Misperception leads to unnecessary conflicts
* Signals can be deliberately misleading

== Geopolitical Framework ==

=== Heartland Theory ===
* Control of continental heartland provides strategic advantage
* Eurasion landmass as key geopolitical prize

=== Rimland Theory ===
* Coastal regions are crucial for maritime power
* Island chains as第一岛链 first island chain

=== Domino Theory ===
* Regional changes can cascade globally
* Small events can trigger larger transformations

== Historical Patterns ==

=== Imperial Overreach ===
* Empires expand until costs exceed benefits
* Overextension leads to vulnerability
* Strategic retrenchment is often too late

=== Power Transitions ===
* Rising powers challenge established ones
* Thucydides Trap - war between rising and declining powers
* But not all transitions lead to war

[[Category:Concepts|{{PAGENAME}}]]
"""
}

def create_page(title, content):
    with open('/tmp/wiki_page_content.txt', 'w') as f:
        f.write(content)
    
    cmd = ['php', '/usr/share/mediawiki/maintenance/edit.php', '--summary', 'Created special page', title]
    with open('/tmp/wiki_page_content.txt', 'r') as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    
    if result.returncode == 0 and 'done' in result.stdout:
        print('Created: {title}'.format(title=title))
        return True
    else:
        print('Failed: {title}'.format(title=title))
        return False

for title, content in pages.items():
    create_page(title, content)
