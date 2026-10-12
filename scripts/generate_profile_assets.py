#!/usr/bin/env python3
"""Generate the animated SVG assets used by the GitHub profile README."""

from __future__ import annotations

import math
import random
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SEED = 20261011
KALI_PATH = (
    "M12.778 5.943s-1.97-.13-5.327.92c-3.42 1.07-5.36 2.587-5.36 2.587s5.098-2.847 "
    "10.852-3.008zm7.351 3.095.257-.017s-1.468-1.78-4.278-2.648c1.58.642 2.954 "
    "1.493 4.021 2.665zm.42.74c.039-.068.166.217.263.337.004.024.01.039-.045.027-.005-.025-.013-.032-.013-.032s-.135-.08-.177-.137c-.041-.057-.049-.157-.028-.195zm3.448 "
    "8.479s.312-3.578-5.31-4.403a18.277 18.277 0 0 0-2.524-.187c-4.506.06-4.67-5.197-1.275-5.462 "
    "1.407-.116 3.087.643 4.73 1.408-.007.204.002.385.136.552.134.168.648.35.813.445.164.094.691.43 "
    "1.014.85.07-.131.654-.512.654-.512s-.14.003-.465-.119c-.326-.122-.713-.49-.722-.511-.01-.022-.015-.055.06-.07.059-.049-.072-.207-.13-.265-.058-.058-.445-.716-.454-.73-.009-.016-.012-.031-.04-.05-.085-.027-.46.04-.46.04s-.575-.283-.774-.893c.003.107-.099.224 0 .469-.3-.127-.558-.344-.762-.88-.12.305 0 .499 0 .499s-.707-.198-.82-.85c-.124.293 0 .469 0 .469s-1.153-.602-3.069-.61c-1.283-.118-1.55-2.374-1.43-2.754 0 0-1.85-.975-5.493-1.406-3.642-.43-6.628-.065-6.628-.065s6.45-.31 11.617 1.783c.176.785.704 2.094.989 2.723-.815.563-1.733 1.092-1.876 2.97-.143 1.878 1.472 3.53 3.474 3.58 1.9.102 3.214.116 4.806.942 1.52.84 2.766 3.4 2.89 5.703.132-1.709-.509-5.383-3.5-6.498 4.181.732 4.549 3.832 4.549 3.832zM12.68 5.663l-.15-.485s-2.484-.441-5.822-.204C3.37 5.211 0 6.38 0 6.38s6.896-1.735 12.68-.717Z"
)


def write_asset(name: str, content: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content.strip() + "\n", encoding="utf-8")


def kali_mask_points(size: int = 220, count: int = 620) -> list[tuple[int, int]]:
    source = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24"><path fill="#000" d="{KALI_PATH}"/></svg>'
    )
    with tempfile.TemporaryDirectory(prefix="kali-particles-") as temp_dir:
        source_path = Path(temp_dir) / "kali.svg"
        source_path.write_text(source, encoding="utf-8")
        subprocess.run(
            ["qlmanage", "-t", "-s", str(size), "-o", temp_dir, str(source_path)],
            capture_output=True,
            check=True,
        )
        preview_path = Path(temp_dir) / "kali.svg.png"
        command = [
            "ffmpeg", "-loglevel", "error", "-i", str(preview_path),
            "-vf", f"scale={size}:{size}", "-frames:v", "1", "-f", "rawvideo",
            "-pix_fmt", "rgba", "pipe:1",
        ]
        pixels = subprocess.run(command, capture_output=True, check=True).stdout
    visible: list[tuple[int, int]] = []
    for y in range(size):
        for x in range(size):
            offset = (y * size + x) * 4
            if sum(pixels[offset:offset + 3]) / 3 < 180:
                visible.append((x, y))
    if not visible:
        raise RuntimeError("Kali silhouette produced no visible pixels")
    rng = random.Random(SEED)
    return rng.sample(visible, min(count, len(visible)))


def particles() -> str:
    rng = random.Random(SEED)
    dots: list[str] = []
    for index, (px, py) in enumerate(kali_mask_points()):
        target_x = 750 + px * 1.55
        target_y = 103 + py * 1.55
        angle = rng.random() * math.tau
        distance = rng.uniform(150, 390)
        start_x = 921 + math.cos(angle) * distance
        start_y = 274 + math.sin(angle) * distance * .68
        release_angle = angle + rng.uniform(-1.1, 1.1)
        end_x = target_x + math.cos(release_angle) * rng.uniform(170, 330)
        end_y = target_y + math.sin(release_angle) * rng.uniform(110, 260)
        arrival = .20 + (index % 13) * .006
        radius = rng.choice((1.1, 1.3, 1.5, 1.8, 2.1))
        color = rng.choices(("#FFFFFF", "#38BDF8", "#8B5CF6"), (72, 20, 8))[0]
        opacity = rng.uniform(.7, 1)
        dots.append(
            f'<circle class="particle" cx="{start_x:.1f}" cy="{start_y:.1f}" r="{radius}" '
            f'fill="{color}" opacity="{opacity:.2f}">'
            f'<animate attributeName="cx" values="{start_x:.1f};{target_x:.1f};{target_x:.1f};'
            f'{end_x:.1f};{start_x:.1f}" keyTimes="0;{arrival:.3f};.64;.84;1" dur="10s" '
            'calcMode="spline" keySplines=".2 .8 .2 1;.2 .8 .2 1;.4 0 .6 1;.4 0 .6 1" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{start_y:.1f};{target_y:.1f};{target_y:.1f};'
            f'{end_y:.1f};{start_y:.1f}" keyTimes="0;{arrival:.3f};.64;.84;1" dur="10s" '
            'calcMode="spline" keySplines=".2 .8 .2 1;.2 .8 .2 1;.4 0 .6 1;.4 0 .6 1" repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values=".05;1;1;.12;.05" '
            f'keyTimes="0;{arrival:.3f};.64;.84;1" dur="10s" repeatCount="indefinite"/>'
            '</circle>'
        )
    return "".join(dots)


def banner() -> str:
    particle_markup = particles()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560" role="img" aria-labelledby="title desc">
  <title id="title">Bryan — React, Kali Linux, ciberseguridad e inteligencia artificial</title>
  <desc id="desc">Ventana macOS animada donde cientos de partículas forman y dispersan el logo de Kali Linux en un bucle.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0A0A0F"/><stop offset=".55" stop-color="#0D1018"/><stop offset="1" stop-color="#07080D"/></linearGradient>
    <radialGradient id="aura"><stop stop-color="#38BDF8" stop-opacity=".2"/><stop offset=".48" stop-color="#7C3AED" stop-opacity=".11"/><stop offset="1" stop-opacity="0"/></radialGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#7C3AED"/><stop offset="1" stop-color="#38BDF8"/></linearGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#FFF" stroke-opacity=".035"/></pattern>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="visual"><rect x="656" y="86" width="500" height="400" rx="16"/></clipPath>
    <style>
      text{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}} .white{{fill:#FFF}} .muted{{fill:#A7ADBB}} .cyan{{fill:#38BDF8}}
      .blink{{animation:blink 1s steps(1,end) infinite}} .scan{{animation:scan 4s linear infinite}} .dash{{animation:dash 11s linear infinite}} .pulse{{animation:pulse 2.8s ease-in-out infinite}}
      @keyframes blink{{0%,48%{{opacity:1}}49%,100%{{opacity:.12}}}} @keyframes scan{{0%{{transform:translateY(-20px);opacity:0}}12%,78%{{opacity:.5}}100%{{transform:translateY(385px);opacity:0}}}}
      @keyframes dash{{to{{stroke-dashoffset:-160}}}} @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
      @media(prefers-reduced-motion:reduce){{.scan,.dash,.blink,.pulse{{animation:none!important}}}}
    </style>
    <path id="kali" d="{KALI_PATH}"/>
  </defs>
  <rect width="1200" height="560" rx="28" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="558" rx="27" fill="none" stroke="#FFF" stroke-opacity=".12" stroke-width="2"/>
  <ellipse cx="915" cy="275" rx="350" ry="270" fill="url(#aura)"/><rect x="18" y="18" width="1164" height="524" rx="22" fill="url(#grid)"/>
  <rect x="42" y="42" width="1116" height="476" rx="20" fill="#13131A" fill-opacity=".83" stroke="#FFF" stroke-opacity=".12"/><path d="M42 94H1158" stroke="#FFF" stroke-opacity=".1"/>
  <circle cx="72" cy="68" r="7" fill="#FF5F57"/><circle cx="96" cy="68" r="7" fill="#FEBC2E"/><circle cx="120" cy="68" r="7" fill="#28C840"/>
  <text x="600" y="73" text-anchor="middle" class="muted" font-size="14">bryan@kali — identity.sh</text><text x="1126" y="73" text-anchor="end" fill="#FFF" fill-opacity=".42" font-size="11">ENCRYPTED / ACTIVE</text>
  <g transform="translate(78 132)">
    <text class="cyan" font-size="15" font-weight="700">┌──(bryan㉿kali)-[~/github]</text><text y="32" class="white" font-size="16">└─$ ./profile --build <tspan class="blink" fill="#38BDF8">▌</tspan></text>
    <text y="92" class="white" font-size="42" font-weight="800" letter-spacing="2">BRYAN</text><rect y="109" width="104" height="4" rx="2" fill="url(#accent)"/>
    <text y="145" class="muted" font-size="16">React-first product developer</text><text y="174" class="muted" font-size="16">with a security mindset.</text>
    <path d="M0 207H510" stroke="#FFF" stroke-opacity=".11"/>
    <text y="242" class="muted" font-size="13">CORE</text><text x="90" y="242" class="white" font-size="13">React · TypeScript · Expo</text>
    <text y="273" class="muted" font-size="13">SEC</text><text x="90" y="273" class="white" font-size="13">Kali · Linux · ethical labs</text>
    <text y="304" class="muted" font-size="13">AI</text><text x="90" y="304" class="white" font-size="13">Claude · Codex · Antigravity</text>
    <rect y="338" width="510" height="46" rx="12" fill="#FFF" fill-opacity=".045" stroke="#FFF" stroke-opacity=".1"/><circle cx="21" cy="361" r="4" fill="#28C840" class="pulse"/>
    <text x="38" y="366" class="white" font-size="12">BUILDING PRODUCTS / TESTING SYSTEMS / SHIPPING</text>
  </g>
  <g clip-path="url(#visual)">
    <rect x="656" y="86" width="500" height="400" fill="#090B11" fill-opacity=".62"/><path d="M656 426L1156 146M656 482L1156 202M656 370L1156 90" stroke="#38BDF8" stroke-opacity=".04"/>
    <circle cx="921" cy="274" r="168" fill="none" stroke="#FFF" stroke-opacity=".065"/><circle cx="921" cy="274" r="139" fill="none" stroke="#38BDF8" stroke-opacity=".18" stroke-dasharray="4 14" class="dash"/>
    <g opacity=".2" transform="translate(750 103) scale(14.2)"><use href="#kali" fill="#38BDF8" filter="url(#glow)"/><animate attributeName="opacity" values="0;0;.2;.2;0;0" keyTimes="0;.2;.29;.62;.72;1" dur="10s" repeatCount="indefinite"/></g>
    <g shape-rendering="geometricPrecision">{particle_markup}</g>
    <rect class="scan" x="686" y="95" width="440" height="3" fill="#38BDF8" opacity="0" filter="url(#glow)"/>
  </g>
  <rect x="656" y="86" width="500" height="400" rx="16" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g font-size="10" letter-spacing="1"><text x="680" y="111" fill="#FFF" fill-opacity=".55">PARTICLE ENGINE / 620 NODES</text><text x="1132" y="111" text-anchor="end" class="cyan">KALI // LOOP ∞</text></g>
  <g transform="translate(680 450)"><rect width="452" height="22" rx="11" fill="#080A10" stroke="#FFF" stroke-opacity=".1"/><rect x="4" y="4" width="110" height="14" rx="7" fill="url(#accent)" opacity=".7"><animate attributeName="x" values="4;334;4" dur="10s" repeatCount="indefinite"/></rect><text x="226" y="15" text-anchor="middle" class="white" font-size="9" letter-spacing="1.6">SCATTER → FORM → HOLD → RELEASE</text></g>
</svg>'''


def about() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
  <title id="title">Perfil profesional de Bryan</title><desc id="desc">Dos ventanas macOS animadas resumen su forma de construir producto y pensar en seguridad.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#11131B"/></linearGradient><linearGradient id="line"><stop stop-color="#7C3AED"/><stop offset="1" stop-color="#38BDF8"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>text{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}.w{fill:#FFF}.m{fill:#A7ADBB}.c{fill:#38BDF8}.reveal{animation:show 8s ease-in-out infinite}.flow{animation:flow 3s linear infinite}@keyframes show{0%,12%{opacity:.15}24%,82%{opacity:1}100%{opacity:.15}}@keyframes flow{to{stroke-dashoffset:-40}}@media(prefers-reduced-motion:reduce){.reveal,.flow{animation:none!important;opacity:1}}</style></defs>
  <rect width="1200" height="360" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="358" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g transform="translate(34 30)"><rect width="704" height="300" rx="18" fill="#13131A" fill-opacity=".88" stroke="#FFF" stroke-opacity=".12"/><path d="M0 48H704" stroke="#FFF" stroke-opacity=".1"/><circle cx="25" cy="24" r="6" fill="#FF5F57"/><circle cx="47" cy="24" r="6" fill="#FEBC2E"/><circle cx="69" cy="24" r="6" fill="#28C840"/><text x="352" y="29" text-anchor="middle" class="m" font-size="12">mission.md — edited</text>
  <text x="34" y="87" class="c" font-size="14">01</text><text x="76" y="87" class="w" font-size="14" font-weight="700">product:</text><text x="184" y="87" class="m" font-size="14">ideas → useful experiences</text>
  <g class="reveal" style="animation-delay:.4s"><text x="34" y="127" class="c" font-size="14">02</text><text x="76" y="127" class="w" font-size="14" font-weight="700">frontend:</text><text x="184" y="127" class="m" font-size="14">React · TypeScript · Expo</text></g>
  <g class="reveal" style="animation-delay:.8s"><text x="34" y="167" class="c" font-size="14">03</text><text x="76" y="167" class="w" font-size="14" font-weight="700">security:</text><text x="184" y="167" class="m" font-size="14">observe · test · strengthen</text></g>
  <g class="reveal" style="animation-delay:1.2s"><text x="34" y="207" class="c" font-size="14">04</text><text x="76" y="207" class="w" font-size="14" font-weight="700">method:</text><text x="184" y="207" class="m" font-size="14">build · verify · improve</text></g>
  <path d="M34 239H670" stroke="#FFF" stroke-opacity=".1"/><rect x="34" y="258" width="636" height="18" rx="9" fill="#FFF" fill-opacity=".04"/><rect x="38" y="262" width="218" height="10" rx="5" fill="url(#line)"><animate attributeName="width" values="84;410;218;84" dur="8s" repeatCount="indefinite"/></rect></g>
  <g transform="translate(766 30)"><rect width="400" height="300" rx="18" fill="#13131A" fill-opacity=".72" stroke="#FFF" stroke-opacity=".12"/><text x="28" y="37" class="m" font-size="11" letter-spacing="1.4">OPERATING PRINCIPLES</text><path d="M28 56H372" stroke="#FFF" stroke-opacity=".1"/>
  <g transform="translate(200 163)"><circle r="101" fill="#38BDF8" fill-opacity=".03" stroke="#FFF" stroke-opacity=".08"/><circle r="73" fill="none" stroke="#38BDF8" stroke-opacity=".32" stroke-dasharray="6 10" class="flow"/><path d="M0-73L63 36.5L-63 36.5Z" fill="#7C3AED" fill-opacity=".09" stroke="url(#line)"/><circle cy="-73" r="7" fill="#38BDF8" filter="url(#glow)"/><circle cx="63" cy="36.5" r="7" fill="#FFF"/><circle cx="-63" cy="36.5" r="7" fill="#8B5CF6"/><text y="-91" text-anchor="middle" class="w" font-size="10">CLARITY</text><text x="83" y="42" class="w" font-size="10">QUALITY</text><text x="-83" y="42" text-anchor="end" class="w" font-size="10">SECURITY</text><text y="5" text-anchor="middle" class="w" font-size="12" font-weight="700">SHIP</text></g></g>
</svg>'''


def react_focus() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="350" viewBox="0 0 1200 350" role="img" aria-labelledby="title desc">
  <title id="title">React como centro del trabajo de Bryan</title><desc id="desc">Una animación conecta React con producto, móvil, datos y despliegue.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#10131B"/></linearGradient><linearGradient id="accent"><stop stop-color="#7C3AED"/><stop offset="1" stop-color="#38BDF8"/></linearGradient><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>text{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}.w{fill:#FFF}.m{fill:#A7ADBB}.orbit{animation:spin 12s linear infinite;transform-origin:190px 175px}.dash{animation:dash 2.4s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}@keyframes dash{to{stroke-dashoffset:-38}}@media(prefers-reduced-motion:reduce){.orbit,.dash{animation:none!important}}</style></defs>
  <rect width="1200" height="350" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="348" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g><circle cx="190" cy="175" r="116" fill="#38BDF8" fill-opacity=".035"/><g class="orbit" fill="none" stroke="#61DAFB" stroke-width="3"><ellipse cx="190" cy="175" rx="92" ry="35"/><ellipse cx="190" cy="175" rx="92" ry="35" transform="rotate(60 190 175)"/><ellipse cx="190" cy="175" rx="92" ry="35" transform="rotate(120 190 175)"/></g><circle cx="190" cy="175" r="14" fill="#61DAFB" filter="url(#glow)"><animate attributeName="r" values="12;16;12" dur="2.8s" repeatCount="indefinite"/></circle></g>
  <text x="350" y="92" class="m" font-size="12" letter-spacing="1.8">PRIMARY FRONTEND SYSTEM</text><text x="350" y="145" class="w" font-size="34" font-weight="800">React turns ideas into products.</text><text x="350" y="183" class="m" font-size="15">Reusable UI · real data · thoughtful interaction · verified delivery</text>
  <path d="M350 224H1120" stroke="#FFF" stroke-opacity=".1"/><path d="M390 266H1080" fill="none" stroke="#38BDF8" stroke-opacity=".42" stroke-width="2" stroke-dasharray="7 12" class="dash"/>
  <g font-size="11" text-anchor="middle"><g transform="translate(390 266)"><circle r="19" fill="#13131A" stroke="#38BDF8"/><circle r="5" fill="#38BDF8"/><text y="42" class="w">IDEA</text></g><g transform="translate(562 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#FFF"/><text y="42" class="w">COMPONENTS</text></g><g transform="translate(735 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#8B5CF6"/><text y="42" class="w">DATA</text></g><g transform="translate(907 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#28C840"/><text y="42" class="w">VERIFY</text></g><g transform="translate(1080 266)"><circle r="19" fill="url(#accent)"/><circle r="5" fill="#FFF"/><text y="42" class="w">SHIP</text></g></g>
  <circle r="4" fill="#FFF" filter="url(#glow)"><animateMotion path="M390 266H1080" dur="3.2s" repeatCount="indefinite"/></circle>
</svg>'''


def ai_toolchain() -> str:
    cards = [
        ("CLAUDE", "reason · structure", "#D97757", "ANTHROPIC"),
        ("CODEX", "build · test · review", "#38BDF8", "OPENAI"),
        ("ANTIGRAVITY", "agents · orchestration", "#8B5CF6", "GOOGLE"),
        ("GEMINI", "research · multimodal", "#4285F4", "GOOGLE"),
        ("COPILOT", "pair · accelerate", "#FFFFFF", "GITHUB"),
    ]
    parts: list[str] = []
    for i, (name, purpose, color, maker) in enumerate(cards):
        x = 38 + i * 227
        delay = i * .45
        parts.append(f'''<g transform="translate({x} 104)"><g class="card" style="animation-delay:{delay}s"><rect width="208" height="164" rx="18" fill="#13131A" fill-opacity=".82" stroke="#FFF" stroke-opacity=".11"/><rect x="16" y="16" width="42" height="42" rx="12" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".7"/><circle cx="37" cy="37" r="7" fill="{color}" filter="url(#glow)"><animate attributeName="r" values="5;8;5" dur="{2.6 + i * .25:.2f}s" repeatCount="indefinite"/></circle><text x="16" y="84" class="w" font-size="15" font-weight="800">{name}</text><text x="16" y="108" class="m" font-size="10">{maker}</text><path d="M16 122H192" stroke="#FFF" stroke-opacity=".08"/><text x="16" y="146" fill="{color}" font-size="10">{purpose}</text></g></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">Ecosistema de inteligencia artificial</title><desc id="desc">Claude, Codex, Google Antigravity, Gemini y GitHub Copilot dentro de un flujo humano y verificable.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#10131B"/></linearGradient><linearGradient id="accent"><stop stop-color="#7C3AED"/><stop offset="1" stop-color="#38BDF8"/></linearGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>text{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}}.w{{fill:#FFF}}.m{{fill:#A7ADBB}}.card{{animation:float 4.8s ease-in-out infinite}}.flow{{animation:flow 3s linear infinite}}@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}@keyframes flow{{to{{stroke-dashoffset:-36}}}}@media(prefers-reduced-motion:reduce){{.card,.flow{{animation:none!important}}}}</style></defs>
  <rect width="1200" height="320" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="318" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <text x="38" y="43" class="w" font-size="17" font-weight="800">AI TOOLCHAIN</text><text x="1162" y="43" text-anchor="end" class="m" font-size="11">HUMAN-DIRECTED / VERIFIED OUTPUT</text><path d="M38 67H1162" stroke="url(#accent)" stroke-opacity=".55" stroke-dasharray="8 10" class="flow"/>
  {''.join(parts)}
  <text x="600" y="300" text-anchor="middle" class="m" font-size="10" letter-spacing="1.2">CONTEXT → DELEGATE → REVIEW → TEST → SHIP</text>
</svg>'''


def main() -> None:
    write_asset("banner-kali.svg", banner())
    write_asset("about-terminal.svg", about())
    write_asset("react-focus.svg", react_focus())
    write_asset("ai-toolchain.svg", ai_toolchain())
    print("Generated banner-kali.svg, about-terminal.svg, react-focus.svg, ai-toolchain.svg")


if __name__ == "__main__":
    main()
