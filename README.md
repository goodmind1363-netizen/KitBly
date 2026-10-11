# Kitbly

Static, trilingual (EN / FR / DE) tools website.

- `content/<lang>/*.md` – articles (edit them in Pages CMS or directly on GitHub)
- `build.py` – generates the whole site into `dist/` (Python 3, no dependencies)
- `src/toolbench.html` – source of the shared texts, styles and slider script
- `static/t/` – self-hosted PDF libraries used by the PDF compressor
- `.pages.yml` – Pages CMS configuration (the admin panel)
- `wrangler.jsonc` – Cloudflare deployment settings

Build locally: `python3 build.py`

Cloudflare build command: `python3 build.py`
