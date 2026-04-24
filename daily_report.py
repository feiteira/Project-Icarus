#!/usr/bin/env python3
"""
Daily morning report — summarizes last 24h of Moltbook activity and project stats.
Sends report to Telegram group chat.
"""
import subprocess, json, os
from datetime import datetime

API_KEY = "moltbook_sk_yUamsRtI2n2R1WzANNqVw5MXfxXlvDB8"
SITE_HOST = "213.239.213.155"
STATE_FILE = "/home/feiteira/.openclaw/workspace/moltbook_state.json"
POST_ID = "5df79c06-6605-49b2-8f0d-5e5c84480185"
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Will be injected from env or config
CHAT_ID = "-1003944840912"

def api(path):
    r = subprocess.run(["curl","-s", f"https://www.moltbook.com/api/v1/{path}",
                       "-H", f"Authorization: Bearer {API_KEY}"],
                      capture_output=True, text=True)
    return json.loads(r.stdout)

def ssh(cmd):
    r = subprocess.run(["ssh","-o","StrictHostKeyChecking=no","-o","LogLevel=ERROR",
                        f"root@{SITE_HOST}", cmd],
                       capture_output=True, text=True)
    return r.stdout.decode()

def get_moltbook_stats():
    """Get current stats and compare to last known state."""
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    
    home = api("home")
    my_posts = home.get("activity_on_your_posts", [])
    builds_activity = [n for n in my_posts if n.get("post_id") == POST_ID]
    
    comments = api(f"posts/{POST_ID}/comments?sort=new&limit=10")
    comment_list = comments.get("comments", [])
    
    account = home.get("your_account", {})
    
    return {
        "karma": account.get("karma", 0),
        "followers": account.get("followerCount", 0),
        "total_comments": len(comment_list),
        "commenters": list({c["author"]["name"] for c in comment_list}),
        "notifications": home.get("unread_notification_count", 0),
        "last_state": state,
    }

def get_site_stats():
    """Get visit counter from site."""
    try:
        counter = ssh("curl -s http://exapix.com/counter.php")
        return int(counter.strip())
    except:
        return None

def build_report(stats, site_visits):
    lines = []
    lines.append("🌅 *Good morning from Clawdia — Daily Icarus Report*")
    lines.append(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    lines.append("")
    
    # Moltbook stats
    s = stats
    old_state = s.get("last_state", {})
    old_comments = old_state.get("last_comment_count", s["total_comments"])
    old_karma = old_state.get("last_karma", s["karma"])
    
    new_comments = s["total_comments"] - old_comments
    new_karma = s["karma"] - old_karma
    
    lines.append("🦞 *Moltbook Activity*")
    lines.append(f"  Karma: {s['karma']} ({'+' if new_karma >= 0 else ''}{new_karma})")
    lines.append(f"  Followers: {s['followers']}")
    lines.append(f"  Comments: {s['total_comments']} ({'+' if new_comments >= 0 else ''}{new_comments} new)")
    
    if s["commenters"]:
        lines.append(f"  Commenters: {', '.join(s['commenters'][:5])}")
    
    if new_comments > 0:
        lines.append("")
        lines.append("💬 *Latest comments:*")
        comments_data = api(f"posts/{POST_ID}/comments?sort=new&limit=3")
        for c in comments_data.get("comments", [])[:3]:
            author = c["author"]["name"]
            content = c["content"][:100].replace("\n", " ")
            lines.append(f"  • {author}: \"{content}...\"")
    
    # Site stats
    lines.append("")
    lines.append("🌐 *Website (exapix.com)*")
    if site_visits:
        lines.append(f"  Total visits: {site_visits}")
    lines.append(f"  Live: https://exapix.com")
    
    # GitHub
    lines.append("")
    lines.append("📦 *GitHub*")
    lines.append(f"  Repo: github.com/feiteira/Project-Icarus")
    
    # Next steps
    lines.append("")
    lines.append("📋 *Suggested next steps:*")
    if new_comments > 0:
        lines.append("  1. Reply to any new Moltbook comments")
    lines.append("  1. Review ouroboros_stack feedback on thrust measurement")
    lines.append("  2. Build simple thrust stand for voltage/thrust characterization")
    lines.append("  3. Consider: bigger wingspan? Ground demonstrator first?")
    
    lines.append("")
    lines.append("_Powered by Clawdia01 on OpenClaw_")
    
    return "\n".join(lines)

def main():
    stats = get_moltbook_stats()
    site_visits = get_site_stats()
    
    report = build_report(stats, site_visits)
    print(report)
    
    # Save state for next report
    state = {
        "last_comment_count": stats["total_comments"],
        "last_karma": stats["karma"],
        "last_followers": stats["followers"],
        "last_check": datetime.now().isoformat(),
        "site_visits": site_visits,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
    
    # Try to send via Telegram if bot token available
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if bot_token:
        tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        msg = report.replace("*", "✳️").replace("_", " ").replace("•", "•")
        subprocess.run(["curl","-s","-X","POST", tg_url,
                       "-d", f"chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"],
                      capture_output=True)

if __name__ == "__main__":
    main()
