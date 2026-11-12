"""Build a source-only archive; never bundle runtime classroom records."""
from pathlib import Path
import hashlib
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = {'groupmate', 'static', 'native', 'deploy', 'docs', 'tests', 'tools', '.github'}
FILES = {'README.md', '.gitignore', '.env.example', 'VERSION'}
BLOCKED = {'__pycache__', 'data', 'uploads', '.git', 'node_modules', 'private'}
EXTENSIONS = {'.py', '.js', '.css', '.html', '.md', '.json', '.txt', '.sh', '.conf', '.template', '.service', '.timer', '.yml', '.png'}

def release_files():
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(ROOT)
        if any(part in BLOCKED for part in rel.parts):
            continue
        if len(rel.parts) == 1:
            if rel.name not in FILES:
                continue
        elif rel.parts[0] not in FOLDERS or path.suffix not in EXTENSIONS:
            continue
        if path.name.startswith('.env') and path.name != '.env.example':
            raise ValueError('Environment file excluded: ' + str(rel))
        if path.suffix != '.png':
            content = path.read_text(encoding='utf-8')
            patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'\bgh[pousr]_[A-Za-z0-9]{30,}', r'\bsk-[A-Za-z0-9_-]{24,}']
            if any(re.search(pattern, content) for pattern in patterns):
                raise ValueError('Possible credential; review before packaging: ' + str(rel))
        yield path, rel

if __name__ == '__main__':
    paths = list(release_files())
    target = ROOT / 'dist' / 'GroupMate_AI_v2.0_GitHub_ready.zip'
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path, rel in paths:
            archive.write(path, 'GroupMate_AI_v2.0/' + rel.as_posix())
    print(f'{len(paths)} source files; SHA256 {hashlib.sha256(target.read_bytes()).hexdigest()}')
