# DSPTCH Design website

Static site for dsptchdesign.com. No framework, no build step on Netlify.

- `src/` is the source: `build.py` (pages, projects, packages), `styles.css`, `site.js`, `posts/` (blog articles in Markdown) and `images/`.
- `site/` is the generated website that Netlify publishes. Don't edit it by hand.

To change anything, edit `src/` and run `python3 src/build.py` (needs `markdown` and `pyyaml`).

Forms (Start a Project, website offer) use Netlify Forms. Old WordPress URLs are redirected in `site/_redirects`.

Site by DSPTCH Design.
