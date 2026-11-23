"""Builds the whole website from products.csv + site.json into the dist/ folder."""
import csv, json, html, shutil
from pathlib import Path
R = Path(__file__).parent
S = json.loads((R / "site.json").read_text(encoding="utf-8"))
B = S.get("base_path", "").rstrip("/")
U = S["site_url"].rstrip("/")
NAME = S["site_name"]
e = html.escape
D = R / "dist"

CATS = [
 dict(slug="home-finds", title="Home Finds Worth Buying", nav="Home Finds", tint="#dfe8dc",
  short="Useful home products and clever household solutions worth a second look.",
  seo="Home Finds Worth Buying | " + NAME,
  meta="Practical home finds and clever household products, chosen for everyday usefulness.",
  intro=["A good home find does one small job well. It saves a few minutes, removes a daily annoyance or makes a room work better.",
         "This page collects useful household products that fit real routines. Each listing explains the problem it solves and who is likely to benefit."]),
 dict(slug="kitchen-gadgets", title="Kitchen Gadgets & Essentials", nav="Kitchen", tint="#efe4cf",
  short="Kitchen tools, cooking accessories and food storage that earn their drawer space.",
  seo="Kitchen Gadgets & Essentials | " + NAME,
  meta="Kitchen gadgets, cooking accessories and food storage ideas that make cooking and cleaning up easier.",
  intro=["Most kitchens have a few tools that get used daily and many that never do. This page focuses on the first group.",
         "Browse kitchen essentials, cooking accessories and storage ideas, each with a plain description of what it does and who it suits."]),
 dict(slug="home-organisation", title="Smart Home Organisation", nav="Organisation", tint="#dde3e0",
  short="Storage solutions and space-saving ideas for wardrobes, shelves and small spaces.",
  seo="Smart Home Organisation & Storage Solutions | " + NAME,
  meta="Storage solutions, space-saving products and wardrobe organisation ideas for a tidier home.",
  intro=["Clutter is usually a storage problem, not a discipline problem. The right container or shelf can change how a space feels.",
         "Here you will find storage solutions and space-saving products for wardrobes, cupboards and small rooms."]),
 dict(slug="everyday-gadgets", title="Clever Everyday Gadgets", nav="Gadgets", tint="#e8e0d6",
  short="Practical gadgets and accessories that solve small daily problems.",
  seo="Clever Everyday Gadgets | " + NAME,
  meta="Useful gadgets and practical accessories that solve everyday problems at home and on the go.",
  intro=["The best gadgets are the ones you stop noticing because they simply make things easier.",
         "This page lists practical accessories and gadgets, with a clear note on the everyday problem each one addresses."]),
 dict(slug="product-recommendations", title="Amazon Finds & Recommendations", nav="Recommendations", tint="#d8e2d2",
  short="Carefully selected product discoveries and useful shopping recommendations.",
  seo="Amazon Finds & Product Recommendations | " + NAME,
  meta="Carefully selected product recommendations and useful finds, with links to check details on Amazon.",
  intro=["These are products that stood out as useful, well matched to a real need and worth a closer look.",
         "Every listing links to Amazon, where you can check current price, availability and customer reviews before you decide."]),
]
CAT = {c["slug"]: c for c in CATS}
DISC = "As an Amazon Associate I earn from qualifying purchases."
DISC2 = "Some links on this site may earn us a commission at no additional cost to you."

def load_products():
    out = []
    with open(R / "products.csv", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = {k: (v or "").strip() for k, v in r.items() if k}
            if not r.get("name") or r.get("category") not in CAT:
                continue
            r["features"] = [x.strip() for x in r["features"].split(";") if x.strip()]
            out.append(r)
    return out
P = load_products()

def head(title, desc, path, extra=""):
    url = U + path
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:site_name" content="{e(NAME)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&family=Fraunces:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{B}/style.css">{extra}</head><body><a class="skip" href="#main">Skip to content</a>"""

def header(cur=""):
    li = "".join(f'<li><a href="{B}/{c["slug"]}/"{" aria-current=\"page\"" if c["slug"]==cur else ""}>{e(c["nav"])}</a></li>' for c in CATS)
    return f"""<header class="top"><div class="wrap bar"><a class="logo" href="{B}/">{e(NAME)}</a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<form class="sform" action="{B}/search/" method="get" role="search"><input type="search" name="q" placeholder="Search finds" aria-label="Search finds"><button type="submit">Search</button></form>
<nav id="nav" aria-label="Main"><ul>{li}</ul></nav></div></header><main id="main">"""

def footer():
    soc = "".join(f'<li><a href="{e(S[k])}" rel="noopener" target="_blank">{n}</a></li>' for k, n in
                  [("pinterest_url", "Pinterest"), ("instagram_url", "Instagram"), ("facebook_url", "Facebook")] if S.get(k))
    pages = [("about", "About Us"), ("contact", "Contact"), ("privacy-policy", "Privacy Policy"), ("affiliate-disclosure", "Affiliate Disclosure"), ("terms", "Terms of Use")]
    li = "".join(f'<li><a href="{B}/{s}/">{n}</a></li>' for s, n in pages)
    return f"""</main><footer><div class="wrap"><ul>{li}</ul><ul>{soc}</ul>
<p>{DISC} {DISC2}</p><p>{e(NAME)} is not operated by or affiliated with Amazon.</p><p>&copy; <span id="y"></span> {e(NAME)}</p></div></footer>
<script>document.getElementById('y').textContent=new Date().getFullYear()</script><script src="{B}/app.js" defer></script></body></html>"""

def disc_box():
    return f'<p class="disc"><strong>{DISC}</strong> {DISC2} <a href="{B}/affiliate-disclosure/">Read our disclosure</a>.</p>'

def img_src(v):
    return v if v.startswith("http") else f"{B}/images/{v}"

def card(p):
    c = CAT[p["category"]]
    pic = (f'<img src="{e(img_src(p["image"]))}" alt="{e(p.get("image_alt") or p["name"])}" loading="lazy" width="400" height="400">'
           if p["image"] else "<span>Product image to come</span>")
    ph = p["status"].lower() != "live"
    b = ""
    if p["price"] and not ph: b += f'<p class="tag">Price: {e(p["price"])}</p>'
    if p["rating"] and not ph: b += f'<p class="tag">Rating: {e(p["rating"])}</p>'
    if p["problem"]: b += f'<p><strong>Solves:</strong> {e(p["problem"])}</p>'
    if p["features"]: b += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in p["features"]) + "</ul>"
    if p["who"]: b += f'<p><strong>Useful for:</strong> {e(p["who"])}</p>'
    btn = (f'<a class="btn" href="{e(p["url"])}" target="_blank" rel="sponsored nofollow noopener">Check Product on Amazon</a>'
           if p["url"] else '<span class="btn off" aria-disabled="true">Link coming soon</span>')
    txt = " ".join([p["name"], c["title"], p["description"], " ".join(p["features"])]).lower()
    return (f'<article class="card" data-cat="{c["slug"]}" data-search="{e(txt)}"><div class="pimg">{pic}</div><div class="pb">'
            f'<span class="tag">{e(c["title"])}</span>{"<span class=badge>Placeholder</span>" if ph else ""}'
            f'<h3>{e(p["name"])}</h3><p>{e(p["description"])}</p>{b}<span class="sp"></span>{btn}</div></article>')

def cat_card(c):
    img = (f'<img src="{B}/images/cat-{c["slug"]}.jpg" alt="{e(c["title"])}" loading="lazy" width="400" height="300">'
           if (R / "images" / f'cat-{c["slug"]}.jpg').exists()
           else f'<div class="ph" style="background:{c["tint"]}" aria-hidden="true">{c["title"][0]}</div>')
    return (f'<a class="cat" href="{B}/{c["slug"]}/">{img}<div class="tx"><h3>{e(c["title"])}</h3><p>{e(c["short"])}</p><b>Explore Category</b></div></a>')

def write(path, content):
    f = D / path.strip("/") / "index.html" if not path.endswith(".html") else D / path.strip("/")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")

def jsonld(d):
    return '<script type="application/ld+json">' + json.dumps(d) + "</script>"

if D.exists(): shutil.rmtree(D)
D.mkdir()
shutil.copy(R / "static/style.css", D); shutil.copy(R / "static/app.js", D)
if (R / "images").exists(): shutil.copytree(R / "images", D / "images")

# Homepage
hero_img = ('<img class="hero-img" src="%s/images/hero.jpg" alt="A bright, organised kitchen with useful everyday products" width="600" height="600">' % B
            if (R / "images/hero.jpg").exists()
            else '<div class="mosaic" aria-hidden="true">' + "".join(f'<div style="background:{c["tint"]}">{e(c["nav"])}</div>' for c in CATS[:4]) + "</div>")
feat = [p for p in P if p["featured"].lower() in ("yes", "y", "true", "1")]
chips = '<div class="chips" role="group" aria-label="Filter featured finds"><button class="chip" aria-pressed="true" data-cat="all">All</button>' + "".join(
    f'<button class="chip" aria-pressed="false" data-cat="{c["slug"]}">{e(c["nav"])}</button>' for c in CATS) + "</div>"
ld = jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": U + "/",
             "potentialAction": {"@type": "SearchAction", "target": U + "/search/?q={q}", "query-input": "required name=q"}})
home = head(f"{NAME} | Clever Home & Kitchen Finds", "Discover practical home essentials, clever kitchen gadgets and useful everyday products worth discovering.", "/", ld) + header() + f"""
<div class="wrap hero"><div><h1>Discover Clever Finds That Make Everyday Life Easier.</h1>
<p>Explore practical home essentials, clever kitchen gadgets and useful everyday products worth discovering.</p>
<a class="btn" href="#categories">Explore Our Finds</a></div>{hero_img}</div>
<section class="alt" id="categories"><div class="wrap"><h2>Shop by category</h2><div class="cats">{"".join(cat_card(c) for c in CATS)}</div></div></section>
<section id="featured"><div class="wrap"><h2>Featured finds</h2>{disc_box()}{chips}
<div class="grid">{"".join(card(p) for p in feat)}</div>
<div class="empty" id="f-empty" {"" if not feat else "hidden"}>No featured finds in this category yet. Check back soon.</div></div></section>
<section class="alt"><div class="wrap"><h2>Why discover with us?</h2><div class="why">
<div><h3>Practical product discoveries</h3><p>We look for products that solve a real, specific problem.</p></div>
<div><h3>Useful ideas for everyday living</h3><p>Ideas for the kitchen, storage and daily routines that are easy to put to use.</p></div>
<div><h3>Carefully selected recommendations</h3><p>Every listing explains what it does and who it suits, so you can decide for yourself.</p></div></div></div></section>""" + footer()
write("/", home)

# Category pages
for c in CATS:
    items = [p for p in P if p["category"] == c["slug"]]
    others = [p for p in P if p["category"] != c["slug"]][:3]
    ld = jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": U + "/"},
        {"@type": "ListItem", "position": 2, "name": c["title"], "item": f'{U}/{c["slug"]}/'}]})
    body = f"""<div class="wrap"><p class="crumb"><a href="{B}/">Home</a> / {e(c["title"])}</p><h1>{e(c["title"])}</h1>
<p style="max-width:40em">{e(c["intro"][0])}</p><p style="max-width:40em;color:var(--m)">{e(c["intro"][1])}</p>{disc_box()}
{'<div class="grid">' + "".join(card(p) for p in items) + "</div>" if items else '<div class="empty"><h3>New finds are on the way</h3><p>Nothing is listed here yet. Browse another category in the meantime.</p></div>'}</div>
<section class="alt" style="margin-top:40px"><div class="wrap"><h2>Explore more categories</h2><div class="cats">{"".join(cat_card(x) for x in CATS if x is not c)}</div>
{'<h2 style="margin-top:36px">You might also like</h2><div class="grid">' + "".join(card(p) for p in others) + "</div>" if others else ""}</div></section>"""
    write("/" + c["slug"], head(c["seo"], c["meta"], f'/{c["slug"]}/', ld) + header(c["slug"]) + body + footer())

# Search
write("/search", head(f"Search finds | {NAME}", "Search product finds by name or category.", "/search/", '<meta name="robots" content="noindex,follow">') + header() + f"""
<div class="wrap"><h1 style="margin-top:28px">Search finds</h1><form class="sform" onsubmit="return false" style="max-width:480px;margin-bottom:12px"><input id="q" type="search" placeholder="Search by name or category" aria-label="Search" style="flex:1;width:auto"></form>
<p class="tag" id="count" aria-live="polite"></p>{disc_box()}<div class="grid" id="results">{"".join(card(p) for p in P)}</div>
<div class="empty" id="s-empty" hidden><h3>No finds match that search</h3><p>Try a simpler word, or browse a category from the menu.</p></div></div>""" + footer())

# Info pages
em = S["contact_email"]
INFO = {
 "about": ("About Us", f"{NAME} is a product discovery site. We look for practical home products, kitchen tools and everyday gadgets, and explain in plain language what each one does and who it suits.</p><p>We are not a store. When you choose to buy, you will go to Amazon to check the current price, availability and reviews.</p><p>Some links on this site are affiliate links, explained on our <a href=\"{B}/affiliate-disclosure/\">disclosure page</a>."),
 "contact": ("Contact", f"Questions, corrections or suggestions are welcome. Email us at <a href=\"mailto:{e(em)}\">{e(em)}</a>."),
 "privacy-policy": ("Privacy Policy", "This site does not ask you to create an account and does not sell products directly. We may use basic analytics to understand which pages are popular. If you add analytics or advertising tools, list them here.</p><p>When you click a link to Amazon, Amazon's own privacy policy applies on its site. Amazon may use cookies to record that you came from our link.</p><p>For questions about your data, contact us using the details on the Contact page."),
 "affiliate-disclosure": ("Affiliate Disclosure", f"<strong>{DISC}</strong></p><p>{DISC2} Our recommendations are based on usefulness, not on commission rates.</p><p>We do not invent reviews, ratings or discounts. Price and availability are shown on Amazon and may change at any time. {e(NAME)} is not operated by or affiliated with Amazon."),
 "terms": ("Terms of Use", "Content on this site is for general information and shopping inspiration. Product details, prices and availability are controlled by Amazon and may change without notice, so always check the product page before buying.</p><p>We try to keep information accurate but cannot guarantee it is complete or current. Links to other sites are provided for convenience, and we are not responsible for their content."),
}
for s, (t, txt) in INFO.items():
    write("/" + s, head(f"{t} | {NAME}", f"{t} for {NAME}.", f"/{s}/") + header() + f'<div class="wrap prose"><h1>{t}</h1><p>{txt}</p></div>' + footer())
write("/404.html", head(f"Page not found | {NAME}", "Page not found.", "/404.html", '<meta name="robots" content="noindex">') + header() + f'<div class="wrap prose"><h1>Page not found</h1><p>That page does not exist. Try the <a href="{B}/">homepage</a> or search for a find.</p></div>' + footer())

# Sitemap + robots
urls = ["/"] + [f'/{c["slug"]}/' for c in CATS] + [f"/{s}/" for s in INFO]
(D / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{U}{u}</loc></url>" for u in urls) + "</urlset>", encoding="utf-8")
(D / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /search/\nSitemap: {U}/sitemap.xml\n")
print("Built", len(urls) + 2, "pages,", len(P), "products")
