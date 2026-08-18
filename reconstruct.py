import base64, hashlib, json
from pathlib import Path

root = Path("chunks-v2")
manifest = json.loads((root / "manifest.json").read_text())
out_dir = Path(".")
for item in manifest:
    pieces = []
    for part in item["parts"]:
        p = root / part["name"]
        text = p.read_text()
        got = hashlib.sha256(text.encode()).hexdigest()[:16]
        if got != part["sha256_16"]:
            raise SystemExit(f"chunk hash mismatch {p}: {got} != {part['sha256_16']}")
        pieces.append(text)
    b64 = "".join(pieces).replace("\n", "").replace("\r", "")
    if len(b64) != item["b64_len"]:
        raise SystemExit(f"b64 length {item['file']}: {len(b64)} != {item['b64_len']}")
    data = base64.b64decode(b64, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if digest != item["jpeg_sha256"]:
        raise SystemExit(f"jpeg hash {item['file']}: {digest} != {item['jpeg_sha256']}")
    dest = out_dir / item["file"]
    dest.write_bytes(data)
    print("wrote", dest, len(data))
print("ok")
