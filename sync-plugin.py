import sys, json, os
import requests

# `safe` and convenient request.get
def Get(target, url):
    print("Getting %s" % target)
    res = requests.get(url)
    if res.status_code != 200:
        print("Error: Get %s failed..." % target, file=sys.stderr)
        exit(0)
    return res.text

res = Get("obsidian plugins","https://raw.githubusercontent.com/obsidianmd/obsidian-releases/refs/heads/master/community-plugins.json")
maps={}
for obj in json.loads(res):
    maps[obj['id']]=obj['repo']

PLUGIN_DIR = 'vault/.obsidian/plugins'
VALID_FILES = ['manifest.json', 'main.js', 'styles.css']
for plugin_id in os.listdir(PLUGIN_DIR):
    repo = maps[plugin_id]
    res = Get(f"Plugin {plugin_id} from {repo}", f"https://api.github.com/repos/{repo}/releases/latest")
    for asset in json.loads(res)['assets']:
        name = asset["name"]
        destination = f"{PLUGIN_DIR}/{plugin_id}/{name}"
        if name not in VALID_FILES: continue
        if os.path.exists(destination): 
            print(f"File {destination} exists, pass")
            continue
        with open(destination, 'w') as f:
            f.write(Get(name, asset["browser_download_url"]))
