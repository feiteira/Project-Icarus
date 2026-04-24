<?php
$guestbook_file = "/var/www/exapix/guestbook.txt";
$messages = @file($guestbook_file, FILE_IGNORE_NEW_LINES) ?: [];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = htmlspecialchars(substr(trim($_POST["name"] ?? "Anonymous"), 0, 50));
    $msg = htmlspecialchars(substr(trim($_POST["message"] ?? ""), 0, 500));
    if (strlen($msg) > 0) {
        $entry = date("Y-m-d H:i") . " | " . $name . " | " . $msg;
        file_put_contents($guestbook_file, $entry . PHP_EOL, FILE_APPEND);
        header("Location: /guestbook.php?added=1");
        exit;
    }
}
$added = $_GET["added"] ?? null;
?>
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Guest Book — Project Icarus</title>
<style>
body { background: #0a0e17; color: #f3f4f6; font-family: sans-serif; max-width: 700px; margin: 0 auto; padding: 2rem; }
h1 { color: #06b6d4; }
.entry { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
.meta { font-size: 0.75rem; color: #9ca3af; margin-bottom: 0.5rem; }
.msg { font-size: 0.9rem; }
form { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; }
input, textarea { width: 100%; background: #1a2332; border: 1px solid #1f2937; color: #f3f4f6; padding: 0.5rem; border-radius: 4px; margin-bottom: 0.75rem; box-sizing: border-box; }
button { background: #06b6d4; color: #0a0e17; border: none; padding: 0.6rem 1.5rem; border-radius: 6px; font-weight: 700; cursor: pointer; }
button:hover { opacity: 0.85; }
.success { background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.4); padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem; color: #10b981; }
a { color: #06b6d4; text-decoration: none; }
</style></head><body>
<p><a href="/">← Back to Project Icarus</a></p>
<h1>📖 Guest Book</h1>
<?php if ($added): ?><div class="success">Message added! Thanks for signing.</div><?php endif; ?>
<form method="POST">
<input name="name" placeholder="Your name (optional)" maxlength="50">
<textarea name="message" placeholder="Leave a message, question, or just say hi..." rows="4" required maxlength="500"></textarea>
<button type="submit">Sign Guest Book</button>
</form>
<?php
$msgs = array_reverse($messages);
foreach ($msgs as $line) {
    $parts = explode(" | ", $line, 3);
    if (count($parts) === 3) {
        echo "<div class=entry><div class=meta>" . htmlspecialchars($parts[0]) . " — <strong>" . htmlspecialchars($parts[1]) . "</strong></div><div class=msg>" . htmlspecialchars($parts[2]) . "</div></div>";
    }
}
if (empty($messages)) echo "<p style='color:#9ca3af;'>No messages yet. Be the first!</p>";
?>
</body></html>