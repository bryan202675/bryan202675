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

CLAUDE_PATH = "m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z"
OPENAI_PATH = "M37.5324 16.8707C37.9808 15.5241 38.1363 14.0974 37.9886 12.6859C37.8409 11.2744 37.3934 9.91076 36.676 8.68622C35.6126 6.83404 33.9882 5.3676 32.0373 4.4985C30.0864 3.62941 27.9098 3.40259 25.8215 3.85078C24.8796 2.7893 23.7219 1.94125 22.4257 1.36341C21.1295.785575 19.7249.491269 18.3058.500197C16.1708.495044 14.0893 1.16803 12.3614 2.42214C10.6335 3.67624 9.34853 5.44666 8.6917 7.47815C7.30085 7.76286 5.98686 8.3414 4.8377 9.17505C3.68854 10.0087 2.73073 11.0782 2.02839 12.312C.956464 14.1591.498905 16.2988.721698 18.4228C.944492 20.5467 1.83612 22.5449 3.268 24.1293C2.81966 25.4759 2.66413 26.9026 2.81182 28.3141C2.95951 29.7256 3.40701 31.0892 4.12437 32.3138C5.18791 34.1659 6.8123 35.6322 8.76321 36.5013C10.7141 37.3704 12.8907 37.5973 14.9789 37.1492C15.9208 38.2107 17.0786 39.0587 18.3747 39.6366C19.6709 40.2144 21.0755 40.5087 22.4946 40.4998C24.6307 40.5054 26.7133 39.8321 28.4418 38.5772C30.1704 37.3223 31.4556 35.5506 32.1119 33.5179C33.5027 33.2332 34.8167 32.6547 35.9659 31.821C37.115 30.9874 38.0728 29.9178 38.7752 28.684C39.8458 26.8371 40.3023 24.6979 40.0789 22.5748C39.8556 20.4517 38.9639 18.4544 37.5324 16.8707ZM22.4978 37.8849C20.7443 37.8874 19.0459 37.2733 17.6994 36.1501L25.9004 31.4156C26.3003 31.1882 26.5549 30.7424 26.5549 30.2825V19.0542L29.9867 21.0902V30.3889C29.9842 34.519 26.6278 37.876 22.4978 37.8849ZM6.39227 31.0064C5.51397 29.4888 5.19742 27.7107 5.49804 25.9832L13.699 30.7248C14.096 30.9568 14.6103 30.9568 15.0073 30.7248L24.731 25.1103V29.1012L16.6317 33.7497C13.0537 35.8113 8.46128 34.5811 6.39227 31.0064ZM4.29707 13.6194C5.17156 12.0998 6.55279 10.9364 8.19885 10.3327L8.19491 19.808C8.19211 20.2676 8.44923 20.713 8.84863 20.9404L18.5723 26.5542L15.0924 28.5082L7.04046 23.8557C3.46465 21.7844 2.23536 17.2006 4.29707 13.6194ZM31.955 20.0556L22.2312 14.4411L25.7111 12.4879L33.7631 17.1364C37.3386 19.2018 38.5678 23.7894 36.4938 27.3633C35.6187 28.8716 34.2462 30.0244 32.6047 30.6641V21.188C32.6085 20.7292 32.353 20.2755 31.955 20.0556ZM35.3055 15.0128L27.1045 10.2712C26.7075 10.0396 26.1933 10.0396 25.7963 10.2712L16.0726 15.8858V11.8949L24.1719 7.25025C27.7491 5.18849 32.3404 6.41939 34.4074 9.99411C35.2813 11.5059 35.5978 13.282 35.3055 15.0128ZM14.2424 21.9419L10.8098 19.9058V10.6071C10.8125 6.47706 14.171 3.12474 18.3058 3.11513C20.0516 3.11274 21.7422 3.72294 23.1034 4.85067L14.9024 9.58517C14.5026 9.81239 14.2479 10.2579 14.2479 10.7175L14.2424 21.9419ZM16.071 17.9991L20.4018 15.4978L24.7325 17.9975V22.9985L20.4018 25.4983L16.071 22.9985V17.9991Z"
ANTIGRAVITY_PATH = "M144.248 149.062C151.748 154.688 162.998 150.938 152.685 140.625C121.748 110.625 128.31 28.125 89.8727 28.125C51.4352 28.125 57.9977 110.625 27.0602 140.625C15.8102 151.875 27.9977 154.688 35.4977 149.062C64.5602 129.375 62.6852 94.6875 89.8727 94.6875C117.06 94.6875 115.185 129.375 144.248 149.062Z"
GEMINI_PATH = "M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81"
COPILOT_PATH = "M23.922 16.997C23.061 18.492 18.063 22.02 12 22.02 5.937 22.02.939 18.492.078 16.997A.641.641 0 0 1 0 16.741v-2.869a.883.883 0 0 1 .053-.22c.372-.935 1.347-2.292 2.605-2.656.167-.429.414-1.055.644-1.517a10.098 10.098 0 0 1-.052-1.086c0-1.331.282-2.499 1.132-3.368.397-.406.89-.717 1.474-.952C7.255 2.937 9.248 1.98 11.978 1.98c2.731 0 4.767.957 6.166 2.093.584.235 1.077.546 1.474.952.85.869 1.132 2.037 1.132 3.368 0 .368-.014.733-.052 1.086.23.462.477 1.088.644 1.517 1.258.364 2.233 1.721 2.605 2.656a.841.841 0 0 1 .053.22v2.869a.641.641 0 0 1-.078.256Zm-11.75-5.992h-.344a4.359 4.359 0 0 1-.355.508c-.77.947-1.918 1.492-3.508 1.492-1.725 0-2.989-.359-3.782-1.259a2.137 2.137 0 0 1-.085-.104L4 11.746v6.585c1.435.779 4.514 2.179 8 2.179 3.486 0 6.565-1.4 8-2.179v-6.585l-.098-.104s-.033.045-.085.104c-.793.9-2.057 1.259-3.782 1.259-1.59 0-2.738-.545-3.508-1.492a4.359 4.359 0 0 1-.355-.508Zm2.328 3.25c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm-5 0c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm3.313-6.185c.136 1.057.403 1.913.878 2.497.442.544 1.134.938 2.344.938 1.573 0 2.292-.337 2.657-.751.384-.435.558-1.15.558-2.361 0-1.14-.243-1.847-.705-2.319-.477-.488-1.319-.862-2.824-1.025-1.487-.161-2.192.138-2.533.529-.269.307-.437.808-.438 1.578v.021c0 .265.021.562.063.893Zm-1.626 0c.042-.331.063-.628.063-.894v-.02c-.001-.77-.169-1.271-.438-1.578-.341-.391-1.046-.69-2.533-.529-1.505.163-2.347.537-2.824 1.025-.462.472-.705 1.179-.705 2.319 0 1.211.175 1.926.558 2.361.365.414 1.084.751 2.657.751 1.21 0 1.902-.394 2.344-.938.475-.584.742-1.44.878-2.497Z"


def write_asset(name: str, content: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content.strip() + "\n", encoding="utf-8")


def kali_mask_points(size: int = 220, count: int = 900) -> list[tuple[int, int]]:
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
    # Sampling raw pixels over-represents Kali's broad head and leaves its thin
    # tail almost empty. One point per small spatial cell preserves the complete
    # silhouette before the final deterministic sample is taken.
    cells: dict[tuple[int, int], tuple[int, int]] = {}
    for point in visible:
        cell = (point[0] // 2, point[1] // 2)
        cells.setdefault(cell, point)
    candidates = list(cells.values())
    rng = random.Random(SEED)
    if len(candidates) >= count:
        return rng.sample(candidates, count)
    selected = list(candidates)
    selected_set = set(selected)
    remaining = [point for point in visible if point not in selected_set]
    selected.extend(rng.sample(remaining, min(count - len(selected), len(remaining))))
    rng.shuffle(selected)
    return selected


def particles() -> str:
    rng = random.Random(SEED)
    dots: list[str] = []
    for index, (px, py) in enumerate(kali_mask_points()):
        target_x = 770 + px * 2
        target_y = 85 + py * 2
        angle = rng.random() * math.tau
        distance = rng.uniform(180, 410)
        start_x = 921 + math.cos(angle) * distance
        start_y = 274 + math.sin(angle) * distance * .68
        orbit_angle = angle + rng.uniform(.45, 1.25)
        orbit_x = 921 + math.cos(orbit_angle) * rng.uniform(150, 250)
        orbit_y = 274 + math.sin(orbit_angle) * rng.uniform(105, 185)
        magnet_x = target_x + math.cos(angle) * rng.uniform(24, 68)
        magnet_y = target_y + math.sin(angle) * rng.uniform(18, 52)
        release_angle = angle + rng.uniform(-1.1, 1.1)
        end_x = target_x + math.cos(release_angle) * rng.uniform(170, 330)
        end_y = target_y + math.sin(release_angle) * rng.uniform(110, 260)
        arrival = .29 + (index % 11) * .005
        radius = rng.choice((.9, 1.1, 1.3, 1.5, 1.8))
        color = rng.choices(("#FFFFFF", "#ECFBFF", "#BDEFFF"), (64, 26, 10))[0]
        opacity = rng.uniform(.7, 1)
        dots.append(
            f'<circle class="particle" cx="{start_x:.1f}" cy="{start_y:.1f}" r="{radius}" '
            f'fill="{color}" opacity="{opacity:.2f}">'
            f'<animate attributeName="cx" values="{start_x:.1f};{orbit_x:.1f};{magnet_x:.1f};{target_x:.1f};'
            f'{target_x:.1f};{end_x:.1f};{start_x:.1f}" keyTimes="0;.12;.24;{arrival:.3f};.68;.86;1" dur="12s" '
            'calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.2 .8 .2 1;.2 .8 .2 1;.4 0 .6 1;.4 0 .6 1" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{start_y:.1f};{orbit_y:.1f};{magnet_y:.1f};{target_y:.1f};'
            f'{target_y:.1f};{end_y:.1f};{start_y:.1f}" keyTimes="0;.12;.24;{arrival:.3f};.68;.86;1" dur="12s" '
            'calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.2 .8 .2 1;.2 .8 .2 1;.4 0 .6 1;.4 0 .6 1" repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values=".03;.22;.7;1;1;.16;.03" '
            f'keyTimes="0;.12;.24;{arrival:.3f};.68;.86;1" dur="12s" repeatCount="indefinite"/>'
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
    <radialGradient id="aura"><stop stop-color="#F4FDFF" stop-opacity=".2"/><stop offset=".48" stop-color="#AEEBFF" stop-opacity=".07"/><stop offset="1" stop-opacity="0"/></radialGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#FFFFFF"/><stop offset=".5" stop-color="#E8FAFF"/><stop offset="1" stop-color="#9EE7FF"/></linearGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#FFF" stroke-opacity=".035"/></pattern>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="visual"><rect x="656" y="86" width="500" height="400" rx="16"/></clipPath>
    <style>
      text{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}} .white{{fill:#FFF}} .muted{{fill:#AEB9C5}} .cyan{{fill:#DDF8FF}}
      .blink{{animation:blink 1s steps(1,end) infinite}} .scan{{animation:scan 4s linear infinite}} .dash{{animation:dash 11s linear infinite}} .pulse{{animation:pulse 2.8s ease-in-out infinite}}
      @keyframes blink{{0%,48%{{opacity:1}}49%,100%{{opacity:.12}}}} @keyframes scan{{0%{{transform:translateX(-24px);opacity:0}}12%,78%{{opacity:.58}}100%{{transform:translateX(448px);opacity:0}}}}
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
    <text class="cyan" font-size="15" font-weight="700">┌──(bryan㉿kali)-[~/github]</text><text y="32" class="white" font-size="16">└─$ ./profile --build <tspan class="blink" fill="#DDF8FF">▌</tspan></text>
    <text y="92" class="white" font-size="42" font-weight="800" letter-spacing="2">BRYAN</text><rect y="109" width="104" height="4" rx="2" fill="url(#accent)"/>
    <text y="145" class="muted" font-size="16">React-first product developer</text><text y="174" class="muted" font-size="16">with a security mindset.</text>
    <path d="M0 207H510" stroke="#FFF" stroke-opacity=".11"/>
    <text y="242" class="muted" font-size="13">CORE</text><text x="90" y="242" class="white" font-size="13">React · TypeScript · Expo</text>
    <text y="273" class="muted" font-size="13">SEC</text><text x="90" y="273" class="white" font-size="13">Kali · Linux · ethical labs</text>
    <text y="304" class="muted" font-size="13">AI</text><text x="90" y="304" class="white" font-size="13">Claude · Codex · Antigravity</text>
    <rect y="338" width="510" height="46" rx="12" fill="#FFF" fill-opacity=".045" stroke="#FFF" stroke-opacity=".1"/><circle cx="21" cy="361" r="4" fill="#DDF8FF" class="pulse" filter="url(#glow)"/>
    <text x="38" y="366" class="white" font-size="12">BUILDING PRODUCTS / TESTING SYSTEMS / SHIPPING</text>
  </g>
  <g clip-path="url(#visual)">
    <rect x="656" y="86" width="500" height="400" fill="#090B11" fill-opacity=".62"/><path d="M656 426L1156 146M656 482L1156 202M656 370L1156 90" stroke="#DDF8FF" stroke-opacity=".035"/>
    <circle cx="921" cy="274" r="168" fill="none" stroke="#FFF" stroke-opacity=".065"/><circle cx="921" cy="274" r="139" fill="none" stroke="#DDF8FF" stroke-opacity=".2" stroke-dasharray="4 14" class="dash"/>
    <g opacity=".26" transform="translate(782 89) scale(12.8)"><use href="#kali" fill="#E8FAFF" filter="url(#glow)"/><animate attributeName="opacity" values="0;0;.08;.26;.26;.06;0" keyTimes="0;.18;.25;.31;.68;.86;1" dur="12s" repeatCount="indefinite"/></g>
    <g shape-rendering="geometricPrecision">{particle_markup}</g>
    <rect class="scan" x="680" y="118" width="3" height="330" fill="#F4FDFF" opacity="0" filter="url(#glow)"/>
  </g>
  <rect x="656" y="86" width="500" height="400" rx="16" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g font-size="10" letter-spacing="1"><text x="680" y="111" fill="#FFF" fill-opacity=".55">PARTICLE ENGINE / 900 NODES</text><text x="1132" y="111" text-anchor="end" class="cyan">KALI // ICE LOOP ∞</text></g>
  <g transform="translate(680 450)"><rect width="452" height="22" rx="11" fill="#080A10" stroke="#FFF" stroke-opacity=".1"/><rect x="4" y="4" width="110" height="14" rx="7" fill="url(#accent)" opacity=".82" filter="url(#glow)"><animate attributeName="x" values="4;334;4" dur="12s" repeatCount="indefinite"/></rect><text x="226" y="15" text-anchor="middle" class="white" font-size="9" letter-spacing="1.6">ORBIT → ASSEMBLE → HOLD → RELEASE</text></g>
</svg>'''


def about() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
  <title id="title">Perfil profesional de Bryan</title><desc id="desc">Dos ventanas macOS animadas resumen su forma de construir producto y pensar en seguridad.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#11131B"/></linearGradient><linearGradient id="line"><stop stop-color="#FFFFFF"/><stop offset=".5" stop-color="#E8FAFF"/><stop offset="1" stop-color="#9EE7FF"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>text{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}.w{fill:#FFF}.m{fill:#AEB9C5}.c{fill:#DDF8FF}.reveal{animation:show 8s ease-in-out infinite}.flow{animation:flow 3s linear infinite}@keyframes show{0%,12%{opacity:.52}24%,82%{opacity:1}100%{opacity:.52}}@keyframes flow{to{stroke-dashoffset:-40}}@media(prefers-reduced-motion:reduce){.reveal,.flow{animation:none!important;opacity:1}}</style></defs>
  <rect width="1200" height="360" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="358" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g transform="translate(34 30)"><rect width="704" height="300" rx="18" fill="#13131A" fill-opacity=".88" stroke="#FFF" stroke-opacity=".12"/><path d="M0 48H704" stroke="#FFF" stroke-opacity=".1"/><circle cx="25" cy="24" r="6" fill="#FF5F57"/><circle cx="47" cy="24" r="6" fill="#FEBC2E"/><circle cx="69" cy="24" r="6" fill="#28C840"/><text x="352" y="29" text-anchor="middle" class="m" font-size="12">mission.md — edited</text>
  <text x="34" y="87" class="c" font-size="14">01</text><text x="76" y="87" class="w" font-size="14" font-weight="700">product:</text><text x="184" y="87" class="m" font-size="14">ideas → useful experiences</text>
  <g class="reveal" style="animation-delay:.4s"><text x="34" y="127" class="c" font-size="14">02</text><text x="76" y="127" class="w" font-size="14" font-weight="700">frontend:</text><text x="184" y="127" class="m" font-size="14">React · TypeScript · Expo</text></g>
  <g class="reveal" style="animation-delay:.8s"><text x="34" y="167" class="c" font-size="14">03</text><text x="76" y="167" class="w" font-size="14" font-weight="700">security:</text><text x="184" y="167" class="m" font-size="14">observe · test · strengthen</text></g>
  <g class="reveal" style="animation-delay:1.2s"><text x="34" y="207" class="c" font-size="14">04</text><text x="76" y="207" class="w" font-size="14" font-weight="700">method:</text><text x="184" y="207" class="m" font-size="14">build · verify · improve</text></g>
  <path d="M34 239H670" stroke="#FFF" stroke-opacity=".1"/><rect x="34" y="258" width="636" height="18" rx="9" fill="#FFF" fill-opacity=".04"/><rect x="38" y="262" width="218" height="10" rx="5" fill="url(#line)"><animate attributeName="width" values="84;410;218;84" dur="8s" repeatCount="indefinite"/></rect></g>
  <g transform="translate(766 30)"><rect width="400" height="300" rx="18" fill="#13131A" fill-opacity=".72" stroke="#FFF" stroke-opacity=".12"/><text x="28" y="37" class="m" font-size="11" letter-spacing="1.4">OPERATING PRINCIPLES</text><path d="M28 56H372" stroke="#FFF" stroke-opacity=".1"/>
  <g transform="translate(200 163)"><circle r="101" fill="#DDF8FF" fill-opacity=".025" stroke="#FFF" stroke-opacity=".08"/><circle r="73" fill="none" stroke="#DDF8FF" stroke-opacity=".36" stroke-dasharray="6 10" class="flow"/><path d="M0-73L63 36.5L-63 36.5Z" fill="#E8FAFF" fill-opacity=".055" stroke="url(#line)"/><circle cy="-73" r="7" fill="#F4FDFF" filter="url(#glow)"/><circle cx="63" cy="36.5" r="7" fill="#DDF8FF" filter="url(#glow)"/><circle cx="-63" cy="36.5" r="7" fill="#BDEFFF" filter="url(#glow)"/><text y="-91" text-anchor="middle" class="w" font-size="10">CLARITY</text><text x="83" y="42" class="w" font-size="10">QUALITY</text><text x="-83" y="42" text-anchor="end" class="w" font-size="10">SECURITY</text><text y="5" text-anchor="middle" class="w" font-size="12" font-weight="700">SHIP</text></g></g>
</svg>'''


def react_focus() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="350" viewBox="0 0 1200 350" role="img" aria-labelledby="title desc">
  <title id="title">React como centro del trabajo de Bryan</title><desc id="desc">Una animación conecta React con producto, móvil, datos y despliegue.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#10131B"/></linearGradient><linearGradient id="accent"><stop stop-color="#FFFFFF"/><stop offset=".5" stop-color="#E8FAFF"/><stop offset="1" stop-color="#9EE7FF"/></linearGradient><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><style>text{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}.w{fill:#FFF}.m{fill:#AEB9C5}.orbit{animation:spin 12s linear infinite;transform-origin:190px 175px}.dash{animation:dash 2.4s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}@keyframes dash{to{stroke-dashoffset:-38}}@media(prefers-reduced-motion:reduce){.orbit,.dash{animation:none!important}}</style></defs>
  <rect width="1200" height="350" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="348" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <g><circle cx="190" cy="175" r="116" fill="#DDF8FF" fill-opacity=".03"/><g class="orbit" fill="none" stroke="#DDF8FF" stroke-width="3" filter="url(#glow)"><ellipse cx="190" cy="175" rx="92" ry="35"/><ellipse cx="190" cy="175" rx="92" ry="35" transform="rotate(60 190 175)"/><ellipse cx="190" cy="175" rx="92" ry="35" transform="rotate(120 190 175)"/></g><circle cx="190" cy="175" r="14" fill="#F4FDFF" filter="url(#glow)"><animate attributeName="r" values="12;16;12" dur="2.8s" repeatCount="indefinite"/></circle></g>
  <text x="350" y="92" class="m" font-size="12" letter-spacing="1.8">PRIMARY FRONTEND SYSTEM</text><text x="350" y="145" class="w" font-size="34" font-weight="800">React turns ideas into products.</text><text x="350" y="183" class="m" font-size="15">Reusable UI · real data · thoughtful interaction · verified delivery</text>
  <path d="M350 224H1120" stroke="#FFF" stroke-opacity=".1"/><path d="M390 266H1080" fill="none" stroke="#DDF8FF" stroke-opacity=".46" stroke-width="2" stroke-dasharray="7 12" class="dash"/>
  <g font-size="11" text-anchor="middle"><g transform="translate(390 266)"><circle r="19" fill="#13131A" stroke="#DDF8FF"/><circle r="5" fill="#F4FDFF" filter="url(#glow)"/><text y="42" class="w">IDEA</text></g><g transform="translate(562 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#E8FAFF"/><text y="42" class="w">COMPONENTS</text></g><g transform="translate(735 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#DDF8FF"/><text y="42" class="w">DATA</text></g><g transform="translate(907 266)"><circle r="19" fill="#13131A" stroke="#FFF" stroke-opacity=".25"/><circle r="5" fill="#BDEFFF"/><text y="42" class="w">VERIFY</text></g><g transform="translate(1080 266)"><circle r="19" fill="url(#accent)" filter="url(#glow)"/><circle r="5" fill="#0A0A0F"/><text y="42" class="w">SHIP</text></g></g>
  <circle r="4" fill="#FFF" filter="url(#glow)"><animateMotion path="M390 266H1080" dur="3.2s" repeatCount="indefinite"/></circle>
</svg>'''


def ai_toolchain() -> str:
    cards = [
        ("CLAUDE", "reason · structure", "ANTHROPIC", "claude"),
        ("CODEX", "build · test · review", "OPENAI", "openai"),
        ("ANTIGRAVITY", "agents · orchestration", "GOOGLE", "antigravity"),
        ("GEMINI", "research · multimodal", "GOOGLE", "gemini"),
        ("COPILOT", "pair · accelerate", "GITHUB", "copilot"),
    ]
    parts: list[str] = []
    for i, (name, purpose, maker, symbol) in enumerate(cards):
        x = 38 + i * 227
        delay = i * .45
        parts.append(f'''<g transform="translate({x} 104)"><g class="card" style="animation-delay:{delay}s"><rect width="208" height="164" rx="18" fill="#13131A" fill-opacity=".82" stroke="#E8FAFF" stroke-opacity=".12"><animate attributeName="stroke-opacity" values=".12;.3;.12" dur="{4.6 + i * .25:.2f}s" repeatCount="indefinite"/></rect><rect x="16" y="16" width="46" height="46" rx="13" fill="#E8FAFF" fill-opacity=".045" stroke="#DDF8FF" stroke-opacity=".36"/><use href="#logo-{symbol}" x="25" y="25" width="28" height="28" color="#F4FDFF" filter="url(#glow)"><animate attributeName="opacity" values=".72;1;.72" dur="{2.8 + i * .22:.2f}s" repeatCount="indefinite"/></use><text x="16" y="88" class="w" font-size="15" font-weight="800">{name}</text><text x="16" y="111" class="m" font-size="10">{maker}</text><path d="M16 124H192" stroke="#FFF" stroke-opacity=".08"/><text x="16" y="148" class="ice" font-size="10">{purpose}</text></g></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">Ecosistema de inteligencia artificial</title><desc id="desc">Claude, Codex, Google Antigravity, Gemini y GitHub Copilot dentro de un flujo humano y verificable.</desc>
  <defs>
    <linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0A0A0F"/><stop offset="1" stop-color="#10131B"/></linearGradient><linearGradient id="accent"><stop stop-color="#FFFFFF"/><stop offset=".5" stop-color="#E8FAFF"/><stop offset="1" stop-color="#9EE7FF"/></linearGradient>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <symbol id="logo-claude" viewBox="0 0 24 24"><path fill="currentColor" d="{CLAUDE_PATH}"/></symbol>
    <symbol id="logo-openai" viewBox="0 0 41 41"><path fill="currentColor" d="{OPENAI_PATH}"/></symbol>
    <symbol id="logo-antigravity" viewBox="0 0 180 180"><path fill="currentColor" d="{ANTIGRAVITY_PATH}"/></symbol>
    <symbol id="logo-gemini" viewBox="0 0 24 24"><path fill="currentColor" d="{GEMINI_PATH}"/></symbol>
    <symbol id="logo-copilot" viewBox="0 0 24 24"><path fill="currentColor" d="{COPILOT_PATH}"/></symbol>
    <style>text{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace}}.w{{fill:#FFF}}.m{{fill:#AEB9C5}}.ice{{fill:#DDF8FF}}.card{{animation:float 5.2s ease-in-out infinite}}.flow{{animation:flow 3s linear infinite}}@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}@keyframes flow{{to{{stroke-dashoffset:-36}}}}@media(prefers-reduced-motion:reduce){{.card,.flow{{animation:none!important}}}}</style>
  </defs>
  <rect width="1200" height="320" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="318" rx="23" fill="none" stroke="#FFF" stroke-opacity=".12"/>
  <text x="38" y="43" class="w" font-size="17" font-weight="800">AI TOOLCHAIN</text><text x="1162" y="43" text-anchor="end" class="m" font-size="11">HUMAN-DIRECTED / VERIFIED OUTPUT</text><path d="M38 67H1162" stroke="url(#accent)" stroke-opacity=".7" stroke-dasharray="8 10" class="flow" filter="url(#glow)"/>
  {''.join(parts)}
  <text x="600" y="300" text-anchor="middle" class="m" font-size="10" letter-spacing="1.2">CONTEXT → DELEGATE → REVIEW → TEST → SHIP</text>
</svg>'''


def main() -> None:
    write_asset("banner-kali-v2.svg", banner())
    write_asset("about-terminal-v2.svg", about())
    write_asset("react-focus-v2.svg", react_focus())
    write_asset("ai-toolchain-v2.svg", ai_toolchain())
    print("Generated versioned ice-neon profile assets")


if __name__ == "__main__":
    main()
