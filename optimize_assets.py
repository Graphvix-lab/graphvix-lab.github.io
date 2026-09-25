"""Generate display-sized WebP copies. Requires Pillow; originals stay intact."""
import json
from hashlib import sha1
from pathlib import Path
from PIL import Image, ImageOps, ImageSequence

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())
papers = json.loads((ROOT / 'publications.json').read_text())
portraits = {'assets/' + person['image'] for person in data['people']}
sources = {paper['image'] for paper in papers} | portraits
output = ROOT / 'assets/optimized'
output.mkdir(exist_ok=True)
manifest = {}
for source in sorted(sources):
    original = ROOT / source
    bounds = (360, 480) if source in portraits else (960, 720)
    digest = sha1(original.read_bytes() + str(bounds).encode() + b'webp-q85-v1').hexdigest()[:12]
    target = output / (original.stem + '-' + digest + '.webp')
    with Image.open(original) as image:
        animated = getattr(image, 'n_frames', 1) > 1
        frames, durations = [], []
        for frame in ImageSequence.Iterator(image):
            duration = frame.info.get('duration', 100)
            resized = ImageOps.exif_transpose(frame).convert('RGBA')
            resized.thumbnail(bounds, Image.Resampling.LANCZOS)
            frames.append(resized)
            durations.append(duration)
        if not target.exists() or not target.stat().st_size:
            options = dict(format='WEBP', quality=85, method=6)
            if animated:
                options.update(save_all=True, append_images=frames[1:], duration=durations,
                               loop=image.info.get('loop', 0))
            frames[0].save(target, **options)
        # Keep the original when encoding does not save bytes.
        chosen = target if target.stat().st_size < original.stat().st_size else original
        if chosen == original:
            target.unlink()
        with Image.open(chosen) as final:
            width, height = final.size
        manifest[source] = dict(src=chosen.relative_to(ROOT).as_posix(), width=width,
                                height=height, original_bytes=original.stat().st_size,
                                bytes=chosen.stat().st_size, animated=animated)
    print(f'{source}: {manifest[source]["original_bytes"]:,} → {manifest[source]["bytes"]:,}', flush=True)
(ROOT / 'assets/image-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
before = sum(item['original_bytes'] for item in manifest.values())
after = sum(item['bytes'] for item in manifest.values())
print(f'Total: {before:,} → {after:,} bytes ({1-after/before:.1%} smaller)')
