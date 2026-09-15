import json, subprocess, os, sys

S = os.path.dirname(os.path.abspath(__file__))
d = json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.stage_verify_2.json'))
skip = set(sys.argv[1:])
for x in d:
    if x['id'] in skip or not x.get('lat'):
        continue
    if os.path.exists(f"{S}/{x['id']}_z18.png"):
        continue
    r = subprocess.run(['python3', f'{S}/wb.py', x['id'], str(x['lat']), str(x['lng']), '18', '2023-06,2024-06,latest'],
                       capture_output=True, text=True)
    print(x['id'], r.stdout.replace('\n', ' | '), r.stderr[-300:], flush=True)
