#!/bin/bash

COOKIES=/tmp/mediawiki_cookies.txt

# Step 1: Get login token
LOGIN_RESP=$(curl -sk "https://localhost/api.php?action=query&meta=tokens&type=login&format=json")
echo "Step 1 response: $LOGIN_RESP"

LOGIN_TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['query']['tokens']['logintoken'])")
echo "Login token: [$LOGIN_TOKEN]"

# Step 2: Login
LOGIN_RESULT=$(curl -sk -X POST "https://localhost/api.php" \
  --data "action=login&lgname=admin&lgpassword=WikiPass123&lgtoken=${LOGIN_TOKEN}&format=json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c "$COOKIES" -b "$COOKIES")
echo "Login result: $LOGIN_RESULT"

# Step 3: Get CSRF with cookies
CSRF_RESP=$(curl -sk "https://localhost/api.php?action=query&meta=tokens&format=json" -b "$COOKIES")
echo "CSRF response: $CSRF_RESP"

CSRF=$(echo "$CSRF_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['query']['tokens']['csrftoken'])")
echo "CSRF: [$CSRF]"

# Step 4: Upload with cookies
echo "Uploading china.png..."
UPLOAD_RESULT=$(curl -sk -X POST "https://localhost/api.php" \
  -b "$COOKIES" \
  -F "file=@/var/lib/mediawiki/images/china---83553628-36cd-4653-9c83-b55815bcce7b.png" \
  -F "filename=china.png" \
  -F "action=upload" \
  -F "token=${CSRF}" \
  -F "format=json")
echo "Upload result: $UPLOAD_RESULT"

# Upload all remaining images
for filepath in /var/lib/mediawiki/images/*.png; do
    filename=$(basename "$filepath")
    # Clean name without uuid suffix
    clean=$(echo "$filename" | sed 's/---.*$/.png/')
    echo "Uploading $clean..."
    RESULT=$(curl -sk -X POST "https://localhost/api.php" \
      -b "$COOKIES" \
      -F "file=@$filepath" \
      -F "filename=$clean" \
      -F "action=upload" \
      -F "token=${CSRF}" \
      -F "format=json")
    echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('upload',{}).get('result','?') + ': ' + d.get('upload',{}).get('file',{}).get('title', d.get('error',{}).get('info','?')))" 2>/dev/null || echo "parse error"
done

echo "Done!"