import json, urllib.request, urllib.parse, ssl, http.cookiejar, hashlib, time, glob, os

ctx = ssl._create_unverified_context()

API = "https://localhost/api.php"

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
# Context is set on the handler, not on open()
opener.add_handler(urllib.request.HTTPSHandler(context=ctx))

def api_post(data):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(API, data=encoded, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with opener.open(req) as r:
        return json.loads(r.read())

def api_get(params):
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params))
    with opener.open(req) as r:
        return json.loads(r.read())

print("Getting login token...")
d = api_get({"action": "query", "meta": "tokens", "lgname": "admin", "format": "json"})
logintoken = d["query"]["tokens"].get("logintoken", "")
print(f"logintoken: {logintoken}")

if logintoken:
    result = api_post({"action": "login", "lgname": "admin", "lgpassword": "WikiPass123", "lgtoken": logintoken, "format": "json"})
    print(f"Login result: {result}")

d = api_get({"action": "query", "meta": "tokens", "format": "json"})
csrf = d["query"]["tokens"]["csrftoken"]
print(f"CSRF: {csrf}")

def upload_file(filename, filepath):
    with open(filepath, "rb") as f:
        filedata = f.read()
    boundary = "----WebKitFormBoundary" + hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
    parts = [
        b"--" + boundary.encode(),
        f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode(),
        b"Content-Type: image/png",
        b"",
        filedata,
        b"--" + boundary.encode(),
        b'Content-Disposition: form-data; name="action"',
        b"upload",
        b"--" + boundary.encode(),
        b'Content-Disposition: form-data; name="token"',
        csrf.encode(),
        b"--" + boundary.encode(),
        b'Content-Disposition: form-data; name="format"',
        b"json",
        b"--" + boundary.encode() + b"--",
        b"",
    ]
    body = b"\r\n".join(parts)
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "multipart/form-data; boundary=" + boundary})
    try:
        with opener.open(req) as r:
            result = json.loads(r.read())
            rv = result.get("upload", {}).get("result", "unknown")
            print(f"  {rv}: {filename}")
    except Exception as e:
        print(f"  ERROR {filename}: {e}")

print("\nUploading images...")
for filepath in sorted(glob.glob("/var/lib/mediawiki/images/*.png")):
    filename = os.path.basename(filepath)
    print(f"Uploading {filename}...")
    upload_file(filename, filepath)

print("\nDone!")