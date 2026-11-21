"""Append newly drawn rounds to data/draws.json (run weekly by GitHub Actions)."""
import json, urllib.request, sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'draws.json'
if not P.exists():  # first run: start from the data embedded in index.html
    import re
    html = (P.parent.parent / 'index.html').read_text(encoding='utf-8')
    P.parent.mkdir(exist_ok=True)
    P.write_text(re.search(r'<script id="seed"[^>]*>(.*?)</script>', html, re.S).group(1).strip())
data = json.loads(P.read_text())
draws = data['draws']; nxt = max(int(k) for k in draws) + 1; added = 0
while True:
    url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={nxt}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        js = json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8'))
    except Exception as e:
        print('stop:', e); break
    if js.get('returnValue') != 'success': break
    nums = sorted(js[f'drwtNo{i}'] for i in range(1, 7))
    draws[str(nxt)] = nums + [js['bnusNo']]; print('added', nxt, draws[str(nxt)]); added += 1; nxt += 1
if added:
    P.write_text(json.dumps(data, separators=(',', ':')))
print('added rounds:', added)
