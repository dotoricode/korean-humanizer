#!/usr/bin/env python3
"""Build a text-only skill ZIP with local runtime references and pinned evidence links."""
import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
FILES = ['SKILL.md', 'LICENSE', 'PROMPT.md', 'PROMPT.short.md',
         'references/ko-ai-signals.md', 'examples/before-after.md',
         'examples/personal-list.md', 'examples/brand-voice-template.md',
         'examples/brand-voice-toss-style.md', 'examples/brand-voice-essayist.md']
FILES += sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'examples').glob('domain-*.md'))
LINK = re.compile(r'(?<!!)\[([^\]]+)\]\(([^\s)]+)\)')


def build(output):
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    contents = {name: (ROOT / name).read_text() for name in FILES}
    contents['README.md'] = (ROOT / 'docs/distribution/PACKAGE-README.md').read_text()
    rewritten = []
    for name, source in list(contents.items()):
        def replace(match):
            label, target = match.groups()
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                return match.group(0)
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), parts.path))
            if resolved in contents:
                return match.group(0)
            if not (ROOT / resolved).is_file():
                raise ValueError(f'Unresolved link: {name} -> {target}')
            url = f'https://github.com/dotoricode/korean-humanizer/blob/{commit}/{resolved}'
            if parts.fragment:
                url += '#' + parts.fragment
            rewritten.append({'file': name, 'target': target, 'url': url})
            return f'[{label}]({url})'
        contents[name] = LINK.sub(replace, source)
    contents = {name: value.encode() for name, value in contents.items()}
    manifest = {'source_commit': commit, 'source_file_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}, 'files': {
        name: hashlib.sha256(value).hexdigest() for name, value in sorted(contents.items())},
        'external_evidence_links': rewritten}
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'korean-humanizer-main-{commit[:7]}.zip'
    with ZipFile(archive, 'w', ZIP_DEFLATED) as zf:
        for name, value in sorted(contents.items()):
            info = ZipInfo(name, (2026, 10, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, value)
    with ZipFile(archive) as zf:
        assert zf.testzip() is None
        assert all(hashlib.sha256(zf.read(name)).hexdigest() == digest
                   for name, digest in manifest['files'].items())
        assert zf.read('SKILL.md') == (ROOT / 'SKILL.md').read_bytes()
        assert zf.read('LICENSE') == (ROOT / 'LICENSE').read_bytes()
    manifest['archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(archive)
    print(f'{len(contents)} text files; archive and runtime instruction checks passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    build(parser.parse_args().output_dir)
