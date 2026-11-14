"""Verify archived artifact hashes and internal Markdown links using only stdlib."""
from pathlib import Path
import hashlib,json,re,urllib.parse
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'DELIVERABLES.json').read_text())
assert len(manifest['artifacts'])==manifest['core_count']==14
for a in manifest['artifacts']:
 p=root/a['path'];assert p.is_file(),a['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],a['id']
for md in root.glob('*.md'):
 for href in re.findall(r'\]\(([^)]+)\)',md.read_text()):
  if href.startswith(('https://','http://','#')):continue
  target=(md.parent/urllib.parse.unquote(href.split('#')[0])).resolve()
  assert target.exists(),(md.name,href)
assert not any(p.name.startswith('ppt-') for p in (root/'site').rglob('*'))
assert not list(root.rglob('project-overview.pdf'))
print('OK: 14 artifact checksums, documentation links and public-export scope.')
