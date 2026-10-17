# Layal Joumaa · ليال جمعة

Personal website for **Layal Joumaa**, CV & resume writer, LinkedIn optimisation specialist and personal-branding consultant.

**Live:** https://nouraldeentofi.github.io/layal-joumaa/

A static, bilingual (Arabic RTL by default, English) site of seven pages, built with plain HTML, CSS and JavaScript, no frameworks.

| Page | What's on it |
|---|---|
| `index.html` | Opening: a sample CV line is struck and rewritten with her red pen, the page folds into a paper plane and flies from Syria to where her clients work (the Gulf, Europe, the US), landing on her real LinkedIn headline. Then services, LinkedIn results, headline checker, a workshop slide, stories, FAQ |
| `services.html` | Six services with what each includes |
| `method.html` | How she works, plus an interactive career-shift checklist |
| `stories.html` | Client stories with a map of destinations |
| `about.html` | Her one-page CV (set from the site's own facts), timeline, certificates, skills and languages |
| `ideas.html` | Her LinkedIn ideas, filterable by topic |
| `contact.html` | Three taps to a ready first message; beside it a letter writes one line per answer and seals itself on copy |

**No photos of Layal**, by her choice: her mark is a pen nib over a stroke of ink, and the share image is a typographic card.

**Details:** the opening plays once per session (reduced motion, no JavaScript and later visits show the finished hero, with a replay button); a living marble background in WebGL that moves on its own; scroll-driven timelines; a mobile layout of its own (full-screen menu, swipe rows, floating message button); respects reduced-motion settings; self-hosted fonts (Readex Pro, Aref Ruqaa).

**Readable by AI assistants and search engines:** schema.org JSON-LD on every page (Person, Service, FAQ), `llms.txt`, `llms-full.txt`, `robots.txt` and `sitemap.xml`.

## Editing

All text lives in `build.py`, in Arabic and English. Change it, then run:

```bash
python3 build.py
```

The link-preview image `assets/img/og.jpg` (1200×630) is drawn by `python3 og.py` (needs Playwright for Python and Chrome); run it again if her name, headline or the map change.

Email and WhatsApp (optional) are set in `CONFIG` at the top of `assets/site.js`; empty values stay hidden.

## Moving to a custom domain (Cloudflare Pages)

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → pick this repo.
2. Framework preset: **None**. Build command: *(empty)*. Output directory: `/`.
3. After the first deploy: **Custom domains** → add the domain.
4. In `build.py` set `BASE_URL = "https://your-domain"`, run `python3 build.py`, commit and push. Cloudflare redeploys by itself.

---

Designed and built by [Nour Aldeen Tofi · نور الدين طفي](https://nouraldeentofi.com).
