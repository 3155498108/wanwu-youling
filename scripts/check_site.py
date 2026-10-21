from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT
(ROOT/'output').mkdir(exist_ok=True)
html=(APP/'index.html').read_text(encoding='utf-8')
(ROOT/'output'/'site-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',html).group(1),encoding='utf-8')
data=json.loads((APP/'process'/'creature-research.json').read_text(encoding='utf-8'))
for c in data:
    assert (APP/c['image']).is_file(),c['image']
print(f'{len(data)} images present; script extracted for node --check')
