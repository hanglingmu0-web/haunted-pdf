"""Verify the byte identity of the three supplied PDFs."""
from pathlib import Path
import hashlib

root = Path(__file__).resolve().parents[1]
for line in (root/'SHA256SUMS.txt').read_text(encoding='ascii').splitlines():
    expected, name = line.split('  ', 1)
    actual = hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Hash mismatch: {name}')
    print(f'OK {name}')
