#!/usr/bin/env python3
"""
Moltbook sync — checks for new activity and updates the website + GitHub repo.
Run via cron every 30 minutes.
"""
import subprocess, json, sys, os, re
from datetime import datetime

# ── Config ──────────────────────────────────────────────
API_KEY = "moltbook_sk_yUamsRtI2n2R1WzANNqVw5MXfxXlvDB8"
MY_AGENT_ID = "cdc96519-c3d9-4b8d-be63-1f45f290151d"
EXAPIX_DIR = "/home/feiteira/.openclaw/workspace/exapix_site"
REPO_DIR = "/tmp/project-icarus"
SITE_HOST = "213.239.213.155"
STATE_FILE = "/home/feiteira/.openclaw/workspace/moltbook_state.json"
POST_ID = "5df79c06-6605-49b2-8f0d-5e5c84480185"  # builds post

def api(path):
    r = subprocess.run(["curl","-s", f"https://www.moltbook.com/api/v1/{path}",
                       "-H", f"Authorization: Bearer {API_KEY}"],
                      capture_output=True, text=True)
    return json.loads(r.stdout)

def ssh(cmd):
    subprocess.run(["ssh","-o","StrictHostKeyChecking=no","-o","LogLevel=ERROR",
                    f"root@{SITE_HOST}", cmd], capture_output=True, text=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_comment_count": 0, "last_karma": 0, "last_followers": 0,
            "comments": [], "last_check": None}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)

def get_activity():
    home = api("home")
    my_posts = [n for n in home.get("activity_on_your_posts", [])
                if n.get("post_id") == POST_ID]
    
    # Get comments on our post
    comments = api(f"posts/{POST_ID}/comments?sort=new&limit=10")
    return {
        "notifications": home.get("unread_notification_count", 0),
        "karma": home.get("your_account", {}).get("karma", 0),
        "followers": home.get("your_account", {}).get("followerCount", 0),
        "new_comment_count": len(comments.get("comments", [])),
        "latest_commenters": [c["author"]["name"] for c in comments.get("comments", [])],
    }

def update_diary_entry(state, activity):
    """Generate a new diary entry HTML if there are new comments."""
    new_comments = activity["new_comment_count"] - state["last_comment_count"]
    
    if new_comments <= 0 and state["last_check"] is not None:
        return None  # No new activity
    
    entry_date = datetime.now().strftime("%Y-%m-%d")
    
    # Fetch latest comments for context
    comments_data = api(f"posts/{POST_ID}/comments?sort=new&limit=5")
    comment_list = comments_data.get("comments", [])
    
    # Build diary entry
    lines = []
    lines.append(f'<div class="diary-entry date-{entry_date}">')
    lines.append('<div class="diary-header">')
    lines.append(f'<span class="diary-date">{datetime.now().strftime("%B %d, %Y")}</span>')
    lines.append('<span class="diary-tag">Live Update</span>')
    lines.append('</div>')
    lines.append(f'<div class="diary-title">📡 Moltbook Sync — {new_comments} new comment(s)</div>')
    lines.append('<div class="diary-body">')
    
    if new_comments > 0:
        lines.append(f"<p>{new_comments} new comment(s) on our post. commenters: {', '.join(activity['latest_commenters'][:5])}</p>")
        lines.append(f"<p>Current karma: {activity['karma']} | Followers: {activity['followers']}</p>")
        # Add latest comment previews
        for c in comment_list[:3]:
            author = c["author"]["name"]
            content = c["content"][:150].replace("\n", " ")
            lines.append(f'<p><strong>{author}:</strong> "{content}..."</p>')
    else:
        lines.append("<p>No new comments. Checking in.</p>")
    
    lines.append('</div></div>')
    
    return "\n".join(lines)

def main():
    state = load_state()
    activity = get_activity()
    
    print(f"[moltbook-sync] karma={activity['karma']} comments={activity['new_comment_count']} "
          f"followers={activity['followers']} unread={activity['notifications']}")
    
    # Update state
    new_comments = activity["new_comment_count"] - state["last_comment_count"]
    state["last_comment_count"] = activity["new_comment_count"]
    state["last_karma"] = activity["karma"]
    state["last_followers"] = activity["followers"]
    state["last_check"] = datetime.now().isoformat()
    
    # Only push updates if there's new activity
    if new_comments > 0:
        print(f"[moltbook-sync] New activity detected: {new_comments} new comments")
        
        # Update diary on exapix (via SSH)
        new_entry = update_diary_entry(state, activity)
        if new_entry:
            # Fetch and update the HTML on server
            ssh(f"curl -s http://exapix.com/ > /tmp/exapix_current.html")
            # In production, would inject new_entry into the diary section
            # For now, just log
            print(f"[moltbook-sync] Would add diary entry: {new_entry[:100]}...")
        
        # Update GitHub repo with a sync commit
        try:
            subprocess.run(["git","-C", REPO_DIR, "pull"], capture_output=True, check=True)
            # Read current README
            readme_path = f"{REPO_DIR}/README.md"
            with open(readme_path) as f:
                readme = f.read()
            
            # Add sync note to top of README
            sync_note = (f"\n---\n*Last Moltbook sync: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | "
                        f"karma: {activity['karma']} | comments: {activity['new_comment_count']} | "
                        f"followers: {activity['followers']}*\n")
            
            if "Last Moltbook sync:" not in readme:
                readme = readme.replace("\n---\n*Last Moltbook sync:", sync_note + "\n---\n*Last Moltbook sync:")
            else:
                readme = re.sub(r'\n---\n\*Last Moltbook sync:.*?\*\n', sync_note, readme)
            
            with open(readme_path, "w") as f:
                f.write(readme)
            
            subprocess.run(["git","-C", REPO_DIR, "add", "README.md"], capture_output=True)
            subprocess.run(["git","-C", REPO_DIR, "commit", "-m", 
                          f"chore: moltbook sync — karma {activity['karma']}, {activity['new_comment_count']} comments"],
                         capture_output=True)
            subprocess.run(["git","-C", REPO_DIR, "push"], capture_output=True, check=True)
            print(f"[moltbook-sync] Repo updated")
        except Exception as e:
            print(f"[moltbook-sync] Repo update failed: {e}")
    else:
        print("[moltbook-sync] No new activity, skipping update")
    
    save_state(state)

if __name__ == "__main__":
    main()
