#!/usr/bin/env python3
"""Builds the DSPTCH Design static site into ../site (Netlify-ready) and a preview entry page.

All projects live in PROJECTS below. To add a project: add one entry (and its images in
site/images/work/), then run:  python3 build.py
"""
import html, json, os, shutil, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "site"
EMAIL = "hello@dsptchdesign.com"

# ---------------------------------------------------------------- projects
# type: "website" or "creative".  basis: "Bespoke engagement" | "DSPTCH package" | "Concept"
# images: list of filenames in images/work/<slug>/ (first is the cover). Empty = placeholder.
PROJECTS = [
    # ---- Websites: DSPTCH concept sites (live). Shown first; label marks them as concepts.
    dict(slug='xenro', name='Xenro', type="website", label="Concept · Logistics", basis="Concept", url='https://xenro.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary='A freight, storage and distribution site with a quick-quote form in the hero and a clear path from first pickup to final handoff.', images=['01-cover.jpg', '02-home.jpg', '03-home-mid.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    dict(slug='alden-mercer', name='Alden & Mercer', type="website", label="Concept · Law", basis="Concept", url='https://alden-mercer.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary='A boutique business law firm site with an editorial serif voice, a practice-area guide and an insights section.', images=['01-cover.jpg', '02-home.jpg', '03-home-mid.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    dict(slug='vela-aesthetics', name='VELA Aesthetics', type="website", label="Concept · Med spa", basis="Concept", url='https://vela-aesthetics.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary='A New York med spa site built around a monumental wordmark, an editorial grid and calm, considered copy.', images=['01-cover.jpg', '02-home.jpg', '03-home-mid.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    dict(slug='davyn', name='DAVYN', type="website", label="Concept · Dental", basis="Concept", url='https://davyn.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary='A boutique dental studio site with framed photography, frosted navigation and a consultation flow that puts nervous patients at ease.', images=['01-cover.jpg', '02-home.jpg', '03-home-mid.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    dict(slug='arena', name='ARENA', type="website", label="Concept · Men's health", basis="Concept", url='https://arena-health.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary="A physician-led men's health and longevity clinic site, with photography that carries charge and copy built on restraint.", images=['01-cover.jpg', '02-home.jpg', '03-home-mid.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    dict(slug='qubik', name='QUBIK', type="website", label="Concept · Engineering", basis="Concept", url='https://qubik-ae.netlify.app',
         deliverables="Brand identity, copy, website design and build", color="#D9D5CF", featured=True,
         summary='An architectural engineering firm site for commercial and industrial building: hard edges and photography-led layouts.', images=['01-cover.jpg', '02-home.jpg', '04-page.jpg', '05-page.jpg', '06-page.jpg', '07-mobile.jpg', '08-mobile.jpg']),
    # ---- Creative: work carried over from the previous dsptchdesign.com (old WordPress slug in `old`)
    dict(slug='stussy', name='Stüssy', type="creative", label='Brand creative', basis="Bespoke engagement", old='stussy', upl='2025/01',
         deliverables='To confirm', color="#D6D3CC", images=['Stussy_S1.jpg', 'Stussy_S2.jpg', 'Stussy_S3.jpg', 'Stussy_S4.jpg', 'Stussy_S5.jpg', 'Stussy_S6.jpg', 'Stussy_S7.jpg']),
    dict(slug='bloved', name='Bloved', type="creative", label='Identity · Packaging · Website', basis="Bespoke engagement", old='bloved', upl='2021/06',
         deliverables='Logo identity, style guide, packaging, website', color="#D6D3CC", summary='A refreshed identity for a cannabis wellness brand made for women: a relaxed, natural voice with an upbeat, energetic look.', images=['Bloved_Mockup.jpg', 'Bloved_Logo.jpg', 'Bloved_homepage-u.jpg', 'Bloved_Cans04.jpg', 'Bloved_Cans03.jpg', 'Bloved_Cans02.jpg', 'Bloved_Cans01.jpg', 'bloved_brand-guide_05.jpg', 'bloved_brand-guide_04.jpg', 'bloved_brand-guide_03.jpg', 'bloved_brand-guide_02.jpg', 'bloved_brand-guide_01.jpg']),
    dict(slug='vitalitea', name='Vitalitea', type="creative", label='Packaging · Identity', basis="Bespoke engagement", old='vitalitea', upl='2023/02',
         deliverables='Visual identity and packaging', color="#D6D3CC", summary='Packaging for a CBD hemp beverage: bold type, striking imagery and a science-inspired palette built to earn trust on the shelf.', images=['Vitalitea_Mock-2.jpg', 'Vitalitea_Mock-1.jpg', 'Vitalitea_Mock-3.jpg']),
    dict(slug='twitch', name='Twitch', type="creative", label='Brand creative', basis="Bespoke engagement", old='twitch-dsptch', upl='2025/01',
         deliverables='To confirm', color="#D6D3CC", images=['TWITCH1.jpg', 'TWITCH2.jpg', 'TWITCH3.jpg', 'TWITCH4.jpg', 'TWITCH5.jpg', 'TWITCH6.jpg', 'TWITCH7.jpg']),
    dict(slug='lucid', name='Lucid', type="creative", label='Brand creative', basis="Bespoke engagement", old='lucid', upl='2025/01',
         deliverables='To confirm', color="#D6D3CC", images=['Lucid1.jpg', 'Lucid2.jpg', 'Lucid3.jpg', 'Lucid4.jpg', 'Lucid5.jpg', 'Lucid6.jpg', 'Lucid7.jpg', 'Lucid8.jpg', 'Lucid9.jpg', 'Lucid10.jpg', 'Lucid11.jpg']),
    dict(slug='mcds', name='MCDS', type="creative", label='Brand creative', basis="Bespoke engagement", old='mcds', upl='2025/01',
         deliverables='To confirm', color="#D6D3CC", images=['MD2.jpg', 'MD3.jpg', 'MD4.jpg', 'MD5.jpg', 'MD8.jpg', 'MD12.jpg', 'MD13.jpg', 'MD19.jpg']),
    dict(slug='rise-cannabis', name='Rise Cannabis', type="creative", label='Identity · Packaging · Website', basis="Bespoke engagement", old='rise-cannabis', upl='2023/02',
         deliverables='Rebrand, packaging, website', color="#D6D3CC", summary='A rebrand and new website for a multi-state cannabis brand, built to keep pace with a market where the rules keep changing.', images=['Rise_Mock-4.jpg', 'Rise_Mock-2.jpg', 'Rise_Mock-1.jpg', 'Rise_Mock-3.jpg', 'Rise_Mock-7.jpg', 'Rise_Mock-6.jpg', 'Rise_Mock-5.jpg']),
    dict(slug='oars-and-alps', name='Oars & Alps', type="creative", label='Brand · Ecommerce', basis="Bespoke engagement", old='oarsandalps', upl='2021/06',
         deliverables='Brand, ecommerce site', color="#D6D3CC", summary='A relaunched online presence for a premium natural skincare brand for men, built to lift conversions.', images=['OA_Mock-5.jpg', 'OA_Mock-2.jpg', 'OA_Mock-1.jpg', 'OA_Mock-4.jpg', 'OA_Mock-3.jpg', 'unnamed-file.jpg']),
    dict(slug='overseas-strategies', name='Overseas Strategies', type="creative", label='Identity · Print · Website', basis="Bespoke engagement", old='overseas', upl='2021/06',
         deliverables='Rebrand, print, website', color="#D6D3CC", summary='A rebrand and aesthetic overhaul for an international business development and training consultancy.', images=['OS_Bizcard_Mock.jpg', 'OS_Identity.png', 'OS_Homepage-u.jpg', 'OS_AboutPage-u.jpg']),
    dict(slug='tg-aware', name='TG Aware', type="creative", label='Campaign · Website', basis="Bespoke engagement", old='tg-aware', upl='2023/02',
         deliverables='Awareness campaign, website', color="#D6D3CC", summary='An awareness initiative for hypertriglyceridemia, a condition linked to pancreatitis, stroke and heart disease.', images=['TGAware_MOCK-1.jpg', 'TG_Desktop-HOMEPAGE-u.jpg', 'TGAware_MOCK-3.jpg', 'TGAware_MOCK-2.jpg']),
    dict(slug='oneness', name='Oneness', type="creative", label='Identity · Website', basis="Bespoke engagement", old='oneness', upl='2021/06',
         deliverables='Visual identity, website', color="#D6D3CC", summary='A visual identity for a whole-plant hemp water, with a mark that brings together yoga and technology.', images=['Oneness_Mock-4.jpg', 'Oneness_Mock-2.jpg', 'Oneness_Mock-3.jpg', 'Oneness_Mock-1-u.jpg']),
    dict(slug='american-hockey-puck-co', name='American Hockey Puck Co.', type="creative", label='Identity · Apparel · Ecommerce', basis="Bespoke engagement", old='ahpc', upl='2021/06',
         deliverables='Logo, visual language, Shopify website', color="#D6D3CC", summary='A lifestyle brand mixing hockey with Americana athletics: an apparel-ready logo and a Shopify store.', images=['AHPC_Mockups.jpg', 'AHPC_Home_New_D-u.jpg', 'AHPC_PDP_UPDATE_D-u.jpg', 'AHPC_Tees.jpg']),
    dict(slug='plus-red-elixir', name='+RED Elixir', type="creative", label='Website', basis="Bespoke engagement", old='plus-red-elixir', upl='2023/02',
         deliverables='Website', color="#D6D3CC", summary='An energetic online presence for a premium energy drink brand five years in development.', images=['iMac-01-Standard-Mockup.jpg', 'iPhone-12-01-Standard-Mockup-1.jpg', 'iPhone-13-scenes-2-1.jpg', 'Red_Homepage-Desktop-u.jpg', 'PRE_Blog-u.jpg']),
    dict(slug='skylight-coffee', name='Skylight Coffee', type="creative", label='Identity', basis="Bespoke engagement", old='skylight-coffee', upl='2023/02',
         deliverables='Brand identity', color="#D6D3CC", summary='A clean, contemporary brand identity for a coffee company.', images=['Skylight_Mock-1.jpg']),
    dict(slug='sturgeons-tree-surgeons', name='Sturgeons Tree Surgeons', type="creative", label='Illustration · Identity · Merch', basis="Bespoke engagement", old='sturgeons-tree-surgeons', upl='2023/02',
         deliverables='Illustrated logo, merchandise, website', color="#D6D3CC", summary='A custom illustrated logo and merchandise for a tree surgery company.', images=['STS_Merch-2.jpg', 'STS_Merch-1.jpg', 'STS_Website_Home_u.jpg']),
    dict(slug='logi-analytics', name='Logi Analytics', type="creative", label='Advertising · Landing pages', basis="Bespoke engagement", old='logi', upl='2021/06',
         deliverables='Brand advertising, landing page', color="#D6D3CC", summary='Brand advertising and landing pages to set a developer-grade analytics company apart from its competitors.', images=['Logi_Ads.jpg', 'LA_BrandAd_4.jpg', 'LA_BrandAd_2.jpg', 'LA_BrandAd_1.jpg', 'LA_BrandAd_3.jpg', 'Logi_LandingPage_u.jpg']),
    dict(slug='christian-banach', name='Christian Banach', type="creative", label='Website', basis="Bespoke engagement", old='christian-banach', upl='2023/02',
         deliverables='Website', color="#D6D3CC", summary='A contemporary website for a business development consultancy that wins 6- and 7-figure deals for agencies.', images=['Pro-Display-XDR-01-Standard-Mockup-1.jpg', 'CB_Homepage-Desktop-u2.jpg', 'Pro-Display-XDR-02-Standard-Mockup.jpg', 'iPhone-13-scenes-1-3-1.jpg']),
    dict(slug='my-nu-leng', name='My Nu Leng', type="creative", label='Website', basis="Bespoke engagement", old='mynuleng', upl='2021/06',
         deliverables='Website', color="#D6D3CC", summary='A new online presence for an electronic dance duo rooted in rave culture.', images=['MYL_Mockup.jpg', 'MYL_Homepage_040320-u.jpg']),
    dict(slug='exwrks', name='ExWrks', type="creative", label='Identity', basis="Bespoke engagement", old='exwrks', upl='2021/06',
         deliverables='Logo identity', color="#D6D3CC", summary='A logo that balances soft luxury with technical precision for a furniture and home decor brand.', images=['ExWrks_IDmockup01.jpg', 'ExWrks_IDmockup.jpg']),
    dict(slug='art-of-property', name='Art of Property', type="creative", label='Product UI', basis="Bespoke engagement", old='aop', upl='2021/06',
         deliverables='Product UI design', color="#D6D3CC", summary='A modern interface for a real estate platform that connects people with expert advice on demand.', images=['AOP-Mockupe.jpg', 'AOP-Home-u.jpg', 'AOP-Browse-u.jpg']),
]

# Images for the homepage Services accordion: put files in images/services/ with these names.
SERVICE_IMAGES = {"websites": "websites.jpg", "design": "design-support.jpg", "visibility": "visibility.jpg"}

PACKAGES = [
    dict(name="Refresh", price="$3,500", pages="Up to 5 pages", cta="Choose Refresh",
         summary="A sharp, professional site for businesses with straightforward content.",
         short=["One established design direction", "Responsive build + contact form", "Basic technical setup", "One revision round"],
         full=["Up to 5 standard pages", "Client-approved copy", "One established design direction", "Responsive implementation",
               "Standard contact form", "Basic technical setup", "One consolidated revision round"]),
    dict(name="Elevate", price="$5,500", pages="Up to 10 pages", cta="Choose Elevate",
         summary="More pages and a more refined design treatment.",
         short=["More refined design treatment", "Light copy editing", "Core technical SEO setup", "Two revision rounds"],
         full=["Up to 10 standard pages", "More refined design treatment", "Light copy editing", "Responsive implementation",
               "Core technical SEO setup", "Two consolidated revision rounds"]),
    dict(name="Accelerate", price="$9,500", pages="Up to 15 pages", cta="Discuss Accelerate",
         summary="Messaging, copy and customization for a bigger step forward.",
         short=["Focused messaging workshop", "Selected copywriting", "Additional layout customization", "Analytics + search-readiness review"],
         full=["Up to 15 standard pages", "Focused messaging workshop", "Selected copywriting", "Additional layout customization",
               "Analytics setup", "Initial search-readiness review"]),
]

PLANS = [
    dict(name="Starter", price="$5,000", hours="50 hours / month", cta="Discuss Starter",
         summary="Steady support for everyday brand and marketing needs."),
    dict(name="Growth", price="$8,000", hours="80 hours / month", cta="Discuss Growth",
         summary="More capacity for active campaigns and content calendars."),
    dict(name="Pro", price="$12,000", hours="120 hours / month", cta="Discuss Pro",
         summary="A dedicated level of output for high-volume teams."),
]

NAV = [("websites.html", "Websites"), ("design-support.html", "Design Support"), ("work.html", "Work"), ("about.html", "About")]

LOGO_PATH = (HERE / "logo-path.txt").read_text().strip()

e = html.escape


# ---------------------------------------------------------------- partials
def head(title, desc, full=True):
    meta = f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300..700&display=swap">
<link rel="stylesheet" href="styles.css">"""
    if not full:
        return meta + "\n"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{meta}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
</head>
<body>
"""


SPRITE = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="logo" viewBox="0 0 742.27 131.612"><path fill="currentColor" d="{LOGO_PATH}"/></symbol></svg>\n'


def nav(active="", minimal=False):
    if minimal:
        return f"""<nav class="nav" aria-label="Main">
      <a href="index.html" aria-label="DSPTCH Design home"><svg class="logo"><use href="#logo"/></svg></a>
      <a class="btn or" href="#offer-form">Tell Us About Your Website</a>
    </nav>"""
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    links += '<a class="m" href="start.html">Start a Project</a>'
    return f"""<nav class="nav" aria-label="Main">
      <a href="index.html" aria-label="DSPTCH Design home"><svg class="logo"><use href="#logo"/></svg></a>
      <div class="links" id="site-links">{links}</div>
      <div class="navr"><a class="btn or" href="start.html">Start a Project</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-links">Menu</button></div>
    </nav>"""


def page_hero(active, eyebrow, h1, sub=None, ctas="", extra=""):
    bot = ""
    if sub or ctas:
        bot = f'<div class="hero-bot">{f"<p>{sub}</p>" if sub else ""}{f"<div class=ctas>{ctas}</div>" if ctas else ""}</div>'
    return f"""<div class="top">
  <div class="wrap">
    {nav(active)}
    <header class="phero">
      <span class="dot">{eyebrow}</span>
      <h1>{h1}</h1>
      {bot}
    </header>
    {extra}
  </div>
</div>
"""


def footer(close_h="It's time for an upgrade.", close_cta=("start.html", "Start Your Website"), show_close=True):
    close = ""
    if show_close:
        close = f"""<div class="close">
    <h2>{close_h}</h2>
    <a class="btn or" href="{close_cta[0]}">{close_cta[1]}</a>
  </div>"""
    return f"""<section class="wrap">
  {close}
  <footer class="foot">
    <span class="mail">{EMAIL}</span>
    <ul><li><a href="websites.html">Websites</a></li><li><a href="packages.html">Packages</a></li><li><a href="design-support.html">Design Support</a></li><li><a href="work.html">Work</a></li><li><a href="about.html">About</a></li><li><a href="blog.html">Blog</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li></ul>
  </footer>
  <svg class="logo giant" aria-hidden="true"><use href="#logo"/></svg>
  <div class="end"></div>
</section>
"""


def tail(full=True):
    s = '<script src="site.js"></script>\n'
    return s + ("</body>\n</html>\n" if full else "")


def have(path):
    return (HERE / "images" / path).exists()


def img_block(p, i=0, ph="Project image"):
    imgs = [x for x in (p.get("images") or []) if have(f"work/{p['slug']}/{x}")]
    if i < len(imgs):
        return f'<img src="images/work/{p["slug"]}/{imgs[i]}" alt="{e(p["name"])}" loading="lazy">'
    return f'<i style="background:{p["color"]}"></i><span class="ph">{ph}</span>'


def svc_img(key, fallback):
    f = SERVICE_IMAGES[key]
    if have(f"services/{f}"):
        return f'<div class="img"><img src="images/services/{f}" alt="" loading="lazy"></div>'
    return f'<div class="img"><i style="background:{fallback}"></i></div>'


def card(p):
    tag = '<span class="tag">Website</span>' if p["type"] == "website" else ""
    if p.get("placeholder"):
        return (f'<div class="card" data-type="{p["type"]}"><div class="img">{img_block(p, 0, "New website example")}{tag}</div>'
                f'<div class="cap"><b>{e(p["name"])}</b><span>{e(p["label"])}</span></div></div>')
    return (f'<a class="card" href="project-{p["slug"]}.html" data-type="{p["type"]}"><div class="img">{img_block(p)}{tag}</div>'
            f'<div class="cap"><b>{e(p["name"])}</b><span>{e(p["label"])}</span></div></a>')


def pk_cards(full=False, link_all=True):
    out = []
    for i, p in enumerate(PACKAGES):
        items = p["full"] if full else p["short"]
        sum_ = f'<p class="sum">{p["summary"]}</p>' if full else ""
        cls = "btn or" if i == 1 else "btn ghost"
        out.append(f'<article class="pkc{" hl" if i == 1 else ""}"><div class="t"><h3>{p["name"]}</h3><span>{p["pages"]}</span></div>'
                   f'<div class="price">{p["price"]}</div>{sum_}<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>'
                   f'<a class="{cls}" href="start.html?package={p["name"].lower()}">{p["cta"]}</a></article>')
    return '<div class="pk">' + "".join(out) + "</div>"


def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


FAQ = {
    "own": ("Who owns the finished site?", "You own the agreed website assets and your domain. Hosting, third-party licenses and code handoff terms are defined in your agreement."),
    "edit": ("Can we update the website ourselves?", "Editing options depend on the build and content setup. We explain the handoff before development starts, so you know exactly how updates will work."),
    "content": ("What happens to our current content?", "We review it with you during scoping. Packages assume client-approved copy; extensive content migration is scoped separately."),
    "pages": ("What if we need additional pages?", "Additional pages and functionality are scoped and priced separately, before any work on them begins."),
    "rank": ("Will my site rank in Google or AI search?", "We build on sound technical foundations, but no provider can guarantee rankings or AI recommendations."),
    "rev": ("How do revisions work?", "Each package includes a defined number of consolidated feedback rounds. Additional changes are quoted separately."),
    "custom": ("What if I need custom strategy?", "We'll recommend a custom engagement when your needs go beyond a fixed package."),
    "time": ("How long will it take?", "We confirm a timeline with your scope. The schedule starts once content, access and approvals are in."),
    "need": ("What will you need from me?", "Accurate content, brand assets, domain access, timely approvals and one decision-maker for feedback."),
    "incl": ("What is included?", "Design direction, responsive layouts, an agreed page count, standard forms, basic technical SEO setup, QA and handoff. Final inclusions vary by package."),
}

pages = {}


# ---------------------------------------------------------------- home
def home(full=True):
    feat = [p for p in PROJECTS if p.get("featured")][:6]
    return head("DSPTCH Design — Exceptional websites", "Premium, fixed-scope websites and on-demand creative support from DSPTCH Design.", full) + SPRITE + f"""<div class="top">
  <div class="wrap">
    {nav()}
    <header class="hero">
      <span class="dot">Websites + Creative Support</span>
      <h1>Exceptional websites. <span>Without the agency complexity.</span></h1>
      <div class="hero-bot">
        <p>Polished, professional websites with thoughtful design, straightforward pricing, and a streamlined process.</p>
        <div class="ctas"><a class="btn or" href="websites.html">Explore Websites</a><a class="btn ghost" href="work.html">See Our Work</a></div>
      </div>
    </header>
    <section class="about">
      <span class="dot">About DSPTCH</span>
      <h2>A better website changes how people see your business. <span>Experienced creative direction, clear deliverables, and a process designed to reduce friction.</span></h2>
    </section>
  </div>
</div>

<section class="wrap sec" id="work">
  <div class="head"><h2>Selected work</h2><a class="btn ghost" href="work.html">View all work</a></div>
  <div class="grid">{"".join(card(p) for p in feat)}</div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="head"><h2>Services</h2><span class="dot">Two ways to work with us</span></div>
    <div class="rows">
      <details class="row" open>
        <summary><h3>Websites</h3><span class="plus" aria-hidden="true">+</span></summary>
        <div class="body">
          <div><p>Premium websites, built a smarter way. Experienced design judgment and efficient production, without a traditional agency engagement.</p><a class="btn or" href="packages.html">View Packages</a></div>
          {svc_img("websites", "radial-gradient(60% 70% at 70% 30%,rgba(232,0,90,.55),transparent 70%),#1A1A1A")}
          <ul class="checks"><li>Design direction</li><li>Responsive layouts</li><li>Forms and lead capture</li><li>Technical SEO setup</li><li>QA and handoff</li></ul>
        </div>
      </details>
      <details class="row">
        <summary><h3>Design Support</h3><span class="plus" aria-hidden="true">+</span></summary>
        <div class="body">
          <div><p>Your design team, on demand. Flexible creative support for campaigns, presentations, social content and everyday brand needs.</p><a class="btn or" href="design-support.html">Explore Plans</a></div>
          {svc_img("design", "radial-gradient(60% 70% at 30% 40%,rgba(110,60,200,.5),transparent 70%),#1A1A1A")}
          <ul class="checks"><li>Marketing materials</li><li>Presentations</li><li>Social creative</li><li>Campaign assets</li><li>Packaging</li></ul>
        </div>
      </details>
      <details class="row">
        <summary><h3>Search &amp; Visibility</h3><span class="plus" aria-hidden="true">+</span></summary>
        <div class="body">
          <div><p>A beautiful website is the starting point. Ask about search-ready foundations and ongoing content and visibility support.</p><a class="btn or" href="start.html">Ask About It</a></div>
          {svc_img("visibility", "radial-gradient(50% 60% at 60% 60%,rgba(255,60,60,.4),transparent 70%),#1A1A1A")}
          <ul class="checks"><li>Visibility audit</li><li>Content opportunities</li><li>Technical recommendations</li><li>Optional reporting</li></ul>
        </div>
      </details>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="head"><h2>Website packages</h2><span class="dot">Clear scope, clear price</span></div>
  {pk_cards()}
  <p class="fine">Final scope is confirmed before work begins. E-commerce, complex integrations, photography, video and extensive content migration are scoped separately. <a class="tl" href="packages.html">Compare packages</a></p>
</section>

{footer()}""" + tail(full)


# ---------------------------------------------------------------- websites
def websites():
    web = [p for p in PROJECTS if p["type"] == "website"][:3]
    return head("Websites — DSPTCH Design", "Premium websites, built a smarter way. Fixed-scope packages from $3,500.") + SPRITE + page_hero(
        "websites.html", "Websites", "Premium websites. <span>A smarter way to build.</span>",
        "We combine experienced design judgment with efficient production to create modern websites without a traditional agency engagement.",
        '<a class="btn or" href="packages.html">View Packages</a><a class="btn ghost" href="website-work.html">See Website Work</a>',
        extra="""<section class="about">
      <span class="dot">The problem</span>
      <h2>Your business has evolved. Your website hasn't. <span>We help you build a digital presence that reflects the quality of what you do.</span></h2>
    </section>""") + f"""
<section class="wrap sec">
  <div class="cols3">
    <div><span class="dot">Designed to impress</span><h3>Refined typography, composition and hierarchy.</h3><p>Every page is art directed, so your site looks considered rather than assembled.</p></div>
    <div><span class="dot">Simple to navigate</span><h3>A clearly defined process and scope.</h3><p>You know what you're getting, what it costs and what we need from you before work starts.</p></div>
    <div><span class="dot">Ready to work</span><h3>Responsive pages, lead capture and technical foundations.</h3><p>Built to look right on every screen and to turn visits into inquiries.</p></div>
  </div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="split">
      <span class="dot">What's included</span>
      <div class="body">
        <h2 class="h2s">Everything a professional website needs.</h2>
        <ul class="tags"><li>Design direction</li><li>Responsive layouts</li><li>Agreed page count</li><li>Standard forms</li><li>Basic technical SEO setup</li><li>QA and handoff</li></ul>
        <p class="mute">Final inclusions vary by package.</p>
      </div>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="head"><h2>See what better<br>can look like</h2><a class="btn ghost" href="website-work.html">See Website Work</a></div>
  <div class="grid">{"".join(card(p) for p in web)}</div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="head"><h2>How it works</h2><span class="dot">Four steps to launch</span></div>
    <ol class="steps">
      <li><h3>Align on scope and assets</h3><p>We confirm the package, page list and everything we need from you.</p></li>
      <li><h3>Build the agreed pages</h3><p>Design direction first, then responsive pages built to that direction.</p></li>
      <li><h3>Review through consolidated feedback</h3><p>One clear round of notes at a time, from one decision-maker.</p></li>
      <li><h3>Test and launch</h3><p>Checked on every screen size, then launched and handed off.</p></li>
    </ol>
  </div>
</section>

<section class="wrap sec">
  <div class="head"><h2>Three ways<br>to get started</h2><span class="dot">Transparent deliverables, clear boundaries</span></div>
  {pk_cards()}
  <p class="fine"><a class="tl" href="packages.html">Compare packages in detail</a></p>
</section>

<section class="wrap sec tight">
  <div class="split">
    <span class="dot">Questions</span>
    {faq([FAQ["edit"], FAQ["content"], FAQ["own"], FAQ["pages"]])}
  </div>
</section>

{footer("Let's build something your business can be proud of.")}""" + tail()


# ---------------------------------------------------------------- packages
def packages():
    return head("Website Packages — DSPTCH Design", "Refresh, Elevate and Accelerate: fixed-scope website packages from $3,500.") + SPRITE + page_hero(
        "websites.html", "Website Packages", "A better website. <span>A clear starting point.</span>",
        "Choose the level of support that fits your business. We confirm the final scope before work begins.") + f"""
<section class="wrap sec">
  {pk_cards(full=True)}
</section>

<section class="wrap">
  <div class="split">
    <span class="dot">Scope transparency</span>
    <div class="body">
      <h2 class="h2s">Not included unless separately scoped.</h2>
      <ul class="tags"><li>E-commerce</li><li>Complex integrations</li><li>Custom applications</li><li>Extensive content migration</li><li>Major copywriting</li><li>Photography</li><li>Video</li><li>Legal compliance audits</li><li>Maintenance</li><li>Additional revisions</li></ul>
    </div>
  </div>
  <div class="split">
    <span class="dot">Timing</span>
    <div class="body">
      <h2 class="h2s">Your schedule starts when your content does.</h2>
      <p class="lede mute">Delivery windows begin once content, access and approvals are received. We confirm your timeline as part of scoping.</p>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="split">
    <span class="dot">Questions</span>
    {faq([FAQ["rev"], FAQ["pages"], FAQ["own"], FAQ["rank"], FAQ["custom"]])}
  </div>
</section>

{footer("Not sure where you fit?", ("start.html", "Get a Recommendation"))}""" + tail()


# ---------------------------------------------------------------- work pages
def work():
    return head("Work — DSPTCH Design", "Selected websites, identities, campaigns and creative systems.") + SPRITE + page_hero(
        "work.html", "Our Work", "Work that makes <span>an impression.</span>",
        "Selected projects across websites, identities, campaigns and creative systems.") + f"""
<section class="wrap sec">
  <div class="head">
    <div class="filters" role="group" aria-label="Filter work">
      <button type="button" data-filter="website" aria-pressed="true">Websites</button>
      <button type="button" data-filter="creative" aria-pressed="false">Creative</button>
      <button type="button" data-filter="all" aria-pressed="false">All</button>
    </div>
    <span class="dot" data-count>{len(real())} projects</span>
  </div>
  <div class="grid" data-grid>{"".join(card(p).replace('class="card"', 'class="card" hidden', 1) if p["type"] != "website" else card(p) for p in PROJECTS)}</div>
</section>

{footer("Have something in mind?", ("start.html", "Start a Project"))}""" + tail()


def website_work():
    web = [p for p in PROJECTS if p["type"] == "website"]
    return head("Website Work — DSPTCH Design", "Websites shaped by thoughtful design and a clear purpose.") + SPRITE + page_hero(
        "work.html", "Website Work", "Websites worth <span>a closer look.</span>",
        "A selection of digital experiences shaped by thoughtful design and a clear purpose.",
        '<a class="btn or" href="packages.html">Explore Packages</a>') + f"""
<section class="wrap sec">
  <div class="grid">{"".join(card(p) for p in web)}</div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="head"><h2>A stronger<br>first impression</h2><span class="dot">Before and after</span></div>
    <div class="ba">
      <div class="img" style="background:#1A1A1A"><span class="lbl">Before</span></div>
      <div class="img" style="background:#2A1420"><span class="lbl">After</span></div>
    </div>
    <p class="fine" style="color:var(--dark-mute)">Real before-and-after redesigns, shown with permission. Speculative redesigns are labeled as concepts.</p>
  </div>
</section>

{footer("See what your website could become.", ("packages.html", "Explore Packages"))}""" + tail()


def gallery(p):
    """Every image after the cover, at its natural shape. Landscape images run full width; tall ones sit in pairs."""
    from PIL import Image
    imgs = [x for x in (p.get("images") or []) if have(f"work/{p['slug']}/{x}")][1:]
    if not imgs:
        return ('<div class="gallery"><div class="wide"><div class="img">' + img_block(p, 9, "Project image") +
                '</div></div><div><div class="img">' + img_block(p, 9, "Project image") + '</div></div><div><div class="img">' +
                img_block(p, 9, "Project image") + '</div></div></div>')
    info = []
    for x in imgs:
        w, h = Image.open(HERE / "images" / "work" / p["slug"] / x).size
        info.append((x, w, h, h > w * 1.05))
    # keep tall images side by side: pair each tall image with the next tall one
    talls = [i for i in info if i[3]]
    order, used = [], set()
    for it in info:
        if it[0] in used: continue
        if it[3]:
            mate = next((t for t in talls if t[0] not in used and t[0] != it[0]), None)
            order.append((it, "g-tall" if mate else "g-solo")); used.add(it[0])
            if mate: order.append((mate, "g-tall")); used.add(mate[0])
        else:
            order.append((it, "g-wide")); used.add(it[0])
    out = [f'<figure class="{c}"><img src="images/work/{p["slug"]}/{x}" alt="{e(p["name"])}" width="{w}" height="{h}" loading="lazy"></figure>'
           for (x, w, h, _), c in order]
    return '<div class="gal">' + "".join(out) + "</div>"


def real():
    return [p for p in PROJECTS if not p.get("placeholder")]


def project(p, i):
    R = real(); n = len(R)
    prev, nxt = R[(i - 1) % n], R[(i + 1) % n]
    cta = ("packages.html", "Explore Website Packages") if p["type"] == "website" else ("design-support.html", "Explore Design Support")
    summary = p.get("summary") or "One concise sentence about the challenge and approach."
    story = p.get("story") or {}
    def sec(key, title, default):
        txt = story.get(key)
        body = f"<p class='lede'>{txt}</p>" if txt else f"<p class='lede mute'>{default}</p>"
        return f'<div class="split"><span class="dot">{title}</span><div class="body">{body}</div></div>'
    return head(f"{p['name']} — DSPTCH Design", summary) + SPRITE + page_hero(
        "work.html", e(p["label"]), e(p["name"]), e(summary),
        f'<a class="btn or" href="{p["url"]}" target="_blank" rel="noopener">Visit the live site</a>' if p.get("url") else "") + f"""
<section class="wrap sec tight cs-hero">
  <div class="img">{img_block(p, 0, "Cover image")}</div>
  <dl class="facts">
    <div><dt>Client</dt><dd>{e(p["name"])}</dd></div>
    <div><dt>Deliverables</dt><dd>{e(p["deliverables"])}</dd></div>
    <div><dt>Type</dt><dd>{"Website" if p["type"] == "website" else "Creative"}</dd></div>
    <div><dt>Engagement</dt><dd>{e(p["basis"])}</dd></div>
  </dl>
</section>

<section class="wrap sec tight">
  {sec("challenge", "The challenge", "Case study copy to come: what the client needed and why.")}
  {sec("approach", "Our approach", "Case study copy to come: how we approached the work.")}
  {sec("created", "What we created", "Case study copy to come: the deliverables, in plain terms.")}
</section>

<section class="wrap sec tight">
  {gallery(p)}
</section>

<section class="wrap sec tight">
  <nav class="pager" aria-label="More projects">
    <a href="project-{prev['slug']}.html"><span>Previous</span><b>{e(prev['name'])}</b></a>
    <a href="project-{nxt['slug']}.html"><span>Next</span><b>{e(nxt['name'])}</b></a>
  </nav>
</section>

{footer("Want results like this?", cta)}""" + tail()


# ---------------------------------------------------------------- design support
def creative_examples():
    picks = [p for p in PROJECTS if p["slug"] in ("stussy", "bloved", "vitalitea")]
    return f"""<section class="wrap sec" style="padding-top:0">
  <div class="head"><h2>Creative work</h2><a class="btn ghost" href="work.html#creative">See all creative</a></div>
  <div class="grid">{"".join(card(p) for p in picks)}</div>
</section>
"""


def design_support():
    return head("Design Support — DSPTCH Design", "Your design team, on demand. Monthly creative support plans.") + SPRITE + page_hero(
        "design-support.html", "Design on Demand", "Your design team, <span>on demand.</span>",
        "Reliable creative support for the work that keeps your business moving, without growing your in-house team.",
        '<a class="btn or" href="design-plans.html">Explore Plans</a><a class="btn ghost" href="work.html">See Our Work</a>') + """
<section class="wrap sec">
  <div class="split">
    <span class="dot">Capabilities</span>
    <div class="body">
      <h2 class="h2s">The everyday design work your business runs on.</h2>
      <ul class="tags"><li>Marketing materials</li><li>Presentations</li><li>Social creative</li><li>Campaign assets</li><li>Packaging</li><li>Digital design</li></ul>
      <p class="mute">Final inclusions depend on your plan.</p>
    </div>
  </div>
</section>

""" + creative_examples() + """
<section class="dark">
  <div class="wrap sec">
    <div class="cols3">
      <div><span class="dot">A consistent team</span><h3>The same designers who know your brand.</h3><p class="mute">No re-briefing a new freelancer every time.</p></div>
      <div><span class="dot">A simpler request process</span><h3>Submit prioritized requests in one place.</h3><p class="mute">Clear queues, clear turnaround, fewer emails.</p></div>
      <div><span class="dot">Flexible capacity</span><h3>Design hours scaled to your needs.</h3><p class="mute">Choose the plan that matches your workload.</p></div>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="head"><h2>How it works</h2><span class="dot">From request to final files</span></div>
  <ol class="steps">
    <li><h3>Choose your plan</h3><p>Pick the monthly capacity that fits your workload.</p></li>
    <li><h3>Submit prioritized requests</h3><p>Tell us what matters most this week.</p></li>
    <li><h3>Collaborate through clear feedback</h3><p>Consolidated notes keep work moving.</p></li>
    <li><h3>Receive production-ready files</h3><p>Final files, ready for print, web or social.</p></li>
  </ol>
</section>

<section class="wrap">
  <div class="note">
    <span class="dot">Already launched with DSPTCH?</span>
    <h3>Keep the momentum going with ongoing creative support.</h3>
    <p>Website clients can add a design plan for campaigns, social and everything that comes after launch.</p>
  </div>
</section>
<div class="sec tight"></div>

""" + footer("Less juggling. Better design.", ("design-plans.html", "Find Your Plan")) + tail()


def design_plans():
    cards = []
    for i, p in enumerate(PLANS):
        cls = "btn or" if i == 1 else "btn ghost"
        cards.append(f'<article class="pkc{" hl" if i == 1 else ""}"><div class="t"><h3>{p["name"]}</h3><span>{p["hours"]}</span></div>'
                     f'<div class="price">{p["price"]}<small>/ month</small></div><p class="sum">{p["summary"]}</p>'
                     f'<ul><li>{p["hours"].replace(" / month", "")} of design capacity</li><li>Prioritized request queue</li><li>Production-ready files</li></ul>'
                     f'<a class="{cls}" href="start.html?intent=design&plan={p["name"].lower()}">{p["cta"]}</a></article>')
    return head("Design Plans — DSPTCH Design", "Monthly design support plans: Starter, Growth and Pro.") + SPRITE + page_hero(
        "design-support.html", "Design Plans", "Creative support that fits <span>your workload.</span>",
        "Choose the amount of ongoing design capacity your business needs.") + f"""
<section class="wrap sec">
  <div class="pk">{"".join(cards)}</div>
  <p class="fine">Plan details are confirmed during your consultation, including monthly hours, request queue, simultaneous tasks, turnaround targets, unused hours, revisions, cancellation, file ownership and exclusions.</p>
</section>

{footer("Less juggling. Better design.", ("start.html?intent=design", "Discuss a Plan"))}""" + tail()


# ---------------------------------------------------------------- about
def about():
    return head("About — DSPTCH Design", "A sharper way to work: experienced creative thinking, modern tools and a simpler process.") + SPRITE + page_hero(
        "about.html", "About", "A sharper way <span>to work.</span>",
        "DSPTCH combines experienced creative thinking, modern tools and a simpler way to get excellent work made.") + """
<section class="wrap sec">
  <div class="split">
    <span class="dot">Philosophy</span>
    <div class="body">
      <h2 class="h2s">Good design should be intentional. Getting it made should be straightforward.</h2>
      <p class="lede mute">We focus on clarity, quality and a process that respects your time.</p>
    </div>
  </div>
  <div class="split">
    <span class="dot">How we're different</span>
    <div class="cols3" style="grid-column:auto">
      <div><h3>Experienced creative direction</h3><p>Every project is art directed by designers with years of brand and web work behind them.</p></div>
      <div><h3>Clear deliverables</h3><p>Fixed scopes and plain-language packages, so nothing is a surprise.</p></div>
      <div><h3>Fewer meetings</h3><p>A process built to reduce friction and keep the work moving.</p></div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="head"><h2>Team</h2><span class="dot">The people behind the work</span></div>
    <div class="grid">
      <div class="card"><div class="img" style="background:var(--dark-tile)"><span class="ph" style="color:rgba(255,255,255,.4)">Portrait</span></div><div class="cap"><b>Name</b><span class="mute">Role</span></div></div>
      <div class="card"><div class="img" style="background:var(--dark-tile)"><span class="ph" style="color:rgba(255,255,255,.4)">Portrait</span></div><div class="cap"><b>Name</b><span class="mute">Role</span></div></div>
      <div class="card"><div class="img" style="background:var(--dark-tile)"><span class="ph" style="color:rgba(255,255,255,.4)">Portrait</span></div><div class="cap"><b>Name</b><span class="mute">Role</span></div></div>
    </div>
    <p class="fine" style="color:var(--dark-mute)">Team bios and verified roles to come.</p>
  </div>
</section>
<div class="sec tight"></div>

""" + footer("Great work starts with a clear conversation.", ("start.html", "Start a Project")) + tail()


# ---------------------------------------------------------------- start / thanks / offer
BUDGET_WEB = ["Under $3,500", "$3,500 – $5,500", "$5,500 – $9,500", "$9,500+", "Not sure yet"]
BUDGET_DES = ["Under $5,000 / month", "$5,000 – $8,000 / month", "$8,000 – $12,000 / month", "$12,000+ / month", "Not sure yet"]


def opts(xs):
    return '<option value="">Select…</option>' + "".join(f"<option>{x}</option>" for x in xs)


def field(id_, label, kind="input", type_="text", req=False, full=False, options=None, ph=""):
    r = " required" if req else ""
    if kind == "select":
        ctl = f'<select id="{id_}" name="{id_}"{r}>{opts(options)}</select>'
    elif kind == "textarea":
        ctl = f'<textarea id="{id_}" name="{id_}" placeholder="{ph}"{r}></textarea>'
    else:
        ctl = f'<input id="{id_}" name="{id_}" type="{type_}" placeholder="{ph}"{r}>'
    return f'<div class="field{" full" if full else ""}"><label for="{id_}">{label}{" *" if req else ""}</label>{ctl}</div>'


def start():
    return head("Start a Project — DSPTCH Design", "Tell us what you're building and we'll recommend the right next step.") + SPRITE + page_hero(
        "", "Start a Project", "Tell us what <span>you're building.</span>",
        "A few details will help us recommend the right next step.") + f"""
<section class="wrap sec">
  <form class="form" name="start" method="POST" action="thanks.html" data-netlify="true" netlify-honeypot="company-website" data-intent-form>
    <input type="hidden" name="form-name" value="start">
    <input type="hidden" name="package" id="package">
    <input type="hidden" name="source" id="source">
    <p class="hp"><label>Leave this empty <input name="company-website"></label></p>

    <fieldset class="fs">
      <legend>What do you need?</legend>
      <div class="choice">
        <label><input type="radio" name="intent" value="website" required checked><b>A website</b><span>New site or redesign</span></label>
        <label><input type="radio" name="intent" value="design"><b>Ongoing design support</b><span>Monthly creative capacity</span></label>
        <label><input type="radio" name="intent" value="unsure"><b>I'm not sure</b><span>We'll help you decide</span></label>
      </div>
    </fieldset>

    <fieldset class="fs" data-for="website unsure">
      <legend>About your website<small>Approximate answers are fine.</small></legend>
      <div class="fgrid">
        {field("current-url", "Current website", type_="url", ph="https://")}
        {field("business-type", "Type of business")}
        {field("project-type", "New site or redesign", "select", options=["New website", "Redesign", "Not sure"])}
        {field("page-count", "Approximate page count", "select", options=["1–5", "6–10", "11–15", "More than 15", "Not sure"])}
        {field("content-ready", "Is your content ready?", "select", options=["Yes, copy and images are ready", "Partly", "Not yet"])}
        {field("launch-window", "Preferred launch window", "select", options=["Within 1 month", "1–3 months", "3+ months", "Flexible"])}
        {field("functionality", "Anything it needs to do?", "textarea", full=True, ph="Forms, booking, integrations, online store…")}
        {field("budget-website", "Budget", "select", options=BUDGET_WEB)}
      </div>
    </fieldset>

    <fieldset class="fs" data-for="design" hidden>
      <legend>About your design needs</legend>
      <div class="fgrid">
        {field("design-type", "Type of design work", full=True, ph="Social, presentations, campaigns, packaging…")}
        {field("monthly-volume", "Estimated monthly volume", "select", options=["A few requests", "Steady weekly requests", "High volume", "Not sure"])}
        {field("start-date", "Desired start date", "select", options=["As soon as possible", "Next month", "Later this year", "Flexible"])}
        {field("budget-design", "Budget", "select", options=BUDGET_DES)}
      </div>
    </fieldset>

    <fieldset class="fs">
      <legend>How can we reach you?</legend>
      <div class="fgrid">
        {field("name", "Name", req=True)}
        {field("email", "Work email", type_="email", req=True)}
        {field("notes", "Anything else?", "textarea", full=True)}
      </div>
    </fieldset>

    <div class="submit">
      <button class="btn or" type="submit">Get My Recommendation</button>
      <p>We'll review your details and follow up with the next step. Submitting an inquiry does not reserve a launch date.</p>
    </div>
  </form>
</section>

{footer(show_close=False)}""" + tail()


def thanks():
    return head("Thank You — DSPTCH Design", "We've received your project details.") + SPRITE + page_hero(
        "", "Thank you", "Thanks. We've received <span>your project details.</span>",
        "Our team will review your request and follow up with the most relevant next step. If we need clarification about your site or timeline, we'll reach out.",
        '<a class="btn or" href="work.html">Explore Our Work</a><a class="btn ghost" href="index.html">Back to Home</a>') + footer(show_close=False) + tail()


def offer():
    web = [p for p in PROJECTS if p["type"] == "website"][:3]
    return head("A Better Website — DSPTCH Design", "Premium design. Clear packages. A more straightforward launch.") + SPRITE + f"""<div class="top">
  <div class="wrap">
    {nav(minimal=True)}
    <header class="phero">
      <span class="dot">DSPTCH Design Websites</span>
      <h1>Your business deserves <span>a better website.</span></h1>
      <div class="hero-bot"><p>Premium design. Clear packages. A more straightforward launch.</p><div class="ctas"><a class="btn or" href="#offer-packages">See Website Packages</a></div></div>
    </header>
  </div>
</div>

<section class="wrap sec">
  <div class="grid">{"".join(card(p) for p in web)}</div>
</section>

<section class="dark">
  <div class="wrap sec">
    <div class="split">
      <span class="dot">Who this is for</span>
      <div class="body"><h2 class="h2s">Established businesses with outdated sites, straightforward content and a need for a more professional digital presence.</h2></div>
    </div>
    <div class="split">
      <span class="dot">What you get</span>
      <div class="body"><ul class="tags"><li>Refined design</li><li>Responsive build</li><li>Lead capture</li><li>Clear revision process</li><li>Launch handoff</li></ul></div>
    </div>
  </div>
</section>

<section class="wrap sec" id="offer-packages">
  <div class="head"><h2>Packages</h2><span class="dot">Clear scope, clear price</span></div>
  {pk_cards()}
</section>

<section class="wrap">
  <div class="split">
    <span class="dot">Questions</span>
    {faq([FAQ["incl"], FAQ["need"], FAQ["time"], FAQ["edit"]])}
  </div>
</section>

<section class="wrap sec" id="offer-form">
  <div class="split">
    <span class="dot">Tell us about your website</span>
    <form class="form" name="website-offer" method="POST" action="thanks.html" data-netlify="true" netlify-honeypot="company-website">
      <input type="hidden" name="form-name" value="website-offer">
      <input type="hidden" name="source" id="source">
      <p class="hp"><label>Leave this empty <input name="company-website"></label></p>
      <div class="fgrid">
        {field("o-name", "Name", req=True)}
        {field("o-email", "Work email", type_="email", req=True)}
        {field("o-url", "Current website", type_="url", full=True, ph="https://")}
        {field("o-budget", "Budget", "select", full=True, options=BUDGET_WEB)}
      </div>
      <div class="submit"><button class="btn or" type="submit">Tell Us About Your Website</button></div>
    </form>
  </div>
</section>

{footer(show_close=False)}""" + tail()


# ---------------------------------------------------------------- legal + 404
def legal(kind):
    if kind == "privacy":
        t, h1, body = "Privacy Policy", "Privacy <span>policy.</span>", """
<p><span class="ph-note">Draft — requires legal review before launch</span></p>
<p>This policy explains what information DSPTCH Design collects through this website and how it is used.</p>
<h2>Information you give us</h2>
<p>When you submit a form, we collect the details you enter, such as your name, email address, website and project information. We use it only to respond to your inquiry and provide our services.</p>
<h2>Form handling and hosting</h2>
<p>This site is hosted on Netlify, which processes form submissions on our behalf.</p>
<h2>Analytics and cookies</h2>
<p>Describe any analytics or cookies in use once they are selected.</p>
<h2>Contact</h2>
<p>Questions about this policy: <span class="mail">""" + EMAIL + "</span></p>"
    else:
        t, h1, body = "Terms of Use", "Terms <span>of use.</span>", """
<p><span class="ph-note">Draft — requires legal review before launch</span></p>
<p>These terms govern your use of this website. Project work is governed by the separate agreement signed for each engagement.</p>
<h2>Website content</h2>
<p>Content on this site, including project imagery, belongs to DSPTCH Design or its clients and is shown with permission.</p>
<h2>Pricing</h2>
<p>Prices shown are starting points. Final scope and price are confirmed in writing before work begins.</p>
<h2>Contact</h2>
<p><span class="mail">""" + EMAIL + "</span></p>"
    return head(f"{t} — DSPTCH Design", t) + SPRITE + page_hero("", "Legal", h1) + f"""
<section class="wrap sec"><div class="prose">{body}</div></section>
{footer(show_close=False)}""" + tail()


def notfound():
    return head("Page Not Found — DSPTCH Design", "Page not found.") + SPRITE + page_hero(
        "", "404", "This page <span>isn't here.</span>", "It may have moved when we rebuilt the site.",
        '<a class="btn or" href="index.html">Go to Home</a><a class="btn ghost" href="work.html">See Our Work</a>') + footer(show_close=False) + tail()



# ---------------------------------------------------------------- blog
# Articles live in posts/*.md (front matter + Markdown). Remove "status: draft" to publish.
import datetime, yaml, markdown as md_lib


def load_posts():
    out = []
    for f in sorted((HERE / "posts").glob("*.md")):
        raw = f.read_text()
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm)
        meta["html"] = md_lib.markdown(body.strip(), extensions=["extra"])
        meta["date"] = meta["date"] if isinstance(meta["date"], datetime.date) else datetime.date.fromisoformat(str(meta["date"]))
        words = len(body.split()) + len(meta.get("answer", "").split())
        meta["mins"] = max(1, round(words / 220))
        out.append(meta)
    return sorted(out, key=lambda m: m["date"], reverse=True)


POSTS = load_posts()


def fdate(d):
    return d.strftime("%B %-d, %Y")


def draft_chip(p):
    return '<span class="ph-note">Draft</span>' if p.get("status") == "draft" else ""


def blog_cover(p, big=False):
    f = p.get("image")
    if f and have(f"blog/{f}"):
        return f'<div class="img"><img src="images/blog/{f}" alt="" loading="lazy"></div>'
    return '<div class="img bcover"><i></i></div>'


def blog_index():
    lead, rest = POSTS[0], POSTS[1:]
    rows = "".join(f"""<a class="brow" href="blog-{p['slug']}.html">
      <span class="bmeta">{fdate(p['date'])}</span>
      <span class="btitle">{e(p['title'])}</span>
      <span class="bex">{e(p['excerpt'])}</span>
      <span class="bmeta">{p['category']} · {p['mins']} min {draft_chip(p)}</span>
    </a>""" for p in rest)
    return head("Blog — DSPTCH Design", "Notes on websites, design and visibility from DSPTCH Design.") + SPRITE + page_hero(
        "", "Blog", "Notes on websites, <span>design and visibility.</span>",
        "Plain answers to the questions businesses ask us most.") + f"""
<section class="wrap sec">
  <a class="blead" href="blog-{lead['slug']}.html">
    {blog_cover(lead, True)}
    <div class="blead-txt">
      <span class="bmeta">{lead['category']} · {fdate(lead['date'])} · {lead['mins']} min read {draft_chip(lead)}</span>
      <h2>{e(lead['title'])}</h2>
      <p class="lede mute">{e(lead['excerpt'])}</p>
      <span class="tl" style="align-self:flex-start">Read article</span>
    </div>
  </a>
</section>

<section class="wrap">
  <div class="split">
    <span class="dot">All articles</span>
    <div class="blist">{rows}</div>
  </div>
</section>
<div class="sec tight"></div>

{footer("Have a question we haven't answered?", ("start.html", "Ask Us"))}""" + tail()


def blog_post(p):
    i = POSTS.index(p)
    others = [x for x in POSTS if x is not p][:2]
    faq_items = p.get("faq") or []
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["excerpt"],
             "datePublished": p["date"].isoformat(), "author": {"@type": "Organization", "name": "DSPTCH Design"},
             "publisher": {"@type": "Organization", "name": "DSPTCH Design"},
             "mainEntityOfPage": f"https://dsptchdesign.com/blog-{p['slug']}"},
        ] + ([{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"],
              "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq_items]}] if faq_items else []),
    }
    related = "".join(f"""<a class="brow" href="blog-{x['slug']}.html">
      <span class="bmeta">{fdate(x['date'])}</span><span class="btitle">{e(x['title'])}</span>
      <span class="bex">{e(x['excerpt'])}</span><span class="bmeta">{x['category']} · {x['mins']} min</span></a>""" for x in others)
    return head(f"{p['title']} — DSPTCH Design", p["excerpt"]) + SPRITE + \
        f'<script type="application/ld+json">{json.dumps(ld)}</script>\n' + f"""<div class="top">
  <div class="wrap">
    {nav()}
    <header class="phero art-hero">
      <span class="dot">{p['category']} · {fdate(p['date'])} · {p['mins']} min read</span>
      <h1>{e(p['title'])}</h1>
    </header>
  </div>
</div>

<article class="wrap sec art">
  <div class="art-side">
    <a class="tl" href="blog.html">All articles</a>
    {draft_chip(p)}
  </div>
  <div class="art-body">
    <div class="answer"><span class="dot">Short answer</span><p>{e(p.get('answer', ''))}</p></div>
    <div class="prose art-prose">{p['html']}</div>
    {('<h2 class="art-faq-h">Frequently asked questions</h2>' + faq([(f['q'], f['a']) for f in faq_items])) if faq_items else ''}
    <div class="art-cta">
      <div><h3>Need a better website?</h3><p class="mute">Fixed-scope packages from $3,500.</p></div>
      <a class="btn or" href="packages.html">View Packages</a>
    </div>
  </div>
</article>

<section class="wrap">
  <div class="split">
    <span class="dot">Keep reading</span>
    <div class="blist">{related}</div>
  </div>
</section>
<div class="sec tight"></div>

{footer()}""" + tail()


# ---------------------------------------------------------------- write
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(HERE / "images", OUT / "images")
    for f in ["styles.css", "site.js"]:
        shutil.copy(HERE / f, OUT / f)
    (OUT / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -45 224 224"><rect x="-10" y="-45" width="224" height="224" rx="36" fill="#0E0E0E"/><path fill="#fff" d="{LOGO_PATH}"/></svg>')

    out = {
        "index.html": home(), "websites.html": websites(), "packages.html": packages(), "work.html": work(),
        "website-work.html": website_work(), "design-support.html": design_support(), "design-plans.html": design_plans(),
        "about.html": about(), "start.html": start(), "thanks.html": thanks(), "website-offer.html": offer(),
        "privacy.html": legal("privacy"), "terms.html": legal("terms"), "404.html": notfound(),
    }
    for i, p in enumerate(real()):
        out[f"project-{p['slug']}.html"] = project(p, i)
    out["blog.html"] = blog_index()
    for post in POSTS:
        out[f"blog-{post['slug']}.html"] = blog_post(post)
    for name, s in out.items():
        (OUT / name).write_text(s)

    # redirects from the old WordPress site + clean URLs from the strategy doc
    red = ["# Old WordPress addresses", "/portfolio/  /work  301", "/portfolio  /work  301",
           "/our-services/  /websites  301", "/our-services  /websites  301",
           "/leave-us-a-note/  /start  301", "/leave-us-a-note  /start  301",
           "/portfolio-category/web-design/*  /website-work  301", "/portfolio-category/*  /work  301"]
    for p in PROJECTS:
        if p.get("old"):
            red.append(f"/portfolio-item/{p['old']}/  /project-{p['slug']}  301")
            red.append(f"/portfolio-item/{p['old']}  /project-{p['slug']}  301")
    red += ["/portfolio-item/*  /work  301", "", "# Routes from the strategy doc",
            "/websites/pricing  /packages  301", "/work/websites  /website-work  301",
            "/design-support/pricing  /design-plans  301"]
    (OUT / "_redirects").write_text("\n".join(red) + "\n")
    urls = ["" if n == "index.html" else n[:-5] for n in out if n not in ("404.html", "thanks.html")]
    sm = "".join(f"<url><loc>https://dsptchdesign.com/{u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://dsptchdesign.com/sitemap.xml\n")
    (OUT / "netlify.toml").write_text('[build]\n  publish = "."\n')

    # preview entry (body-only home page for the Artifact preview)
    (HERE.parent / "preview-index.html").write_text(home(full=False))
    print("built", len(out), "pages ->", OUT)


if __name__ == "__main__":
    build()
