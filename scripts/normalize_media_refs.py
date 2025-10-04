#!/usr/bin/env python3
"""
Normalize image/audio references in docs/source markdown files.
- Fix image filenames to match files in docs/source/images (case-sensitive match best-effort).
- Convert image syntax that points to audio files (*.mp3, *.wav) into plain links: [caption](path)
- Backup original files as .bak before overwriting.
- Print a concise report of changes.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "source"
IMG_DIR = SOURCE / "images"

img_files = {p.name: p.name for p in IMG_DIR.iterdir() if p.is_file()}
# Also create a lowercase map for case-insensitive matching
img_files_lower = {p.name.lower(): p.name for p in IMG_DIR.iterdir() if p.is_file()}

md_files = sorted(SOURCE.glob("*.md"))

img_md_re = re.compile(r"(!\[([^\]]*)\])\(([^)]+)\)")
changes = []

for md in md_files:
    text = md.read_text(encoding="utf-8")
    orig = text
    def repl(m):
        full, alttext, path = m.group(1), m.group(2), m.group(3)
        # Only handle relative paths (images/ or sounds/)
        p = path.strip()
        if p.startswith("images/"):
            fname = p.split('/')[-1]
            # Exact match ok
            if fname in img_files:
                return m.group(0)
            # try case-insensitive
            if fname.lower() in img_files_lower:
                correct = img_files_lower[fname.lower()]
                newpath = p.replace(fname, correct)
                changes.append((md.name, p, newpath, 'fixed-case'))
                return f"{full}({newpath})"
            # try common extensions
            base = '.'.join(fname.split('.')[:-1]) if '.' in fname else fname
            for ext in ['jpg','jpeg','png','gif']:
                cand = f"{base}.{ext}"
                if cand in img_files_lower:
                    correct = img_files_lower[cand]
                    newpath = p.replace(fname, correct)
                    changes.append((md.name, p, newpath, 'fixed-ext'))
                    return f"{full}({newpath})"
            # not found
            changes.append((md.name, p, p, 'missing'))
            return m.group(0)
        elif p.lower().endswith(('.mp3','.wav','.ogg')):
            # Convert image markdown pointing to audio into a normal link
            new = f"[{alttext}]({p})"
            changes.append((md.name, p, p, 'audio-as-image->link'))
            return new
        else:
            return m.group(0)

    newtext = img_md_re.sub(repl, text)
    if newtext != orig:
        bak = md.with_suffix(md.suffix + '.bak')
        bak.write_text(orig, encoding='utf-8')
        md.write_text(newtext, encoding='utf-8')

# Print report
print('Normalization run complete. Summary:')
from collections import defaultdict
summary = defaultdict(int)
for t in changes:
    summary[t[3]] += 1
for k,v in summary.items():
    print(f" - {k}: {v}")
if changes:
    print('\nDetailed changes (first 30):')
    for c in changes[:30]:
        print(c)
else:
    print('No changes made.')
