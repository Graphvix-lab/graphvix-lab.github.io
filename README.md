# GraphViX Lab

The website of GraphViX Lab, led by Changjian Li in the School of Informatics at the University of Edinburgh.

**Website:** https://graphvix-lab.github.io/

## Edit and preview

The site is static HTML, CSS and JavaScript. Python's standard library generates the pages; there is no JavaScript build dependency.

```sh
python3 build.py
python3 -m http.server 8766 --bind 127.0.0.1
```

Visit http://127.0.0.1:8766/.

- `content.json`: home introduction, featured research, research directions, people, alumni and news.
- `publications.json`: complete publication records, source links and Research page assignments. Set `research.show_on_research` to `false` to keep a paper only in Publications.
- `build.py`: shared page layout, metadata, 404 page and sitemap generation.
- `assets/site.css`: typography, colours, spacing and responsive layout.
- `assets/site.js`: navigation, publication filters and video controls.
- `SOURCES.md`: content and media attribution.

After changing content or templates, run `python3 build.py` and commit both the sources and generated files. Push to `main` to publish through GitHub Pages. Pages serves the repository root; `.nojekyll` preserves the static files without Jekyll processing.

## Images

Original assets are retained alongside optimised images. If images change, install Pillow, run `python3 optimize_assets.py`, then `python3 build.py`. The image manifest maps original files to smaller versions. Ordinary content edits require only Python's standard library.

`assets/social-card.png` is the 1200 × 630 sharing image; its editable vector source is `assets/social-card.svg`.

## Content scope

Publications includes Changjian Li's earlier work and collaborations. Research presents four selected themes; each list runs from newest to oldest. Alumni destinations describe the next step recorded on the source homepage. Materials remain attributable to their original creators; see `SOURCES.md`.
