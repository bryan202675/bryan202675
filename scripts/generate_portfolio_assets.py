#!/usr/bin/env python3
"""Generate compact, self-contained SVGs for the profile below its hero."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "profile"

STYLE = """
text{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}
.title{fill:#F8FDFF;font-size:17px;font-weight:700;letter-spacing:1.5px}
.label{fill:#F8FDFF;font-size:15px;font-weight:700}
.muted{fill:#AEBBC7;font-size:12px}
.ice{fill:#BDEFFF}
.pulse{animation:pulse 4.6s ease-in-out infinite}
.trace{animation:trace 9s linear infinite}
.reveal{animation:reveal 9s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.48}50%{opacity:1}}
@keyframes trace{to{stroke-dashoffset:-72}}
@keyframes reveal{0%,5%{opacity:.32}16%,86%{opacity:1}100%{opacity:.32}}
@media(prefers-reduced-motion:reduce){.pulse,.trace,.reveal{animation:none!important;opacity:1!important}.traveler{display:none}}
"""


def frame(title: str, description: str, height: int, content: str, *, width: int = 800) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc>
<defs><linearGradient id="ice" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#FFFFFF"/><stop offset=".55" stop-color="#DDF8FF"/><stop offset="1" stop-color="#9EE7FF"/></linearGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>{STYLE}</style></defs>
<rect width="{width}" height="{height}" rx="20" fill="#0A0A0F"/><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="19" fill="none" stroke="#DDF8FF" stroke-opacity=".18"/>
{content}
</svg>'''


def intro() -> str:
    rows = [
        "BUILDING SCALABLE DIGITAL PRODUCTS",
        "FULL STACK DEVELOPMENT",
        "AI-POWERED SYSTEMS",
        "SECURE INFRASTRUCTURE",
        "MOBILE &amp; WEB EXPERIENCES",
    ]
    lines = []
    for index, row in enumerate(rows):
        y = 78 + index * 31
        lines.append(
            f'<g class="reveal" style="animation-delay:{index * .55}s">'
            f'<circle cx="43" cy="{y-6}" r="3" fill="#BDEFFF"/><text x="61" y="{y}" fill="#F8FDFF" font-size="19">{row}</text></g>'
        )
    body = '''<circle cx="32" cy="27" r="5" fill="#FF5F57"/><circle cx="50" cy="27" r="5" fill="#FEBC2E"/><circle cx="68" cy="27" r="5" fill="#28C840"/>
<text x="400" y="32" text-anchor="middle" class="muted">profile.engineering — overview</text><path d="M24 48H776" stroke="#DDF8FF" stroke-opacity=".15"/>
''' + "".join(lines) + '''<rect x="574" y="181" width="10" height="18" rx="2" fill="#BDEFFF" class="pulse"/><text x="595" y="195" class="muted">READY TO BUILD</text>'''
    return frame("Enfoque profesional", "Terminal con cinco líneas sobre desarrollo full stack, inteligencia artificial, infraestructura y experiencias web y móviles.", 228, body)


def signal() -> str:
    groups = [("FULL STACK", "DEVELOPMENT"), ("BUILDING", "PRODUCTS"), ("OPEN SOURCE", "EXPLORATION"), ("AI", "ENGINEERING")]
    cards = []
    for index, (first, second) in enumerate(groups):
        x = 20 + index * 195
        cards.append(
            f'<g transform="translate({x} 43)" class="reveal" style="animation-delay:{index*.55}s"><rect width="184" height="78" rx="14" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".14"/>'
            f'<circle cx="20" cy="29" r="4" fill="#BDEFFF" class="pulse" style="animation-delay:{index*.5}s"/>'
            f'<text x="34" y="33" fill="#F8FDFF" font-size="13" font-weight="700">{first}</text>'
            f'<text x="34" y="54" class="muted">{second}</text></g>'
        )
    body = '<text x="25" y="29" class="muted">ENGINEERING SIGNAL / AREAS OF WORK</text>' + "".join(cards)
    return frame("Áreas de trabajo", "Cuatro áreas de especialidad sin métricas ni estados de servicios.", 142, body)


def project_art(name: str) -> str:
    if name == "axiom":
        body = '''<text x="31" y="42" class="title">AXIOM-OS</text><text x="529" y="42" text-anchor="end" class="muted">CONCEPT ART</text>
<path d="M30 60H530" stroke="#E8FAFF" stroke-opacity=".15"/>
<circle cx="280" cy="141" r="57" fill="#BDEFFF" fill-opacity=".025" stroke="#DDF8FF" stroke-opacity=".35"/>
<circle cx="280" cy="141" r="28" fill="none" stroke="url(#ice)" stroke-opacity=".75" stroke-width="2"/>
<circle cx="280" cy="141" r="7" fill="#F8FDFF" filter="url(#glow)" class="pulse"/>
<path d="M45 140H192M368 140H515M280 79V70M280 211V203" stroke="#BDEFFF" stroke-opacity=".25" stroke-dasharray="5 9" class="trace"/>
<rect x="48" y="111" width="104" height="58" rx="10" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/><path d="M65 130H130M65 142H115M65 154H135" stroke="#E8FAFF" stroke-opacity=".32"/>
<rect x="408" y="111" width="104" height="58" rx="10" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/><circle cx="438" cy="140" r="9" fill="none" stroke="#BDEFFF"/><path d="M455 140H492" stroke="#E8FAFF" stroke-opacity=".32"/>
<text x="31" y="260" class="muted">INTERFACE EXPERIMENT / HTML · CSS · JAVASCRIPT</text>'''
        title = "Axiom-OS, experimento de interfaz"
        description = "Arte conceptual del experimento visual Axiom-OS; no es una captura real."
    else:
        body = '''<text x="31" y="42" class="title">SYNAPSE</text><text x="529" y="42" text-anchor="end" class="muted">CONCEPT ART</text>
<path d="M30 60H530" stroke="#E8FAFF" stroke-opacity=".15"/>
<rect x="52" y="84" width="456" height="151" rx="13" fill="#121920" stroke="#BDEFFF" stroke-opacity=".18"/>
<path d="M52 113H508" stroke="#BDEFFF" stroke-opacity=".18"/><circle cx="72" cy="99" r="4" fill="#BDEFFF" opacity=".55"/><circle cx="87" cy="99" r="4" fill="#BDEFFF" opacity=".35"/>
<text x="77" y="154" fill="#F8FDFF" font-size="20" font-weight="700">Interface study</text><path d="M77 171H272M77 186H225" stroke="#E8FAFF" stroke-opacity=".35" stroke-width="3"/>
<rect x="340" y="132" width="115" height="64" rx="10" fill="#BDEFFF" fill-opacity=".07" stroke="#BDEFFF" stroke-opacity=".5"/>
<circle cx="371" cy="165" r="12" fill="none" stroke="#BDEFFF"/><circle cx="420" cy="153" r="8" fill="none" stroke="#BDEFFF"/>
<path d="M382 162L412 155" stroke="#BDEFFF" stroke-opacity=".7" stroke-dasharray="5 6" class="trace"/>
<text x="31" y="260" class="muted">LANDING PAGE EXPERIMENT / HTML · CSS</text>'''
        title = "Synapse, experimento de landing page"
        description = "Arte conceptual del experimento Synapse; no es una captura real."
    return frame(title, description, 280, body, width=560)


def stack() -> str:
    groups = [
        ("FRONTEND", "React · TypeScript · JavaScript · Vite"),
        ("BACKEND", "Supabase · Auth · API integration"),
        ("DATABASE", "PostgreSQL · Firebase (learning)"),
        ("MOBILE", "React Native · Expo"),
        ("AI + AUTOMATION", "Claude · Codex · Python · Bash"),
        ("INFRA + SECURITY", "Git · GitHub · Vercel · Kali Linux"),
    ]
    cards = []
    for index, (heading, detail) in enumerate(groups):
        column, row = index % 2, index // 2
        x, y = 22 + column * 390, 70 + row * 109
        cards.append(
            f'<g transform="translate({x} {y})" class="reveal" style="animation-delay:{index*.5}s"><rect width="366" height="92" rx="14" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".15"/>'
            f'<circle cx="23" cy="31" r="5" fill="#BDEFFF" class="pulse" style="animation-delay:{index*.4}s"/>'
            f'<text x="41" y="36" class="label">{heading}</text><text x="22" y="68" class="muted">{detail}</text></g>'
        )
    body = '''<text x="23" y="35" class="title">TECH STACK / CONNECTED PRACTICE</text>
<path d="M400 62V390" stroke="#BDEFFF" stroke-opacity=".23" stroke-dasharray="5 10" class="trace"/>''' + "".join(cards)
    return frame("Mapa de tecnologías", "Seis grupos de tecnología: frontend, backend, bases de datos, móvil, inteligencia artificial e infraestructura.", 404, body)


def delivery() -> str:
    nodes = [
        ("01", "IDEA", 46, 64), ("02", "DESIGN", 300, 64), ("03", "DEVELOPMENT", 554, 64),
        ("06", "MONITORING", 46, 164), ("05", "DEPLOYMENT", 300, 164), ("04", "TESTING", 554, 164),
    ]
    path = "M246 104H300M500 104H554M654 144V164M554 204H500M300 204H246"
    cards = []
    for number, label, x, y in nodes:
        cards.append(f'<g transform="translate({x} {y})"><rect width="200" height="80" rx="14" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/><circle cx="27" cy="27" r="5" fill="#BDEFFF" class="pulse"/><text x="45" y="31" class="muted">{number}</text><text x="27" y="57" class="label">{label}</text></g>')
    body = f'''<text x="23" y="35" class="title">FROM IDEA TO PRODUCTION</text><path d="{path}" fill="none" stroke="#BDEFFF" stroke-opacity=".48" stroke-width="2" stroke-dasharray="5 8" class="trace"/>
<circle r="4" fill="#F8FDFF" class="traveler" filter="url(#glow)"><animateMotion path="M146 104H654V204H146" dur="16s" repeatCount="indefinite"/></circle>'''
    body += "".join(cards)
    return frame("Del concepto a producción", "Flujo conceptual de idea, diseño, desarrollo, pruebas, despliegue y monitoreo.", 260, body)


def architecture() -> str:
    groups = [("CLIENT", "WEB / MOBILE"), ("API", "REQUESTS"), ("SERVICES", "APPLICATION"), ("DATABASE", "PERSISTENCE")]
    cards = []
    for index, (name, subline) in enumerate(groups):
        x = 22 + index * 195
        cards.append(
            f'<g transform="translate({x} 91)" class="reveal" style="animation-delay:{index*.6}s"><rect width="172" height="104" rx="15" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/>'
            f'<circle cx="26" cy="29" r="7" fill="none" stroke="#BDEFFF" stroke-width="2" class="pulse" style="animation-delay:{index*.5}s"/>'
            f'<text x="24" y="64" class="label">{name}</text><text x="24" y="84" class="muted">{subline}</text></g>'
        )
    body = '''<text x="23" y="36" class="title">SYSTEM ARCHITECTURE / CONCEPTUAL VIEW</text>
<path d="M194 143H217M389 143H412M584 143H607" stroke="#BDEFFF" stroke-opacity=".6" stroke-width="2" stroke-dasharray="5 7" class="trace"/>''' + "".join(cards)
    body += '''<circle r="4" fill="#F8FDFF" class="traveler" filter="url(#glow)"><animateMotion path="M194 143H607" dur="9s" repeatCount="indefinite"/></circle>
<text x="24" y="235" class="muted">Diagramas de referencia; cada proyecto tiene sus propias decisiones de arquitectura.</text>'''
    return frame("Arquitectura conceptual", "Flujo ilustrativo desde clientes web y móvil hasta API, servicios y base de datos; no representa un proyecto específico.", 254, body)


def activity_fallback() -> str:
    body = '''<text x="24" y="36" class="title">ENGINEERING ACTIVITY</text><text x="24" y="63" class="muted">CONTRIBUTION GRAPH / STATIC FALLBACK</text>
<path d="M25 97H775" stroke="#BDEFFF" stroke-opacity=".2" stroke-width="2"/>
<circle cx="58" cy="97" r="6" fill="#BDEFFF"/>
<path d="M58 97L119 82L178 100L244 73L304 92L366 69L429 90L491 75L557 94L620 78L691 90L750 68" fill="none" stroke="url(#ice)" stroke-opacity=".66" stroke-width="2"/>
<text x="24" y="134" class="muted">Illustrative signal only · no contribution count implied</text>'''
    return frame("Actividad de ingeniería, ilustración de respaldo", "Ilustración estática sin datos de contribución; el workflow genera el gráfico real al ejecutarse.", 151, body)


def footer() -> str:
    body = '''<path d="M25 35H775" stroke="#DDF8FF" stroke-opacity=".15"/><path d="M25 35H150" stroke="url(#ice)" stroke-width="2" stroke-dasharray="8 14" class="trace"/>
<circle cx="25" cy="35" r="4" fill="#BDEFFF" class="pulse"/><text x="400" y="66" text-anchor="middle" class="muted">BUILD · VERIFY · IMPROVE</text>'''
    return frame("Cierre del perfil", "Línea de terminal con pulso sutil y lema construir, verificar y mejorar.", 82, body)


def connect() -> str:
    body = '''<text x="30" y="45" class="title">LET'S CONNECT</text>
<text x="30" y="75" class="muted">REACT · PRODUCT · SECURITY</text>
<rect x="554" y="29" width="216" height="57" rx="12" fill="#DDF8FF" fill-opacity=".07" stroke="#DDF8FF" stroke-opacity=".48"/>
<circle cx="579" cy="57" r="5" fill="#BDEFFF" class="pulse"/>
<text x="597" y="63" fill="#F8FDFF" font-size="14" font-weight="700">OPEN GITHUB ↗</text>'''
    return frame("Abrir perfil de GitHub", "Tarjeta de contacto con enlace al perfil de GitHub.", 116, body)


def intro_mobile() -> str:
    rows = [
        "BUILDING DIGITAL PRODUCTS",
        "FULL STACK DEVELOPMENT",
        "AI-POWERED SYSTEMS",
        "SECURE INFRASTRUCTURE",
        "MOBILE &amp; WEB EXPERIENCES",
    ]
    lines = "".join(
        f'<g class="reveal" style="animation-delay:{i*.55}s"><circle cx="30" cy="{72+i*32}" r="3" fill="#BDEFFF"/>'
        f'<text x="46" y="{77+i*32}" fill="#F8FDFF" font-size="15">{row}</text></g>'
        for i, row in enumerate(rows)
    )
    body = '''<circle cx="25" cy="25" r="4" fill="#FF5F57"/><circle cx="41" cy="25" r="4" fill="#FEBC2E"/><circle cx="57" cy="25" r="4" fill="#28C840"/>
<text x="202" y="30" class="muted" font-size="11">profile.engineering</text><path d="M18 46H382" stroke="#DDF8FF" stroke-opacity=".15"/>''' + lines
    return frame("Enfoque profesional móvil", "Versión compacta de la introducción animada para teléfonos.", 254, body, width=400)


def signal_mobile() -> str:
    groups = [("FULL STACK", "DEVELOPMENT"), ("BUILDING", "PRODUCTS"), ("OPEN SOURCE", "EXPLORATION"), ("AI", "ENGINEERING")]
    cards = []
    for i, (first, second) in enumerate(groups):
        x, y = 18 + (i % 2) * 185, 61 + (i // 2) * 104
        cards.append(f'<g transform="translate({x} {y})" class="reveal" style="animation-delay:{i*.55}s"><rect width="178" height="87" rx="12" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".17"/>'
                     f'<circle cx="18" cy="27" r="4" fill="#BDEFFF" class="pulse" style="animation-delay:{i*.5}s"/>'
                     f'<text x="31" y="31" fill="#F8FDFF" font-size="14" font-weight="700">{first}</text><text x="18" y="57" class="muted">{second}</text></g>')
    return frame("Áreas de trabajo móvil", "Cuatro tarjetas de especialidad distribuidas en dos filas.", 266,
                 '<text x="19" y="32" class="muted">ENGINEERING SIGNAL</text>' + "".join(cards), width=400)


def stack_mobile() -> str:
    groups = [
        ("FRONTEND", "React · TypeScript · JavaScript"),
        ("BACKEND", "Supabase · Auth · APIs"),
        ("DATABASE", "PostgreSQL · Firebase (learning)"),
        ("MOBILE", "React Native · Expo"),
        ("AI + AUTOMATION", "Claude · Codex · Python · Bash"),
        ("INFRA + SECURITY", "Git · Vercel · Kali Linux"),
    ]
    cards = []
    for i, (heading, detail) in enumerate(groups):
        y = 59 + i * 84
        cards.append(f'<g transform="translate(18 {y})" class="reveal" style="animation-delay:{i*.45}s"><rect width="364" height="73" rx="12" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".15"/>'
                     f'<circle cx="19" cy="25" r="4" fill="#BDEFFF" class="pulse" style="animation-delay:{i*.4}s"/>'
                     f'<text x="32" y="29" fill="#F8FDFF" font-size="14" font-weight="700">{heading}</text>'
                     f'<text x="19" y="54" class="muted">{detail}</text></g>')
    return frame("Tecnologías móvil", "Mapa vertical de seis grupos de herramientas y tecnologías.", 574,
                 '<text x="19" y="33" class="muted">TECH STACK / CONNECTED PRACTICE</text>' + "".join(cards), width=400)


def delivery_mobile() -> str:
    steps = ["IDEA", "DESIGN", "DEVELOPMENT", "TESTING", "DEPLOYMENT", "MONITORING"]
    cards = []
    for i, label in enumerate(steps):
        y = 56 + i * 78
        cards.append(f'<g transform="translate(26 {y})"><rect width="348" height="65" rx="12" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/>'
                     f'<circle cx="24" cy="32" r="5" fill="#BDEFFF" class="pulse"/>'
                     f'<text x="43" y="37" class="muted">{i+1:02d}</text><text x="95" y="38" class="label">{label}</text></g>')
    body = '''<text x="19" y="32" class="muted">FROM IDEA TO PRODUCTION</text>
<path d="M50 89V479" fill="none" stroke="#BDEFFF" stroke-opacity=".45" stroke-width="2" stroke-dasharray="5 8" class="trace"/>
<circle r="4" fill="#F8FDFF" class="traveler" filter="url(#glow)"><animateMotion path="M50 89V479" dur="16s" repeatCount="indefinite"/></circle>''' + "".join(cards)
    return frame("Flujo de desarrollo móvil", "Seis pasos de idea a monitoreo en una columna.", 542, body, width=400)


def architecture_mobile() -> str:
    steps = [("CLIENT", "WEB / MOBILE"), ("API", "REQUESTS"), ("SERVICES", "APPLICATION"), ("DATABASE", "PERSISTENCE")]
    cards = []
    for i, (label, detail) in enumerate(steps):
        y = 57 + i * 86
        cards.append(f'<g transform="translate(25 {y})" class="reveal" style="animation-delay:{i*.6}s"><rect width="350" height="69" rx="12" fill="#13151D" stroke="#E8FAFF" stroke-opacity=".18"/>'
                     f'<circle cx="25" cy="34" r="6" fill="none" stroke="#BDEFFF" stroke-width="2" class="pulse"/>'
                     f'<text x="48" y="31" class="label">{label}</text><text x="48" y="50" class="muted">{detail}</text></g>')
    body = '''<text x="19" y="32" class="muted">SYSTEM ARCHITECTURE / CONCEPT</text>
<path d="M50 91V349" fill="none" stroke="#BDEFFF" stroke-opacity=".45" stroke-width="2" stroke-dasharray="5 8" class="trace"/>''' + "".join(cards)
    return frame("Arquitectura conceptual móvil", "Cuatro capas de arquitectura ilustrativa en una columna.", 420, body, width=400)


def activity_fallback_mobile() -> str:
    body = '''<text x="19" y="33" fill="#F8FDFF" font-size="17" font-weight="700">ENGINEERING ACTIVITY</text>
<text x="19" y="60" class="muted">ILLUSTRATION / NO REAL DATA</text><path d="M20 90H380" stroke="#BDEFFF" stroke-opacity=".2"/>
<path d="M20 90L66 77L114 93L163 72L212 88L260 69L310 86L380 75" fill="none" stroke="url(#ice)" stroke-width="2"/>
<text x="19" y="130" class="muted">See verified activity on GitHub</text>'''
    return frame("Actividad ilustrativa móvil", "Gráfico decorativo sin datos de contribución.", 153, body, width=400)


def footer_mobile() -> str:
    body = '''<path d="M18 30H382" stroke="#DDF8FF" stroke-opacity=".2"/><path d="M18 30H107" stroke="url(#ice)" stroke-width="2" stroke-dasharray="8 14" class="trace"/>
<circle cx="18" cy="30" r="4" fill="#BDEFFF" class="pulse"/><text x="200" y="61" text-anchor="middle" class="muted">BUILD · VERIFY · IMPROVE</text>'''
    return frame("Cierre del perfil móvil", "Línea decorativa sutil y lema.", 82, body, width=400)


def connect_mobile() -> str:
    body = '''<text x="19" y="37" fill="#F8FDFF" font-size="17" font-weight="700">LET'S CONNECT</text>
<rect x="18" y="56" width="364" height="51" rx="11" fill="#DDF8FF" fill-opacity=".07" stroke="#DDF8FF" stroke-opacity=".48"/>
<circle cx="39" cy="82" r="5" fill="#BDEFFF" class="pulse"/>
<text x="57" y="88" fill="#F8FDFF" font-size="15" font-weight="700">OPEN GITHUB ↗</text>'''
    return frame("Abrir GitHub en móvil", "Tarjeta de contacto compacta con enlace al perfil.", 126, body, width=400)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    assets = {
        "intro-terminal.svg": intro(),
        "engineering-signal.svg": signal(),
        "project-axiom.svg": project_art("axiom"),
        "project-synapse.svg": project_art("synapse"),
        "tech-network.svg": stack(),
        "delivery-flow.svg": delivery(),
        "architecture.svg": architecture(),
        "activity-fallback.svg": activity_fallback(),
        "footer-pulse.svg": footer(),
        "connect-github.svg": connect(),
        "intro-terminal-mobile.svg": intro_mobile(),
        "engineering-signal-mobile.svg": signal_mobile(),
        "tech-network-mobile.svg": stack_mobile(),
        "delivery-flow-mobile.svg": delivery_mobile(),
        "architecture-mobile.svg": architecture_mobile(),
        "activity-fallback-mobile.svg": activity_fallback_mobile(),
        "footer-pulse-mobile.svg": footer_mobile(),
        "connect-github-mobile.svg": connect_mobile(),
    }
    for name, content in assets.items():
        (OUTPUT / name).write_text(content + "\n", encoding="utf-8")
    print(f"Generated {len(assets)} profile assets in {OUTPUT}")


if __name__ == "__main__":
    main()
