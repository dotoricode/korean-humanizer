#!/usr/bin/env python3
"""Build the Agensi MCP file payload with local runtime references and pinned evidence links."""
import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
# PROMPT.md and PROMPT.short.md stay on GitHub: MCP clients load the skill itself.
FILES = ['SKILL.md', 'LICENSE', 'references/ko-ai-signals.md', 'examples/before-after.md',
         'examples/personal-list.md', 'examples/brand-voice-template.md',
         'examples/brand-voice-toss-style.md', 'examples/brand-voice-essayist.md']
FILES += sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'examples').glob('domain-*.md'))
# Agensi submit_skill/update_skill accept at most 100 files and 5 MB.
MAX_FILES = 100
MAX_BYTES = 5 * 1024 * 1024
LINK = re.compile(r'(?<!!)\[([^\]]+)\]\(([^\s)]+)\)')


def build(output):
    status = subprocess.check_output(
        ['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=ROOT, text=True)
    if status:
        raise ValueError('Packaging requires a clean source tree; commit source changes first.')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    source_names = FILES + ['docs/distribution/PACKAGE-README.md']
    sources = {name: subprocess.check_output(['git', 'show', f'{commit}:{name}'], cwd=ROOT)
               for name in source_names}
    contents = {name: sources[name].decode() for name in FILES}
    contents['README.md'] = sources['docs/distribution/PACKAGE-README.md'].decode()
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
            if subprocess.run(['git', 'cat-file', '-e', f'{commit}:{resolved}'], cwd=ROOT,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
                raise ValueError(f'Unresolved link: {name} -> {target}')
            url = f'https://github.com/dotoricode/korean-humanizer/blob/{commit}/{resolved}'
            if parts.fragment:
                url += '#' + parts.fragment
            rewritten.append({'file': name, 'target': target, 'url': url})
            return f'[{label}]({url})'
        contents[name] = LINK.sub(replace, source)
    contents = {name: value.encode() for name, value in contents.items()}
    manifest = {'source_commit': commit, 'source_file_sha256': {name: hashlib.sha256(value).hexdigest() for name, value in sources.items()}, 'files': {
        name: hashlib.sha256(value).hexdigest() for name, value in sorted(contents.items())},
        'external_evidence_links': rewritten}
    if len(contents) > MAX_FILES or sum(map(len, contents.values())) > MAX_BYTES:
        raise ValueError(f'Package exceeds the Agensi limit of {MAX_FILES} files / {MAX_BYTES} bytes.')
    payload = {'skill_slug': 'korean-humanizer', 'files': [
        {'path': name, 'content': value.decode()} for name, value in sorted(contents.items())]}
    assert contents['SKILL.md'] == sources['SKILL.md']
    assert contents['LICENSE'] == sources['LICENSE']
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode()
    output.mkdir(parents=True, exist_ok=True)
    payload_file = output / f'korean-humanizer-{commit[:7]}.agensi.json'
    payload_file.write_bytes(data)
    manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(payload_file)
    print(f'{len(contents)} text files; Agensi MCP payload and runtime instruction checks passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    build(parser.parse_args().output_dir)
