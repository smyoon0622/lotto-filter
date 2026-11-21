"""Append newly drawn rounds to data/draws.json (run by GitHub Actions)."""
import json, urllib.request, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / 'data' / 'draws.json'
if not P.exists():  # first run: start from the data embedded in index.html
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    P.parent.mkdir(exist_ok=True)
    P.write_text(re.search(r'<script id="seed"[^>]*>(.*?)</script>', html, re.S).group(1).strip())
data = json.loads(P.read_text())
draws = data['draws']
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.dhlottery.co.kr/lt645/result'}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8'))


def fetch_round(n):
    """Return [6 numbers sorted] + [bonus] for round n, or None if not drawn yet."""
    js = get(f'https://www.dhlottery.co.kr/lt645/selectPstLt645InfoNew.do?srchDir=center&srchLtEpsd={n}')
    for it in (js.get('data') or {}).get('list') or []:
        if int(it.get('ltEpsd', 0)) == n:
            return sorted(int(it[f'tm{i}WnNo']) for i in range(1, 7)) + [int(it['bnsWnNo'])]
    return None


added = 0
nxt = max(int(k) for k in draws) + 1
while True:
    try:
        row = fetch_round(nxt)
    except Exception as e:
        print('stop:', e); break
    if not row:
        break
    draws[str(nxt)] = row; print('added', nxt, row); added += 1; nxt += 1
if added:
    P.write_text(json.dumps(data, separators=(',', ':')))
print('added rounds:', added)
