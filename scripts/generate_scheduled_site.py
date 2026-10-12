#!/usr/bin/env python3
"""Generate a polished, dependency-free website for each five-hour UTC slot."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from html import escape
from pathlib import Path


INTERVAL_SECONDS = 5 * 60 * 60
ROOT = Path(__file__).resolve().parents[1] / "webs"

CONCEPTS = (
    {
        "slug": "northstar",
        "eyebrow": "Decision intelligence",
        "title": "Move from signals to decisions.",
        "lead": "Northstar gives product teams one calm, precise view of the metrics that shape sustainable growth.",
        "cta": "Explore the platform",
        "secondary": "View methodology",
        "accent": "#ff5a36",
        "ink": "#18211d",
        "paper": "#f4f1e8",
        "panel": "#fffdf7",
        "muted": "#69726d",
        "metrics": (("42%", "faster planning"), ("3.1×", "signal clarity"), ("18h", "saved weekly")),
        "services": (("01", "Unified context", "Bring product, customer and revenue signals into one legible operating view."), ("02", "Decision rooms", "Turn reviews into focused sessions with owners, evidence and clear next moves."), ("03", "Durable learning", "Keep the reasoning behind every decision available to the whole organization.")),
    },
    {
        "slug": "form-studio",
        "eyebrow": "Architecture & interiors",
        "title": "Spaces with a point of view.",
        "lead": "Form Studio designs tactile places that feel inevitable: generous in daylight, honest in material and exact in detail.",
        "cta": "See selected work",
        "secondary": "Start a project",
        "accent": "#bd4d2d",
        "ink": "#27231f",
        "paper": "#e9e2d5",
        "panel": "#f7f3eb",
        "muted": "#716b63",
        "metrics": (("27", "built projects"), ("11", "design awards"), ("8", "cities")),
        "services": (("01", "Residential", "Homes shaped around rituals, landscape and the changing quality of light."), ("02", "Hospitality", "Memorable environments where service, identity and spatial rhythm align."), ("03", "Adaptive reuse", "Existing structures reworked with restraint, care and a clear contemporary layer.")),
    },
    {
        "slug": "common-table",
        "eyebrow": "Seasonal kitchen",
        "title": "A table worth gathering around.",
        "lead": "Common Table serves bright, ingredient-led cooking from nearby farms, small fisheries and people we know by name.",
        "cta": "Reserve a table",
        "secondary": "View today’s menu",
        "accent": "#d84b2a",
        "ink": "#16372a",
        "paper": "#efe9d8",
        "panel": "#faf7ed",
        "muted": "#617066",
        "metrics": (("14", "local growers"), ("4", "seasonal menus"), ("0", "waste to landfill")),
        "services": (("01", "Lunch", "Simple plates, warm bread and produce at its most expressive."), ("02", "Dinner", "A generous evening menu made for sharing across the whole table."), ("03", "Private dining", "Thoughtful menus and an intimate room for your most important gatherings.")),
    },
    {
        "slug": "fieldwork",
        "eyebrow": "Independent creative practice",
        "title": "Identity that earns attention.",
        "lead": "Fieldwork builds clear brands for ambitious teams through strategy, language and design that work as one system.",
        "cta": "View our work",
        "secondary": "Meet the studio",
        "accent": "#3657d6",
        "ink": "#17191e",
        "paper": "#ecebe6",
        "panel": "#faf9f5",
        "muted": "#666970",
        "metrics": (("36", "brands launched"), ("12", "markets entered"), ("91%", "client referrals")),
        "services": (("01", "Positioning", "Find the useful truth your organization can own and act on."), ("02", "Identity", "Build a visual and verbal system with distinction, range and discipline."), ("03", "Launch", "Bring the idea to market through the moments that matter most.")),
    },
    {
        "slug": "meridian",
        "eyebrow": "Strategy for complex change",
        "title": "Clarity before momentum.",
        "lead": "Meridian helps leadership teams make consequential choices, align the organization and move with confidence.",
        "cta": "How we work",
        "secondary": "Read our perspective",
        "accent": "#c54a34",
        "ink": "#182432",
        "paper": "#e9edf0",
        "panel": "#f8fafb",
        "muted": "#66717c",
        "metrics": (("64", "transformations"), ("19", "countries"), ("4.8/5", "partner rating")),
        "services": (("01", "Direction", "Translate ambiguity into a small set of choices people can understand."), ("02", "Alignment", "Connect leadership intent to the operating decisions that make it real."), ("03", "Delivery", "Build a practical cadence that keeps change moving and learning visible.")),
    },
)


def slot_for(moment: datetime) -> int:
    return int(moment.timestamp()) // INTERVAL_SECONDS


def slot_datetime(slot: int) -> datetime:
    return datetime.fromtimestamp(slot * INTERVAL_SECONDS, tz=timezone.utc)


def render_html(concept: dict[str, object], generated_at: datetime, edition: int) -> str:
    metrics = "".join(
        f'<div><strong>{escape(value)}</strong><span>{escape(label)}</span></div>'
        for value, label in concept["metrics"]
    )
    services = "".join(
        f'<article><span>{number}</span><h3>{escape(title)}</h3><p>{escape(body)}</p></article>'
        for number, title, body in concept["services"]
    )
    stamp = generated_at.strftime("%d %b %Y · %H:%M UTC")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(str(concept['lead']))}">
  <title>{escape(str(concept['slug']).replace('-', ' ').title())} — Edition {edition:03d}</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="#top" aria-label="Home"><i></i>{escape(str(concept['slug']).replace('-', ' '))}</a>
    <button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" aria-label="Primary navigation"><a href="#work">Expertise</a><a href="#about">About</a><a class="nav-cta" href="#contact">Contact</a></nav>
  </header>
  <main id="top">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">{escape(str(concept['eyebrow']))}</p>
        <h1>{escape(str(concept['title']))}</h1>
        <p class="lead">{escape(str(concept['lead']))}</p>
        <div class="actions"><a class="button" href="#work">{escape(str(concept['cta']))}</a><a class="text-link" href="#about">{escape(str(concept['secondary']))} <span>↗</span></a></div>
      </div>
      <div class="hero-art" aria-hidden="true"><div class="frame"><span>05</span><b></b><em>Edition<br>{edition:03d}</em></div><div class="disc"></div></div>
    </section>
    <section class="metrics" aria-label="Highlights">{metrics}</section>
    <section class="work" id="work">
      <div class="section-heading"><p class="eyebrow">What we do</p><h2>Focused expertise.<br>Measurable progress.</h2></div>
      <div class="service-grid">{services}</div>
    </section>
    <section class="statement" id="about"><p>Good work creates movement without creating noise.</p><div><span>Our principle</span><strong>Useful over impressive.<br>Specific over familiar.</strong></div></section>
  </main>
  <footer id="contact"><div><p class="eyebrow">Start a conversation</p><a href="mailto:hello@example.com">hello@example.com</a></div><p>Generated {stamp}<br>Five-hour design study · no gradients</p></footer>
  <script src="script.js"></script>
</body>
</html>
'''


def render_css(concept: dict[str, object]) -> str:
    return f''':root{{--ink:{concept['ink']};--paper:{concept['paper']};--panel:{concept['panel']};--accent:{concept['accent']};--muted:{concept['muted']};--line:color-mix(in srgb,var(--ink) 18%,transparent);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);background:var(--paper);font-synthesis:none}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;min-width:320px}}a{{color:inherit;text-decoration:none}}.site-header{{height:92px;display:flex;align-items:center;justify-content:space-between;padding:0 clamp(24px,6vw,96px);border-bottom:1px solid var(--line);position:relative;z-index:10}}.brand{{font-weight:800;text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;display:flex;gap:12px;align-items:center}}.brand i{{display:block;width:13px;height:13px;background:var(--accent);border-radius:50%}}nav{{display:flex;gap:36px;align-items:center;font-size:.88rem;font-weight:650}}nav a:not(.nav-cta):hover{{color:var(--accent)}}.nav-cta{{border:1px solid var(--ink);padding:11px 18px;border-radius:99px}}.menu{{display:none;border:0;background:none;color:inherit;font:inherit}}.hero{{min-height:calc(100vh - 92px);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(360px,.9fr);padding:clamp(64px,10vw,152px) clamp(24px,6vw,96px);gap:7vw;align-items:center}}.eyebrow{{margin:0 0 26px;text-transform:uppercase;letter-spacing:.18em;font-weight:750;font-size:.72rem}}h1{{font-family:Georgia,"Times New Roman",serif;font-size:clamp(4.2rem,9vw,9.6rem);font-weight:400;letter-spacing:-.065em;line-height:.82;margin:0;max-width:9ch}}.lead{{font-size:clamp(1.05rem,1.4vw,1.28rem);line-height:1.65;color:var(--muted);max-width:590px;margin:40px 0}}.actions{{display:flex;align-items:center;gap:28px;flex-wrap:wrap}}.button{{background:var(--ink);color:var(--panel);padding:16px 23px;border-radius:3px;font-weight:700;font-size:.9rem}}.button:hover{{background:var(--accent)}}.text-link{{font-weight:700;font-size:.9rem;border-bottom:1px solid var(--line);padding:14px 0}}.text-link span{{color:var(--accent);margin-left:8px}}.hero-art{{height:min(66vw,650px);max-height:650px;min-height:450px;background:var(--panel);border:1px solid var(--line);position:relative;overflow:hidden}}.frame{{position:absolute;inset:8%;border:1px solid var(--ink)}}.frame span{{position:absolute;top:18px;left:20px;font-size:.7rem;letter-spacing:.15em}}.frame b{{position:absolute;width:54%;aspect-ratio:1;border:1px solid var(--ink);border-radius:50%;top:20%;left:23%}}.frame b::before,.frame b::after{{content:"";position:absolute;background:var(--accent)}}.frame b::before{{height:1px;width:150%;left:-25%;top:50%;transform:rotate(-35deg)}}.frame b::after{{width:28px;height:28px;border-radius:50%;left:calc(50% - 14px);top:calc(50% - 14px)}}.frame em{{position:absolute;bottom:20px;right:20px;text-align:right;font-style:normal;font-family:Georgia,serif;font-size:1.1rem}}.disc{{position:absolute;width:120px;height:120px;border-radius:50%;background:var(--accent);right:-45px;bottom:12%}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:0 clamp(24px,6vw,96px)}}.metrics div{{padding:42px 4vw;border-right:1px solid var(--line)}}.metrics div:first-child{{padding-left:0}}.metrics div:last-child{{border:0}}.metrics strong{{font-family:Georgia,serif;font-size:clamp(2.3rem,4vw,4rem);font-weight:400;display:block}}.metrics span{{color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.12em}}.work{{padding:clamp(90px,12vw,170px) clamp(24px,6vw,96px);background:var(--panel)}}.section-heading{{display:grid;grid-template-columns:1fr 2fr;margin-bottom:80px}}h2{{font-family:Georgia,serif;font-size:clamp(3rem,6vw,6.5rem);font-weight:400;letter-spacing:-.055em;line-height:.96;margin:0}}.service-grid{{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line)}}.service-grid article{{padding:32px 38px 12px 0;border-right:1px solid var(--line);min-height:260px}}.service-grid article+article{{padding-left:38px}}.service-grid article:last-child{{border:0}}.service-grid span{{color:var(--accent);font-weight:800;font-size:.75rem}}h3{{font-size:1.15rem;margin:55px 0 18px}}.service-grid p{{color:var(--muted);line-height:1.7;font-size:.94rem;max-width:35ch}}.statement{{padding:clamp(90px,13vw,180px) clamp(24px,6vw,96px);display:grid;grid-template-columns:1fr 1fr;gap:8vw}}.statement>p{{font-family:Georgia,serif;font-size:clamp(2.5rem,5vw,5.5rem);line-height:.95;letter-spacing:-.045em;margin:0}}.statement div{{border-left:1px solid var(--line);padding-left:40px;align-self:end}}.statement span{{display:block;text-transform:uppercase;letter-spacing:.15em;font-size:.7rem;color:var(--muted);margin-bottom:18px}}.statement strong{{font-size:1.15rem;line-height:1.55}}footer{{background:var(--ink);color:var(--panel);padding:80px clamp(24px,6vw,96px);display:flex;justify-content:space-between;align-items:end;gap:32px}}footer a{{font-family:Georgia,serif;font-size:clamp(2rem,5vw,5rem);letter-spacing:-.04em}}footer>p{{color:color-mix(in srgb,var(--panel) 65%,transparent);font-size:.75rem;line-height:1.6;text-align:right}}@media(max-width:820px){{.site-header{{height:76px}}.menu{{display:block}}nav{{display:none;position:absolute;top:76px;left:0;right:0;background:var(--panel);padding:24px;flex-direction:column;align-items:flex-start;border-bottom:1px solid var(--line)}}nav.open{{display:flex}}.hero{{grid-template-columns:1fr;padding-top:80px}}h1{{font-size:clamp(3.8rem,18vw,6.6rem)}}.hero-art{{min-height:380px;height:120vw}}.metrics{{grid-template-columns:1fr}}.metrics div{{border-right:0;border-bottom:1px solid var(--line);padding:28px 0}}.section-heading,.statement{{grid-template-columns:1fr;gap:45px}}.service-grid{{grid-template-columns:1fr}}.service-grid article,.service-grid article+article{{padding:30px 0;border-right:0;border-bottom:1px solid var(--line);min-height:0}}.statement div{{border-left:0;border-top:1px solid var(--line);padding:30px 0 0}}footer{{align-items:flex-start;flex-direction:column}}footer>p{{text-align:left}}}}@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}'''


SCRIPT = '''const menu=document.querySelector('.menu');const nav=document.querySelector('#nav');menu?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});nav?.addEventListener('click',()=>{nav.classList.remove('open');menu?.setAttribute('aria-expanded','false');});'''


def load_json(path: Path, fallback: object) -> object:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_site(root: Path, slot: int, edition: int) -> dict[str, object]:
    generated_at = slot_datetime(slot)
    concept = CONCEPTS[slot % len(CONCEPTS)]
    folder_name = f"{generated_at:%Y-%m-%dT%H-%MZ}-{concept['slug']}"
    destination = root / "sites" / folder_name
    destination.mkdir(parents=True, exist_ok=True)
    files = {
        "index.html": render_html(concept, generated_at, edition),
        "styles.css": render_css(concept),
        "script.js": SCRIPT + "\n",
    }
    for name, content in files.items():
        (destination / name).write_text(content, encoding="utf-8")
        shutil.copyfile(destination / name, root / name)
    return {"edition": edition, "slot": slot, "generated_at": generated_at.isoformat(), "concept": concept["slug"], "path": f"sites/{folder_name}/"}


def generate(root: Path, now: datetime, force: bool = False) -> list[dict[str, object]]:
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / "state.json"
    catalog_path = root / "catalog.json"
    state = load_json(state_path, {})
    catalog = load_json(catalog_path, [])
    assert isinstance(state, dict) and isinstance(catalog, list)
    current_slot = slot_for(now)
    last_slot = state.get("last_slot")
    if force or last_slot is None:
        slots = [current_slot]
    else:
        slots = list(range(int(last_slot) + 1, current_slot + 1))
    created = []
    for slot in slots:
        entry = write_site(root, slot, len(catalog) + 1)
        catalog.append(entry)
        created.append(entry)
    if created:
        state_path.write_text(json.dumps({"last_slot": current_slot, "last_generated_at": slot_datetime(current_slot).isoformat()}, indent=2) + "\n", encoding="utf-8")
        catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Generate the current slot even if it already exists")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    created = generate(args.root.resolve(), datetime.now(timezone.utc), force=args.force)
    if created:
        for entry in created:
            print(f"Generated edition {entry['edition']}: {entry['path']}")
    else:
        print("No five-hour slot is due")


if __name__ == "__main__":
    main()
