#!/usr/bin/env python3
"""Post Professor Jiang analysis comments to MediaWiki Talk pages."""
import json, re, sys, os, subprocess, datetime

MAINTAINER_PHP = "/usr/share/mediawiki/maintenance/edit.php"

def load_data():
    with open('/home/feiteira/.openclaw/workspace/video_summaries.json','r') as f:
        return json.load(f)

def get_topic_videos(data, topic):
    return [v for v in data if topic in [t['topic'] for t in v.get('topics',[])]]

def extract_topic_snippets(video, topic):
    """Extract text snippets mentioning the topic from full_text."""
    text = video.get('full_text', '')
    if not text:
        return []

    snippets = []
    for t in video.get('topics', []):
        if t['topic'] == topic and t.get('first_mention'):
            start = t['first_mention'].get('start')
            if start is None:
                continue
            # Extract ~800 chars around the mention
            chars_per_sec = 15  # approximate
            pos = int(start * chars_per_sec)
            buf = 600
            start_idx = max(0, pos - buf)
            end_idx = min(len(text), pos + buf)
            snippet = text[start_idx:end_idx]
            # Remove filler words
            snippet = re.sub(r'\b(um|uh|like|you know|sort of|kind of)\b', '', snippet, flags=re.IGNORECASE)
            snippet = re.sub(r'\s+', ' ', snippet).strip()
            if snippet:
                snippets.append(snippet)
    return snippets[:2]  # max 2 per video

def get_api_content(title):
    """Read existing Talk page content via API."""
    import urllib.parse
    encoded = urllib.parse.quote(title, safe='')
    cmd = ['curl', '-sk', f'https://localhost/api.php?action=query&prop=revisions&titles={encoded}&rvslots=main&format=json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if page_id == '-1':
                return ''
            revisions = page_data.get('revisions', [])
            if revisions:
                return revisions[0].get('slots', {}).get('main', {}).get('*', '')
        return ''
    except Exception as e:
        print(f"API read error: {e}")
        return ''

def write_via_php(title, content, summary):
    """Write content to page via PHP maintenance script."""
    cmd = ['php', MAINTAINER_PHP, '--summary', summary, '--no-rc', title]
    result = subprocess.run(cmd, input=content, capture_output=True, text=True, timeout=60)
    return result.stdout + result.stderr

COMMENTS = {
    "Civilization": """Professor Jiang's analysis of Civilization draws from 134 videos across his Predictive History series, forming one of the most comprehensive civilizational frameworks in his work. He argues that civilizations are not merely political arrangements but living organisms that move through predictable stages of birth, growth,成熟, decline, and collapse. His core model draws on Tainter's complexity theory and Polybius's cyclical history, combined with his own Law of Proximity — the principle that actors closest to a conflict bear the greatest costs and possess the strongest incentives to resolve it, while distant powers consistently miscalculate. He identifies elite overproduction as the primary driver of civilizational collapse: when a civilization produces more elite aspirants than its institutional structures can absorb, the resulting competition becomes destructive, fragmenting society and undermining the shared myths that hold civilizations together.

His treatment of American civilization is particularly significant. In videos such as [[Video:_gH4PvIni5E|Civilization #END: The Decline and Fall of the American Empire]] and [[Video:ENry-rDFzmA|America is an Anti-Civilization]], he argues that the United States has entered an advanced stage of civilizational decline characterized by deindustrialization, institutional corruption, elite overproduction in universities and credentialing systems, and the replacement of substantive shared mythology with ideological fragmentation. He draws extensively on the Roman Empire as a parallel, noting that empires do not typically collapse from external invasion but from internal incapacity to adapt to changing circumstances. Rome's Senate, he argues, faced the same structural dilemma as Washington: how to maintain imperial commitments when the fiscal and demographic base no longer supported them.

The religious dimension of civilization receives substantial treatment. Videos like [[Video:VanPH0GFTsA|Civilization #3: The Religious Imagination]] and [[Video:C9rzPGJ0wm4|Civilization #28: Muhammad's Revolution of God]] explore how civilizations encode their deepest values and fears into religious narratives that provide social cohesion across generations. When these religious-imaginative structures lose their binding power, civilizations become vulnerable to what he calls "elite overproduction" — the system produces more credentialed aspirants than positions exist, generating resentment and ideological radicalization. His analysis of the Reformation in [[Video:TcxlOiJz8V0|Civilization #42: The Protestant Reformation and the Birth of the Modern World]] demonstrates how religious fragmentation preceded and enabled the modern nation-state system.

He identifies the Scientific Revolution and the Enlightenment as critical inflection points where European civilization began systematically dismantling the religious frameworks that had provided civilizational coherence. [[Video:_3c3FjS57x4|Civilization #55: Kant, Hegel, and the Theory of Everything]] traces how German idealist philosophy attempted to construct new foundations for civilization after the erosion of traditional religious authority, ultimately failing to provide the binding mythological power that previous generations had derived from religion. This creates, in his view, the fundamental crisis of modernity: the destruction of civilizational mythology without a replacement that can command broad allegiance. The consequence is identity politics and ideological tribalism as substitute mythologies that further fragment rather than unite.""",

    "Strategy": """Professor Jiang's analysis of Strategy draws from 136 videos in his Predictive History collection, constituting the most systematic application of game theory to geopolitics in his body of work. At the heart of his strategic framework lies the Law of Asymmetry: smaller, more motivated powers consistently defeat larger, overextended empires throughout history because the asymmetry of incentives produces superior commitment and strategic patience. He demonstrates this principle across diverse cases from Hannibal Barca's destruction of Roman armies in [[Video:tH3QKnxGi90|Civilization #14: Hannibal Barca, Lucius Brutus, and the Tragedy of Glory]], to Philip II of Macedon's methodical construction of military superiority in [[Video:l6AroD58jkE|Civilization #11: The Greatness of Philip II of Macedon]], to the contemporary US-Iran dynamic where he argues America has entered a strategic trap it cannot escape without catastrophic consequences.

The Law of Proximity, developed in [[Video:nOQqGy4boBY|Game Theory #14: The Law of Proximity]], states that those closest to a conflict bear the greatest costs and possess the strongest incentives for resolution, while distant powers consistently miscalculate because they bear lower costs and therefore exercise less care. This principle explains, in his analysis, why the United States has lost every major war since Korea despite overwhelming material superiority — the incentives structure of a distant hegemon systematically produces strategic hubris and inadequate commitment. He applies this to the Iran situation in multiple videos including [[Video:7y_hbz6loEo|Geo-Strategy #8: The Iran Trap]], where he argues that Iran has constructed a deliberate trap using geographic advantages, asymmetric capabilities, and the incentive structures of regional powers to make American military action suicidal.

He identifies geographic constraint as the fundamental variable in strategic analysis. [[Video:DUzcd54snrs|The Iran Trap: How Geography Destroys Superpowers]] analyzes how the Strait of Hormuz, the Zagros Mountains, and Iran's strategic depth create insurmountable challenges for any conventional invasion. His broader geopolitical framework, articulated in [[Video:x7x_raOIiHc|The Three Evergreen Laws of Geopolitics]], synthesizes historical patterns into three enduring principles: geographic constraints shape strategic options; the incentive structures of actors determine their behavior more reliably than their stated intentions; and empires decline when their commitments exceed their capabilities. The current moment represents, in his analysis, the terminal phase of American hegemony as these laws produce their inevitable effects.""",

    "Islam": """Professor Jiang's analysis of Islam draws from 90 videos across his Civilization, Geo-Strategy, and Secret History series, treating Islam as a major civilizational force rather than a geopolitical variable to be managed. His most extensive treatment appears in [[Video:2OdO8LoKuo8|Civilization #37: The Golden Age of Islam]], where he describes the period from roughly 750 to 1100 CE as one of history's greatest intellectual explosions, during which Islamic civilizations preserved Greek knowledge, made transformative advances in mathematics and astronomy, and created institutional structures for scholarship that Europe would not match for centuries. He argues that understanding this intellectual heritage is essential for comprehending both the historical relationship between Islamic and Western civilizations and the contemporary geopolitical landscape.

His analysis of Muhammad's revolution in [[Video:C9rzPGJ0wm4|Civilization #28: Muhammad's Revolution of God]] situates the birth of Islam within the context of Late Antiquity's crisis — the simultaneous exhaustion of Roman and Persian empires, the failure of existing religious structures to provide meaning, and the emergence of new political-religious syntheses that could unite diverse populations under coherent moral frameworks. He draws a sharp distinction between the original Islamic message, the institutional church that developed under the Caliphates, and the diverse regional traditions that emerged from them. This differentiation is critical to his geopolitical analysis, where he argues that Iran represents a distinct Islamic strategic tradition — Shia Islam's emphasis on hidden knowledge and messianic waiting has produced a civilization capable of strategic patience and subterranean development that Sunni traditions do not replicate.

The convergence of Islamic eschatology with other religious frameworks receives attention in videos such as [[Video:YQ-xg1nIbMs|Geo-Strategy Update #7: When Eschatologies Converge]] and [[Video:lkKrZq4YdqY|Geo-Strategy #2: Christian Zionism and the Middle East Conflict]]. He argues that when religious end-times narratives become intertwined with concrete geopolitical interests, they produce additional dimensions of conflict that purely rational actor models cannot capture. [[Video:QTs3fOyebOU|Islam was a Major Intellectual Revolution]] extends his argument that Islam belongs in the same category as the Scientific Revolution and the Enlightenment as a transformative intellectual event that reshaped human understanding of nature, society, and the divine.""",

    "Christianity": """Professor Jiang's analysis of Christianity draws from 72 videos spanning his Civilization, Secret History, and Great Books series, treating Christianity not as a doctrinal system but as a civilizational force that reshaped human consciousness and political organization. His treatment begins with Jesus's original vision in [[Video:pp0E1gb80WQ|Secret History #22: The Divine Spark of Jesus]] and [[Video:NY2hjRIIKf4|The Real Jesus Was Too Dangerous for the Church]], where he argues that the historical Jesus represented a radical critique of religious institutional power that was immediately co-opted and neutralized by the very movement his execution paradoxically enabled. The transformation of Jesus's critique into Roman state religion under Constantine, analyzed in [[Video:za30rbC3tTg|Civilization #26: Constantine's Monotheistic Revolution]], represents in his view one of history's great betrayals — the reduction of a revolutionary spiritual vision to an instrument of imperial control.

The career of Paul of Tarsus receives particular scrutiny in [[Video:kuMhSFXnr5I|Civilization #25: Paul of Tarsus, Messiah of Rome]], where he argues that Paul's genius lay in translating Jesus's Jewish critique into terms the Roman world could accept — exchanging the critique of religious power for a critique of political power, and positioning Christianity as compatible with imperial governance rather than subversive of it. This theological translation made Christianity politically useful to Rome, but in Jiang's analysis it also amputated the spiritual core that had made the movement dangerous to established order. The resulting institutional church bore the structural imprint of the Roman Empire it inherited: hierarchical, bureaucratic, and oriented toward maintaining order rather than pursuing prophetic transformation.

His analysis extends through the Byzantine Empire in [[Video:abs6z7VPEMc|Civilization #33: The Rise and Fall of the Byzantine Empire]], where he traces how the fusion of Christianity with imperial power produced a civilization that lasted a millennium but ultimately collapsed under the weight of its own contradictions. [[Video:GdbZBVUIVDE|Civilization #27: Augustine's Empire of God]] examines how Augustine's theology provided the intellectual framework for Christendom's self-understanding as a spiritual empire coexisting uneasily with temporal power. The Protestant Reformation in [[Video:TcxlOiJz8V0|Civilization #42: The Protestant Reformation and the Birth of the Modern World]] represents, in his analysis, Christianity's internal explosion under the weight of its accumulated contradictions — a rupture that ultimately enabled the modern nation-state system by destroying the religious unity that had made Christendom possible as a civilizational unit.""",

    "Nuclear": """Professor Jiang's analysis of Nuclear strategy draws from 96 videos where he examines how the existence of nuclear weapons fundamentally transforms the logic of great power conflict. His core argument is that nuclear deterrence creates a new strategic reality in which escalation dynamics make direct military confrontation between nuclear powers potentially civilizational-ending events, constraining their behavior in ways that conventional analysis cannot capture. In [[Video:HzIX1hy8hr0|Israel's Iran War Plan for Total Domination]], he argues that while Israel possesses substantial nuclear capabilities, the uncertainty of escalation outcomes in a regional nuclear exchange creates a form of mutual deterrence that paradoxically makes total war less likely even as it increases the stakes of any conflict that does occur.

The Iran nuclear question receives extensive treatment across his Geo-Strategy series. Videos such as [[Video:8XdL-7tAqnU|Geo-Strategy Update: US-Iran War Incoming]] and [[Video:jIS2eB-rGv0|Game Theory #9: The US-Iran War]] explore how Iran's development of nuclear capabilities — or strategic ambiguity regarding those capabilities — fundamentally changes the strategic calculus of any potential military confrontation. His analysis suggests that a nuclear-armed Iran would be effectively immune from the regime change operations that the United States has successfully deployed against non-nuclear adversaries like Iraq and Libya. The nuclear dimension transforms Iran from a regional power into a potential civilization-shaping actor, since any conflict involving Iranian nuclear assets would necessarily draw in major powers and risk escalation beyond the regional level.

He connects nuclear strategy to his broader civilizational analysis in videos like [[Video:GdbZBVUIVDE|Civilization #27: Augustine's Empire of God]] and [[Video:5HwZx5kQm9o|Civilization #46: The Revolution of Reason]], where he traces how the scientific and technological revolution that produced nuclear weapons simultaneously created the intellectual frameworks for understanding and the institutional structures for developing them. The nuclear topic intersects with his analysis of elite overproduction in [[Video:QwfB-vXXKWU|Civilization #6: Elite Overproduction and the Bronze Age Collapse]], where he draws parallels between civilizational collapses driven by internal contradictions and contemporary dynamics where advanced societies may be approaching systemic failure points. His prediction is that nuclear-armed great power competition will produce a new equilibrium — a cold peace maintained by mutual deterrence that ultimately proves more stable than the unipolar moment it replaced.""",

    "India": """Professor Jiang's analysis of India draws from 93 videos where he examines the subcontinent's civilizational depth, colonial exploitation, and emerging strategic position. His most direct treatment of India's relationship with Western imperialism appears in [[Video:2AkLsDPgdng|How the British Stole India's Future]], where he describes the systematic deindustrialization of what had been one of the world's most sophisticated manufacturing economies — India historically produced roughly a quarter of global GDP before British rule, and the systematic destruction of Indian textile and manufacturing industries created the foundation for Britain's industrial revolution while pauperizing the Indian population. He argues that this colonial extraction represents one of history's most significant wealth transfers, and that understanding it is essential for comprehending contemporary global economic inequalities.

The civilizational continuity of India forms a major theme across his Civilization series. [[Video:cvI8rukoda8|Civilization #20: The Proto-Buddhists of the Indus Valley]] examines the deep historical roots of Indian civilization in the Indus Valley culture, tracing continuities through the Vedic period, the Buddha's revolution, and the classical Hindu-Buddhist synthesis that defined Indian civilization for millennia. He argues that India's civilizational resilience — surviving conquest, absorption, and attempted erasure by multiple external powers — represents a remarkable case of cultural persistence that provides the subcontinent with resources for renewed great power status that more historically fragile civilizations cannot draw upon. The Hindu-Muslim divide receives substantial attention as both a legacy of India's composite civilizational heritage and a contemporary source of strategic vulnerability, particularly in [[Video:MNSrL77VQ-U|Predictive History on Islamic Empires and Civilization]].

India's emerging strategic position in the great power competition between the United States and China forms the contemporary dimension of his analysis. Videos such as [[Video:Awmi6GcMih0|What the Next 10 to 20 Years Look Like]] examine how both superpowers seek Indian partnership, creating opportunities for India to extract concessions from both sides while maintaining strategic autonomy. He predicts that India will emerge as a major pole in the emerging multipolar order, but that internal divisions — particularly between Hindu nationalist forces and secular pluralist traditions — represent the primary threat to realizing this potential. The British colonial legacy, in his analysis, was not merely economic but psychological: it instilled a civilizational inferiority complex in Indian elites that has only begun to be overcome in the current generation.""",

    "Japan": """Professor Jiang's analysis of Japan draws from 96 videos where he examines Japan's unique trajectory as the only non-Western civilization to achieve comprehensive modernization while maintaining cultural continuity and strategic autonomy. His central argument is that Japan's Meiji Restoration represents a strategic masterclass in selective modernization — the Japanese leadership recognized that Western technology and institutional forms provided functional advantages that could be adopted without surrendering Japanese cultural identity or political sovereignty. This model stands in contrast to both the total Westernization attempted by some non-Western elites and the defensive traditionalism that proved insufficient against Western imperial expansion.

His treatment of Japan's economic trajectory draws important lessons for his broader geopolitical framework. [[Video:Awmi6GcMih0|What the Next 10 to 20 Years Look Like]] discusses the Japanese economic miracle, the Plaza Accord's disruption of Japan's export-led growth model, and the subsequent "lost decades" of stagnation as a case study in how rising powers transition through different stages of development and face new vulnerabilities at each transition. He argues that Japan's demographic crisis — its rapidly aging and declining population — represents the most significant challenge to any country's long-term strategic position, more determinative than any particular policy choice. [[Video:0rALqcPWuH0|Civilization #53: Dostoevsky and the Soul of Russia]] draws parallels between Russian and Japanese attempts to navigate the transition from traditional to modern society, noting that both civilizations maintained stronger cultural coherence through the transition than Western Europe, but at the cost of different vulnerabilities.

Japan's relationship with the United States and China forms the strategic context for his contemporary analysis. He argues that America's alliance system in Asia depends fundamentally on Japanese cooperation, and that any reconfiguration of the regional order must account for Japanese interests. Japan's post-war constitutional constraints on military development, in his view, represent a temporary accommodation to American dominance that may be revisited as regional dynamics shift. His predictions for Japan's role in the emerging multipolar order emphasize that Japan's technological capabilities, social discipline, and institutional capacity give it resources that most other nations cannot match — the question is whether its political system can mobilize these resources effectively in the new strategic environment.""",

    "Ukraine": """Professor Jiang's analysis of Ukraine draws from 87 videos where he frames the conflict as an inflection point in the broader decline of American hegemony rather than a discrete territorial dispute to be resolved through diplomatic engineering. His core argument, developed most directly in [[Video:AEPSUC-UQ5k|Geo-Strategy #9: Putin's War for the Soul of Russia]] and [[Video:_gH4PvIni5E|Civilization #END: The Decline and Fall of the American Empire]], is that the war in Ukraine represents a proxy conflict within the larger structural competition between a declining American hegemon and rising revisionist powers, and that the outcome will be determined less by battlefield dynamics than by which side exhausts its political will and fiscal capacity first.

He argues that Western policymakers fundamentally miscalculated Putin's strategic intentions and Russia's capacity for sustained conflict. In [[Video:ZgvAHZqaawA|Geo-Strategy Update #6: Is Putin the Ubermensch?]], he analyzes Putin as a strategic actor operating within a coherent worldview that prioritizes Russian security interests and the restoration of Russian great power status, rejecting Western characterizations of Putin as merely authoritarian or irrational. The war, in this framework, is not Putin's personal war but a structural response to NATO expansion and the perceived threat to Russian security interests that followed the Soviet collapse. This perspective suggests that the war cannot be resolved through regime change or diplomatic humiliation, but only through some accommodation that addresses Russian security concerns.

His predictions regarding the war's outcome emphasize the structural constraints on both sides. [[Video:Go1bMQKnJBQ|Geo-Strategy #11: The Second American Civil War]] examines how American domestic political fragmentation limits the duration and intensity of foreign commitment possible, while [[Video:0rALqcPWuH0|Civilization #53: Dostoevsky and the Soul of Russia]] analyzes Russian strategic culture's tolerance for sustained suffering and deferred gratification in ways that Western political systems cannot match. He predicts that Ukraine will ultimately be partitioned or forced into unfavorable negotiations, as neither total victory for Ukraine nor Russian conquest of the entire country is achievable given the constraints on both sides. The conflict accelerates American decline by depleting resources that could otherwise maintain global commitments, while demonstrating Russian capacity for sustained strategic competition.""",

    "Gold": """Professor Jiang's analysis of Gold draws from 93 videos where he connects historical monetary systems to his broader framework of civilizational cycles and great power competition. His core argument is that monetary integrity — the degree to which a currency maintains its value over time — serves as a reliable indicator of civilizational health. Empires that maintain currency discipline tend to sustain their power longer than those that inflate their currencies to delay difficult decisions, because currency debasement creates cascading effects that undermine social trust, savings behavior, and the elite consensus that holds complex societies together. His historical analysis ranges from Rome's debasement of the denarius to the seventeenth-century financial revolutions that enabled Dutch and British hegemony.

His treatment of the gold standard in [[Video:3751ZjwmrBw|Civilization #40: Church and Empire]] traces how the informal gold standard of the early modern period constrained government spending and monetary manipulation in ways that forced rulers to make difficult fiscal decisions rather than defer them through inflation. The abandonment of the gold standard, in his analysis, enabled unprecedented levels of government spending and debt that have become structural features of modern economies, but that create new vulnerabilities when confidence in fiat currencies erodes. [[Video:35HRPLVyF0g|Game Theory #4: The Immigration Trap]] connects monetary policy to demographic dynamics, arguing that the welfare state's unfunded liabilities represent a form of currency debasement that future generations will be forced to confront.

He applies this framework to contemporary predictions in videos such as [[Video:ORyCS0r2Tpg|Jiang Xueqin: Predictions for 2026]] and [[Video:GJf0g2EFQ30|What the Next 2 to 4 Years Look Like]], arguing that the combination of fiscal recklessness, demographic decline, and the loss of manufacturing capacity creates conditions for a monetary crisis that will accelerate the loss of American hegemonic status. His specific predictions regarding gold and silver prices are grounded in historical precedent: during periods of monetary crisis and empire decline, precious metals historically surge as investors flee fiat currencies. He connects the monetary dimension to his geopolitical analysis, arguing that a monetary crisis would fundamentally reconfigure the great power competition by undermining the dollar's role as the world's reserve currency — a change that would reduce American fiscal capacity to maintain global commitments and accelerate the multipolar reordering he predicts across other topic areas."""
}

def main():
    topics = ["Civilization", "Strategy", "Islam", "Christianity", "Nuclear", "India", "Japan", "Ukraine", "Gold"]

    data = load_data()
    updated = 0

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"Processing: {topic}")
        print(f"{'='*60}")

        videos = get_topic_videos(data, topic)
        print(f"Found {len(videos)} videos for {topic}")

        # Get top videos for the videos referenced section
        top_ids = [v['id'] for v in videos[:8]]
        video_links = []
        for v in videos[:8]:
            title = v['title'][:70]
            video_links.append(f'*[[Video:{v["id"]}|{title}]]*')

        # Build full comment
        comment_text = COMMENTS.get(topic, f"Analysis of {topic} from Professor Jiang's Predictive History series.")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')

        full_comment = f"""== {timestamp} ==

{comment_text}

== Videos Referenced ==
{chr(10).join(video_links)}"""

        # Read existing content
        title = f"Talk:{topic}"
        existing = get_api_content(title)
        print(f"Existing content length: {len(existing)}")

        # Append new content
        new_content = existing + "\n\n" + full_comment if existing else full_comment

        # Write via PHP
        summary = f"Adding video analysis for {topic}"
        result = write_via_php(title, new_content, summary)
        print(f"Write result: {result.strip()}")

        if 'done' in result.lower() or 'saved' in result.lower():
            print(f"✓ Updated Talk:{topic}")
            updated += 1
        else:
            print(f"✗ Issue writing Talk:{topic}: {result[:300]}")

    print(f"\n\nTotal Talk pages updated: {updated}/{len(topics)}")

if __name__ == '__main__':
    main()
